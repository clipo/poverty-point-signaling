"""
Core simulation module for Poverty Point aggregation model.

This module implements the main simulation loop with:
- Seasonal cycles (dispersal vs aggregation seasons)
- Band decision-making about aggregation
- Monument investment during aggregation
- Cooperation benefits and information exchange
"""

import numpy as np
from dataclasses import dataclass, field
from typing import List, Tuple
from enum import Enum


class Season(Enum):
    """Seasonal phase of the annual cycle."""
    DISPERSAL = "dispersal"  # Bands forage independently
    AGGREGATION = "aggregation"  # Bands gather at central site


class BandStrategy(Enum):
    """Band-level strategy for aggregation participation."""
    COMMITTED = "committed"  # Always aggregates, invests heavily
    OPPORTUNISTIC = "opportunistic"  # Aggregates when conditions favorable
    INDEPENDENT = "independent"  # Rarely aggregates, minimal investment


@dataclass
class ResourcePatch:
    """A foraging patch with variable productivity."""
    patch_id: int
    location: Tuple[float, float]  # x, y coordinates
    base_productivity: float  # Average productivity (0-1)
    variability: float  # Standard deviation of productivity
    current_productivity: float = 0.0

    def update_productivity(self, rng: np.random.Generator) -> float:
        """Update productivity with seasonal and stochastic variation."""
        # Log-normal distribution to ensure positive values
        self.current_productivity = max(0.0, min(1.0,
            rng.normal(self.base_productivity, self.variability)
        ))
        return self.current_productivity


@dataclass
class Band:
    """A mobile hunter-gatherer band."""
    band_id: int
    size: int  # Number of individuals
    home_patch: int  # ID of home foraging patch
    strategy: BandStrategy

    # State variables
    food_stores: float = 0.0
    accumulated_prestige: float = 0.0
    monument_contributions: float = 0.0
    exotic_goods: float = 0.0
    social_obligations: List[int] = field(default_factory=list)  # Band IDs

    # History
    aggregation_history: List[bool] = field(default_factory=list)

    def decide_aggregation(
        self,
        expected_benefit: float,
        travel_cost: float,
        food_stores: float,
        rng: np.random.Generator
    ) -> bool:
        """
        Decide whether to aggregate this season.

        Args:
            expected_benefit: Expected returns from aggregation
            travel_cost: Cost of traveling to aggregation site
            food_stores: Current food reserves
            rng: Random number generator

        Returns:
            Boolean decision to aggregate
        """
        if self.strategy == BandStrategy.COMMITTED:
            # Always aggregate unless starving
            return food_stores > 0.2

        elif self.strategy == BandStrategy.INDEPENDENT:
            # Only aggregate if exceptional benefits
            threshold = 0.8
            return expected_benefit - travel_cost > threshold

        else:  # OPPORTUNISTIC
            # Cost-benefit calculation with some randomness
            net_benefit = expected_benefit - travel_cost
            # Probabilistic decision based on net benefit
            prob = 1 / (1 + np.exp(-5 * net_benefit))  # Sigmoid
            return rng.random() < prob


@dataclass
class AggregationSite:
    """A location where bands aggregate."""
    site_id: int
    name: str
    location: Tuple[float, float]

    # Accumulated infrastructure
    monument_investment: float = 0.0
    construction_history: List[float] = field(default_factory=list)

    # Current aggregation
    attending_bands: List[int] = field(default_factory=list)
    current_population: int = 0

    def calculate_cooperation_benefits(self) -> float:
        """
        Calculate benefits from cooperation during aggregation.

        Benefits scale with:
        - Number of attending bands (network effects)
        - Accumulated monument investment (infrastructure)
        - Diminishing returns at very large sizes
        """
        n_bands = len(self.attending_bands)

        if n_bands < 2:
            return 0.0

        # Network benefits: more bands = more cooperation opportunities
        network_benefit = np.log(n_bands) * 0.3

        # Infrastructure benefits: monuments facilitate collective action
        infrastructure_benefit = np.sqrt(self.monument_investment) * 0.01

        # Diminishing returns at large sizes (crowding costs)
        crowding_penalty = 0.0
        if n_bands > 20:
            crowding_penalty = (n_bands - 20) * 0.02

        return max(0.0, network_benefit + infrastructure_benefit - crowding_penalty)


@dataclass
class SimulationConfig:
    """Configuration parameters for simulation."""
    # Temporal
    start_year: int = -1700  # BCE (negative)
    end_year: int = -1100  # BCE (negative)

    # Population
    n_bands: int = 50
    initial_band_size: int = 25

    # Spatial
    n_patches: int = 30
    region_size: float = 500.0  # km

    # Environmental
    base_productivity: float = 0.6
    productivity_variability: float = 0.15

    # Aggregation
    aggregation_season_length: float = 0.25  # Fraction of year
    travel_cost_per_km: float = 0.001

    # Signaling
    monument_cost_rate: float = 0.15  # Fraction of productivity
    exotic_acquisition_cost: float = 0.10

    # Reproduction
    birth_rate: float = 0.03
    death_rate: float = 0.02
    starvation_death_rate: float = 0.15

    # Random seed
    seed: int = 42


