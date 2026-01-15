"""
Core simulation for Poverty Point aggregation model.

This implements the theoretical framework from docs/THEORETICAL_DERIVATION.md
with the architecture defined in docs/ABM_ARCHITECTURE.md.
"""

import numpy as np
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional
from enum import Enum

from .parameters import (
    SimulationParameters, default_parameters,
    W_aggregator, W_independent, cooperation_benefit, critical_threshold
)
from .agents import Band, AggregationSite, Strategy, create_bands, create_aggregation_site


@dataclass
class YearlyState:
    """State snapshot for a single year."""
    year: int

    # Population
    total_population: int
    n_bands: int
    mean_band_size: float

    # Strategy distribution
    n_aggregators: int
    n_independents: int
    strategy_dominance: float  # (n_agg - n_ind) / n_total, in [-1, 1]

    # Aggregation
    aggregation_size: int      # Bands at aggregation
    aggregation_population: int  # Individuals at aggregation

    # Investment
    monument_level: float      # Cumulative
    annual_construction: float # This year
    total_exotics: int

    # Environment
    sigma_effective: float
    in_shortfall: bool
    shortfall_magnitude: float

    # Fitness
    mean_fitness_aggregators: float
    mean_fitness_independents: float


@dataclass
class SimulationResults:
    """Complete results from a simulation run."""
    # Parameters
    sigma: float
    epsilon: float
    seed: int

    # Time series
    yearly_states: List[YearlyState] = field(default_factory=list)

    # Summary statistics (computed after simulation)
    final_strategy_dominance: float = 0.0
    mean_aggregation_size: float = 0.0
    final_monument_level: float = 0.0
    total_exotics: int = 0
    mean_population: float = 0.0

    # Theoretical comparison
    sigma_star_theoretical: float = 0.0

    def compute_summary(self, burn_in: int = 100) -> None:
        """Compute summary statistics from time series."""
        # Use post-burn-in data
        analysis_states = [s for s in self.yearly_states if s.year >= burn_in]

        if not analysis_states:
            return

        self.final_strategy_dominance = np.mean([s.strategy_dominance
                                                  for s in analysis_states])
        self.mean_aggregation_size = np.mean([s.aggregation_size
                                               for s in analysis_states])
        self.final_monument_level = analysis_states[-1].monument_level
        self.total_exotics = analysis_states[-1].total_exotics
        self.mean_population = np.mean([s.total_population
                                         for s in analysis_states])