@dataclass
class SimulationState:
    """State of the simulation at a given time step."""
    year: int
    season: Season

    # Populations
    total_population: int = 0
    n_bands: int = 0

    # Aggregation
    bands_aggregating: int = 0
    aggregation_population: int = 0

    # Investment
    total_monument_investment: float = 0.0
    annual_construction: float = 0.0
    total_exotic_goods: float = 0.0

    # Environment
    mean_productivity: float = 0.0

    # Cooperation
    total_cooperation_benefit: float = 0.0


class PovertyPointSimulation:
    """
    Main simulation class for Poverty Point aggregation model.

    The simulation models seasonal aggregation of hunter-gatherer bands
    at a central site, where they invest in monumental construction and
    exchange exotic goods as costly signals facilitating cooperation.
    """

    def __init__(self, config: SimulationConfig):
        """Initialize simulation with given configuration."""
        self.config = config
        self.rng = np.random.default_rng(config.seed)

        # Initialize components
        self.patches = self._initialize_patches()
        self.bands = self._initialize_bands()
        self.aggregation_site = self._initialize_aggregation_site()

        # Track state
        self.year = config.start_year
        self.season = Season.DISPERSAL
        self.history: List[SimulationState] = []

    def _initialize_patches(self) -> List[ResourcePatch]:
        """Create resource patches distributed across the region."""
        patches = []
        for i in range(self.config.n_patches):
            x = self.rng.uniform(0, self.config.region_size)
            y = self.rng.uniform(0, self.config.region_size)

            # Vary base productivity spatially
            base_prod = self.config.base_productivity + self.rng.normal(0, 0.1)
            base_prod = max(0.2, min(0.9, base_prod))

            patches.append(ResourcePatch(
                patch_id=i,
                location=(x, y),
                base_productivity=base_prod,
                variability=self.config.productivity_variability
            ))
        return patches

    def _initialize_bands(self) -> List[Band]:
        """Create initial population of bands."""
        bands = []

        # Strategy distribution
        strategy_probs = [0.3, 0.5, 0.2]  # Committed, Opportunistic, Independent
        strategies = [BandStrategy.COMMITTED, BandStrategy.OPPORTUNISTIC,
                     BandStrategy.INDEPENDENT]

        for i in range(self.config.n_bands):
            strategy_idx = self.rng.choice(len(strategies), p=strategy_probs)
            strategy = strategies[strategy_idx]
            home_patch = self.rng.integers(0, len(self.patches))

            bands.append(Band(
                band_id=i,
                size=self.config.initial_band_size,
                home_patch=home_patch,
                strategy=strategy,
                food_stores=0.5  # Start with moderate stores
            ))
        return bands

    def _initialize_aggregation_site(self) -> AggregationSite:
        """Create the main aggregation site (Poverty Point)."""
        # Place at central location
        center = self.config.region_size / 2
        return AggregationSite(
            site_id=0,
            name="Poverty Point",
            location=(center, center)
        )

    def _calculate_travel_cost(self, band: Band) -> float:
        """Calculate cost for band to travel to aggregation site."""
        patch = self.patches[band.home_patch]
        dx = patch.location[0] - self.aggregation_site.location[0]
        dy = patch.location[1] - self.aggregation_site.location[1]
        distance = np.sqrt(dx**2 + dy**2)
        return distance * self.config.travel_cost_per_km

    def _run_dispersal_season(self) -> None:
        """Execute dispersal season: bands forage independently."""
        # Update patch productivities
        for patch in self.patches:
            patch.update_productivity(self.rng)

        # Each band forages
        for band in self.bands:
            patch = self.patches[band.home_patch]

            # Foraging success depends on patch productivity and band size
            foraging_efficiency = 0.8 + self.rng.normal(0, 0.1)
            harvest = patch.current_productivity * foraging_efficiency * band.size * 0.1

            # Update food stores
            consumption = band.size * 0.05  # Per capita consumption
            band.food_stores += harvest - consumption
            band.food_stores = max(0.0, band.food_stores)

            # Population dynamics
            if band.food_stores < 0.1:
                # Starvation
                deaths = int(band.size * self.config.starvation_death_rate)
                band.size = max(1, band.size - deaths)
            else:
                # Normal dynamics
                births = int(band.size * self.config.birth_rate)
                deaths = int(band.size * self.config.death_rate)
                band.size = max(1, band.size + births - deaths)

    def _run_aggregation_season(self) -> None:
        """Execute aggregation season: bands gather and cooperate."""
        # Clear previous aggregation
        self.aggregation_site.attending_bands = []
        self.aggregation_site.current_population = 0

        # Calculate expected benefits
        expected_benefit = self.aggregation_site.calculate_cooperation_benefits()
        # Add bonus based on accumulated infrastructure
        expected_benefit += np.sqrt(self.aggregation_site.monument_investment) * 0.005

        # Each band decides whether to aggregate
        for band in self.bands:
            travel_cost = self._calculate_travel_cost(band)

            if band.decide_aggregation(expected_benefit, travel_cost,
                                       band.food_stores, self.rng):
                self.aggregation_site.attending_bands.append(band.band_id)
                self.aggregation_site.current_population += band.size
                band.aggregation_history.append(True)

                # Pay travel cost
                band.food_stores -= travel_cost
            else:
                band.aggregation_history.append(False)

        # Cooperation benefits for attending bands
        if len(self.aggregation_site.attending_bands) > 1:
            coop_benefit = self.aggregation_site.calculate_cooperation_benefits()

            for band_id in self.aggregation_site.attending_bands:
                band = self.bands[band_id]

                # Receive cooperation benefits
                band.food_stores += coop_benefit * 0.5

                # Monument investment (costly signal)
                if band.food_stores > 0.3:
                    investment = band.size * self.config.monument_cost_rate
                    band.monument_contributions += investment
                    self.aggregation_site.monument_investment += investment
                    band.food_stores -= investment * 0.1  # Cost in food

                # Exotic goods acquisition
                if band.food_stores > 0.4 and self.rng.random() < 0.3:
                    exotic_cost = self.config.exotic_acquisition_cost
                    band.exotic_goods += 1
                    band.food_stores -= exotic_cost
                    band.accumulated_prestige += 0.1

                # Social obligations (create reciprocal ties)
                if self.rng.random() < 0.2:
                    other_bands = [b for b in self.aggregation_site.attending_bands
                                  if b != band_id]
                    if other_bands:
                        partner = self.rng.choice(other_bands)
                        if partner not in band.social_obligations:
                            band.social_obligations.append(partner)

        # Record construction for this season
        self.aggregation_site.construction_history.append(
            self.aggregation_site.monument_investment
        )

    def step(self) -> SimulationState:
        """Execute one time step (half year)."""
        if self.season == Season.DISPERSAL:
            self._run_dispersal_season()
            self.season = Season.AGGREGATION
        else:
            self._run_aggregation_season()
            self.season = Season.DISPERSAL
            self.year += 1

        # Record state
        state = self._get_current_state()
        self.history.append(state)
        return state

    def _get_current_state(self) -> SimulationState:
        """Capture current simulation state."""
        total_pop = sum(b.size for b in self.bands)
        mean_prod = float(np.mean([p.current_productivity for p in self.patches]))

        return SimulationState(
            year=self.year,
            season=self.season,
            total_population=total_pop,
            n_bands=len([b for b in self.bands if b.size > 0]),
            bands_aggregating=len(self.aggregation_site.attending_bands),
            aggregation_population=self.aggregation_site.current_population,
            total_monument_investment=self.aggregation_site.monument_investment,
            annual_construction=(
                self.aggregation_site.construction_history[-1] -
                self.aggregation_site.construction_history[-2]
                if len(self.aggregation_site.construction_history) > 1
                else self.aggregation_site.monument_investment
            ),
            total_exotic_goods=sum(b.exotic_goods for b in self.bands),
            mean_productivity=float(mean_prod),
            total_cooperation_benefit=self.aggregation_site.calculate_cooperation_benefits()
        )

    def run(self, verbose: bool = True) -> List[SimulationState]:
        """
        Run simulation from start to end year.

        Args:
            verbose: Print progress updates

        Returns:
            List of SimulationState objects for each time step
        """
        if verbose:
            print(f"Running simulation: {self.config.start_year} to {self.config.end_year} BCE")

        steps = 0
        while self.year < self.config.end_year:
            self.step()
            steps += 1

            if verbose and steps % 100 == 0:
                state = self.history[-1]
                print(f"  Year {-state.year} BCE: Pop={state.total_population}, "
                      f"Monuments={state.total_monument_investment:.0f}")

        if verbose:
            print(f"Simulation complete: {len(self.history)} time steps")

        return self.history


def run_simple_test():
    """Run a simple test of the simulation."""
    config = SimulationConfig(
        start_year=-1700,
        end_year=-1600,  # Short run for testing
        n_bands=30,
        seed=42
    )

    sim = PovertyPointSimulation(config)
    history = sim.run(verbose=True)

    # Print summary
    final = history[-1]
    print(f"\nFinal state ({-final.year} BCE):")
    print(f"  Population: {final.total_population}")
    print(f"  Bands: {final.n_bands}")
    print(f"  Monument investment: {final.total_monument_investment:.1f}")
    print(f"  Exotic goods: {final.total_exotic_goods:.0f}")

    return history


if __name__ == "__main__":
    run_simple_test()