class PovertyPointSimulation:
    """
    Main simulation class for Poverty Point aggregation model.

    Implements the annual cycle:
    1. Shortfall determination
    2. Dispersal season foraging
    3. Strategy decisions
    4. Aggregation season activities
    5. Shortfall mortality
    6. Reproduction
    7. State recording
    """

    def __init__(self, params: Optional[SimulationParameters] = None):
        """
        Initialize simulation.

        Args:
            params: Simulation parameters (uses defaults if None)
        """
        self.params = params or default_parameters()
        self.rng = np.random.default_rng(self.params.seed)

        # Initialize agents
        self.bands = create_bands(
            n_bands=self.params.population.n_bands,
            initial_size=self.params.population.initial_band_size,
            region_size=self.params.environment.region_size,
            rng=self.rng
        )

        # Initialize aggregation site at center (maximum ecotone)
        center = self.params.environment.region_size / 2
        self.aggregation_site = create_aggregation_site(
            location=(center, center),
            epsilon=self.params.epsilon,
            name="Poverty Point"
        )

        # State tracking
        self.year = 0
        self.in_shortfall = False
        self.shortfall_remaining = 0
        self.shortfall_magnitude = 0.0

        # Results
        self.results = SimulationResults(
            sigma=self.params.sigma,
            epsilon=self.params.epsilon,
            seed=self.params.seed
        )

    def _generate_shortfall(self) -> Tuple[bool, float, int]:
        """
        Generate shortfall event based on σ.

        Higher σ = more frequent, more severe shortfalls.

        Returns:
            (is_shortfall, magnitude, duration)
        """
        sigma = self.params.sigma

        # Frequency: inter-arrival time decreases with σ
        # At σ=0.2: ~15 years; at σ=0.8: ~5 years
        mean_interval = 20 * (1 - sigma) + 5
        p_shortfall = 1.0 / mean_interval

        if self.rng.random() < p_shortfall:
            # Magnitude scales with σ (with noise)
            magnitude = 0.3 + 0.5 * sigma + self.rng.normal(0, 0.1)
            magnitude = np.clip(magnitude, 0.2, 0.9)

            # Duration increases with magnitude
            duration = max(1, int(1 + magnitude * 2.5))

            return True, magnitude, duration

        return False, 0.0, 0

    def _run_dispersal_season(self) -> None:
        """
        Run dispersal season: bands forage independently.

        Resource acquisition depends on strategy:
        - Independents: full foraging
        - Aggregators: reduced foraging (preparing for travel)
        """
        for band in self.bands:
            # Base foraging success
            base_harvest = 0.4 + 0.2 * self.rng.random()

            # Shortfall reduces productivity
            if self.in_shortfall:
                base_harvest *= (1 - self.shortfall_magnitude)

            if band.strategy == Strategy.AGGREGATOR:
                # Reduced foraging (opportunity cost)
                harvest = base_harvest * (1 - self.params.costs.C_opportunity)
            else:
                # Full foraging
                harvest = base_harvest

            # Update resources (with consumption)
            consumption = band.size * 0.02  # Per capita consumption
            band.resources += harvest - consumption
            band.resources = np.clip(band.resources, 0.0, 1.0)

    def _run_strategy_decisions(self) -> None:
        """
        Bands decide their strategy for this year.

        Decision based on expected fitness comparison with memory effects.
        """
        # Estimate expected aggregation size (from last year)
        last_n = self.aggregation_site.n_attending
        expected_n = max(5, last_n)  # Minimum expected

        for band in self.bands:
            band.strategy = band.decide_strategy(
                expected_n=expected_n,
                sigma=self.params.sigma,
                epsilon=self.params.epsilon,
                params=self.params,
                rng=self.rng
            )
            band.strategy_history.append(band.strategy)

    def _run_aggregation_season(self) -> None:
        """
        Run aggregation season.

        Aggregators:
        - Travel to site (pay travel cost)
        - Invest in monuments
        - Acquire exotics
        - Form obligations

        Independents:
        - Continue foraging
        """
        # Reset aggregation site
        self.aggregation_site.reset_annual_state()

        total_construction = 0.0

        for band in self.bands:
            if band.strategy == Strategy.AGGREGATOR:
                # Travel to aggregation site
                travel_cost = band.calculate_travel_cost(
                    self.aggregation_site.location
                )
                band.resources -= min(travel_cost, band.resources * 0.5)

                # Register attendance
                self.aggregation_site.add_attending_band(band)
                band.aggregation_history.append(True)

                # Invest in monument
                investment = band.invest_in_monument(
                    investment_rate=self.params.costs.C_signal,
                    rng=self.rng
                )
                total_construction += investment

                # Attempt exotic acquisition
                band.acquire_exotic(
                    acquisition_cost=0.1,
                    rng=self.rng
                )

                # Form obligations with other attending bands
                if len(self.aggregation_site.attending_bands) > 1:
                    potential_partners = [
                        b_id for b_id in self.aggregation_site.attending_bands
                        if b_id != band.band_id
                    ]
                    if potential_partners and self.rng.random() < 0.3:
                        partner_id = self.rng.choice(potential_partners)
                        band.form_obligation(partner_id)

            else:
                # Independent: continue foraging
                extra_harvest = 0.1 * (1 - self.shortfall_magnitude if self.in_shortfall else 1)
                band.resources += extra_harvest
                band.resources = min(1.0, band.resources)
                band.aggregation_history.append(False)

        # Record construction
        self.aggregation_site.record_construction(total_construction)

    def _apply_shortfall_mortality(self) -> None:
        """
        Apply mortality during shortfall.

        Aggregators: lower mortality (buffered by ecotone + pooling)
        Independents: higher mortality (exposed)
        """
        if not self.in_shortfall:
            return

        for band in self.bands:
            if band.strategy == Strategy.AGGREGATOR:
                # Effective sigma reduced by ecotone
                sigma_eff = self.params.sigma * (1 - self.params.epsilon)
                vulnerability = self.params.vulnerability.alpha_agg
            else:
                sigma_eff = self.params.sigma
                vulnerability = self.params.vulnerability.beta_ind

            # Mortality
            band.suffer_shortfall(vulnerability, sigma_eff, self.rng)

            # Aggregators can call obligations for help
            if band.strategy == Strategy.AGGREGATOR and band.obligations:
                partner_id = self.rng.choice(list(band.obligations.keys()))
                help_received = band.call_obligation(partner_id, need=0.2)
                band.resources += help_received

    def _apply_reproduction(self) -> None:
        """
        Apply reproduction and baseline mortality.

        Fitness affects birth rate.
        """
        for band in self.bands:
            # Calculate realized fitness
            if band.aggregation_history and band.aggregation_history[-1]:
                fitness = W_aggregator(
                    self.params.sigma,
                    self.params.epsilon,
                    self.aggregation_site.n_attending,
                    self.params
                )
            else:
                fitness = W_independent(self.params.sigma, self.params)

            band.fitness_history.append(fitness)

            # Reproduction
            band.reproduce(
                fitness=fitness,
                birth_rate=self.params.population.birth_rate,
                death_rate=self.params.population.death_rate,
                rng=self.rng
            )

            # Band dissolution/fission
            if band.size < self.params.population.min_band_size:
                band.size = self.params.population.min_band_size
            elif band.size > self.params.population.max_band_size:
                band.size = self.params.population.max_band_size

    def _record_state(self) -> YearlyState:
        """
        Record current state.

        Returns:
            YearlyState snapshot
        """
        # Count strategies
        n_agg = sum(1 for b in self.bands if b.strategy == Strategy.AGGREGATOR)
        n_ind = len(self.bands) - n_agg
        n_total = len(self.bands)

        # Strategy dominance
        dominance = (n_agg - n_ind) / n_total if n_total > 0 else 0.0

        # Fitness by strategy
        agg_fitness = [b.fitness_history[-1] for b in self.bands
                       if b.strategy == Strategy.AGGREGATOR and b.fitness_history]
        ind_fitness = [b.fitness_history[-1] for b in self.bands
                       if b.strategy == Strategy.INDEPENDENT and b.fitness_history]

        state = YearlyState(
            year=self.year,
            total_population=sum(b.size for b in self.bands),
            n_bands=len(self.bands),
            mean_band_size=np.mean([b.size for b in self.bands]),
            n_aggregators=n_agg,
            n_independents=n_ind,
            strategy_dominance=dominance,
            aggregation_size=self.aggregation_site.n_attending,
            aggregation_population=self.aggregation_site.current_population,
            monument_level=self.aggregation_site.monument_level,
            annual_construction=(self.aggregation_site.monument_history[-1] -
                                 self.aggregation_site.monument_history[-2]
                                 if len(self.aggregation_site.monument_history) > 1
                                 else self.aggregation_site.monument_level),
            total_exotics=sum(b.exotic_goods for b in self.bands),
            sigma_effective=self.params.sigma * (1 - self.params.epsilon),
            in_shortfall=self.in_shortfall,
            shortfall_magnitude=self.shortfall_magnitude,
            mean_fitness_aggregators=np.mean(agg_fitness) if agg_fitness else 0.0,
            mean_fitness_independents=np.mean(ind_fitness) if ind_fitness else 0.0
        )

        self.results.yearly_states.append(state)
        return state

    def step(self) -> YearlyState:
        """
        Execute one year of simulation.

        Returns:
            State after this year
        """
        # 1. Shortfall determination
        if self.shortfall_remaining > 0:
            self.shortfall_remaining -= 1
            if self.shortfall_remaining == 0:
                self.in_shortfall = False
                self.shortfall_magnitude = 0.0
        else:
            new_shortfall, magnitude, duration = self._generate_shortfall()
            if new_shortfall:
                self.in_shortfall = True
                self.shortfall_magnitude = magnitude
                self.shortfall_remaining = duration

        # 2. Dispersal season
        self._run_dispersal_season()

        # 3. Strategy decisions
        self._run_strategy_decisions()

        # 4. Aggregation season
        self._run_aggregation_season()

        # 5. Shortfall mortality
        self._apply_shortfall_mortality()

        # 6. Reproduction
        self._apply_reproduction()

        # 7. Record state
        state = self._record_state()

        self.year += 1
        return state

    def run(self, verbose: bool = False) -> SimulationResults:
        """
        Run complete simulation.

        Args:
            verbose: Print progress updates

        Returns:
            SimulationResults object
        """
        if verbose:
            print(f"Running simulation: σ={self.params.sigma:.2f}, "
                  f"ε={self.params.epsilon:.2f}")

        for _ in range(self.params.duration):
            self.step()

            if verbose and self.year % 100 == 0:
                state = self.results.yearly_states[-1]
                print(f"  Year {self.year}: Pop={state.total_population}, "
                      f"Dominance={state.strategy_dominance:.2f}, "
                      f"Monument={state.monument_level:.0f}")

        # Compute summary statistics
        self.results.compute_summary(burn_in=self.params.burn_in)

        # Add theoretical comparison
        self.results.sigma_star_theoretical = critical_threshold(
            self.params.epsilon,
            n=self.params.cooperation.n_optimal,
            params=self.params
        )

        if verbose:
            print(f"Complete. Final dominance: {self.results.final_strategy_dominance:.3f}")
            print(f"Theoretical σ*: {self.results.sigma_star_theoretical:.3f}")

        return self.results


def run_single_simulation(sigma: float, epsilon: float, seed: int,
                          duration: int = 600, verbose: bool = False
                          ) -> SimulationResults:
    """
    Convenience function to run a single simulation.

    Args:
        sigma: Environmental uncertainty
        epsilon: Ecotone advantage
        seed: Random seed
        duration: Simulation duration in years
        verbose: Print progress

    Returns:
        SimulationResults object
    """
    params = default_parameters(sigma=sigma, epsilon=epsilon, seed=seed)
    params.duration = duration

    sim = PovertyPointSimulation(params)
    return sim.run(verbose=verbose)


if __name__ == "__main__":
    # Quick test
    results = run_single_simulation(
        sigma=0.55,
        epsilon=0.35,
        seed=42,
        duration=200,
        verbose=True
    )

    print(f"\nFinal Results:")
    print(f"  Strategy dominance: {results.final_strategy_dominance:.3f}")
    print(f"  Mean aggregation: {results.mean_aggregation_size:.1f} bands")
    print(f"  Monument level: {results.final_monument_level:.0f}")
    print(f"  Total exotics: {results.total_exotics}")
