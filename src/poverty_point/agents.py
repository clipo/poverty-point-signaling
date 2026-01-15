"""
Agent definitions for the Poverty Point ABM.

Agents:
- Band: Mobile hunter-gatherer group
- AggregationSite: Location where bands gather
"""

from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional
from enum import Enum
import numpy as np

from .parameters import (
    SimulationParameters, cooperation_benefit,
    W_aggregator, W_independent
)


class Strategy(Enum):
    """Band strategy for aggregation."""
    AGGREGATOR = "aggregator"      # Participates in aggregation
    INDEPENDENT = "independent"    # Remains dispersed


@dataclass
class Band:
    """
    A mobile hunter-gatherer band.

    Bands are the primary decision-making units. They choose whether
    to aggregate at the central site or remain independent, and their
    fitness depends on this choice and environmental conditions.
    """
    band_id: int
    size: int                               # Number of individuals
    home_location: Tuple[float, float]      # Base foraging location
    strategy: Strategy                       # Current strategy

    # Resource state
    resources: float = 0.5                  # Current resource holdings [0, 1]

    # Signaling state
    prestige: float = 0.0                   # Accumulated prestige
    monument_contributions: float = 0.0     # Total monument investment
    exotic_goods: int = 0                   # Exotic items held

    # Social network (band_id -> obligation strength)
    obligations: Dict[int, float] = field(default_factory=dict)

    # History tracking
    aggregation_history: List[bool] = field(default_factory=list)
    fitness_history: List[float] = field(default_factory=list)
    strategy_history: List[Strategy] = field(default_factory=list)

    def decide_strategy(self,
                        expected_n: float,
                        sigma: float,
                        epsilon: float,
                        params: SimulationParameters,
                        rng: np.random.Generator) -> Strategy:
        """
        Decide whether to aggregate based on expected fitness.

        Uses soft-max decision rule with memory effects.

        Args:
            expected_n: Expected number of bands at aggregation
            sigma: Environmental uncertainty
            epsilon: Ecotone advantage at aggregation site
            params: Simulation parameters
            rng: Random number generator

        Returns:
            Chosen strategy
        """
        # Calculate expected fitness for each strategy
        E_W_agg = W_aggregator(sigma, epsilon, expected_n, params)
        E_W_ind = W_independent(sigma, params)

        # Base fitness difference
        fitness_diff = E_W_agg - E_W_ind

        # Memory effect: recent experience influences decision
        if len(self.fitness_history) >= 5:
            recent_fitness = np.mean(self.fitness_history[-5:])
            long_term_fitness = np.mean(self.fitness_history)

            if self.aggregation_history[-1]:
                # Was aggregator last year
                if recent_fitness > long_term_fitness:
                    fitness_diff += 0.05  # Positive reinforcement
                else:
                    fitness_diff -= 0.05  # Negative reinforcement
            else:
                # Was independent last year
                if recent_fitness > long_term_fitness:
                    fitness_diff -= 0.05  # Stay independent
                else:
                    fitness_diff += 0.05  # Try aggregating

        # Probabilistic choice (sigmoid with temperature)
        temperature = 10.0  # Higher = more deterministic
        p_aggregate = 1.0 / (1.0 + np.exp(-temperature * fitness_diff))

        if rng.random() < p_aggregate:
            return Strategy.AGGREGATOR
        else:
            return Strategy.INDEPENDENT

    def calculate_travel_cost(self,
                              destination: Tuple[float, float],
                              cost_per_km: float = 0.0005) -> float:
        """
        Calculate travel cost to a destination.

        Args:
            destination: (x, y) coordinates
            cost_per_km: Resource cost per km traveled

        Returns:
            Travel cost as fraction of resources
        """
        dx = destination[0] - self.home_location[0]
        dy = destination[1] - self.home_location[1]
        distance = np.sqrt(dx**2 + dy**2)
        return distance * cost_per_km

    def invest_in_monument(self,
                           investment_rate: float,
                           rng: np.random.Generator) -> float:
        """
        Invest resources in monument construction.

        Args:
            investment_rate: Fraction of resources to invest
            rng: Random number generator

        Returns:
            Amount invested
        """
        # Can only invest if have sufficient resources
        if self.resources < 0.3:
            return 0.0

        # Investment proportional to band size and resources
        base_investment = self.size * investment_rate * self.resources

        # Some variation in investment
        investment = base_investment * (0.8 + 0.4 * rng.random())

        # Update state
        self.monument_contributions += investment
        self.prestige += investment * 0.1  # Prestige from contribution

        return investment

    def acquire_exotic(self,
                       acquisition_cost: float,
                       rng: np.random.Generator) -> bool:
        """
        Attempt to acquire an exotic good.

        Args:
            acquisition_cost: Resource cost of acquisition
            rng: Random number generator

        Returns:
            True if acquired, False otherwise
        """
        # Must have sufficient resources
        if self.resources < acquisition_cost + 0.2:
            return False

        # Probability of acquisition depends on resources and prestige
        p_acquire = 0.3 * (1 + self.prestige / (1 + self.prestige))

        if rng.random() < p_acquire:
            self.exotic_goods += 1
            self.resources -= acquisition_cost
            self.prestige += 0.15  # Exotics boost prestige
            return True

        return False

    def form_obligation(self,
                        partner_id: int,
                        strength: float = 0.1) -> None:
        """
        Form or strengthen reciprocal obligation with another band.

        Args:
            partner_id: ID of partner band
            strength: Initial/additional obligation strength
        """
        if partner_id in self.obligations:
            self.obligations[partner_id] += strength
        else:
            self.obligations[partner_id] = strength

        # Cap obligation strength
        self.obligations[partner_id] = min(1.0, self.obligations[partner_id])

    def call_obligation(self,
                        partner_id: int,
                        need: float) -> float:
        """
        Call on an obligation for help during shortfall.

        Args:
            partner_id: ID of partner band
            need: Amount of help requested

        Returns:
            Amount of help received
        """
        if partner_id not in self.obligations:
            return 0.0

        # Help proportional to obligation strength
        help_received = min(need, self.obligations[partner_id] * 0.5)

        # Calling reduces obligation
        self.obligations[partner_id] *= 0.7

        # Remove if too weak
        if self.obligations[partner_id] < 0.05:
            del self.obligations[partner_id]

        return help_received

    def reproduce(self,
                  fitness: float,
                  birth_rate: float,
                  death_rate: float,
                  rng: np.random.Generator) -> None:
        """
        Update population based on fitness.

        Args:
            fitness: Realized fitness this year
            birth_rate: Base birth rate
            death_rate: Base death rate
            rng: Random number generator
        """
        # Births scale with fitness and resources
        effective_birth_rate = birth_rate * fitness * (0.5 + self.resources)
        births = rng.binomial(self.size, effective_birth_rate)

        # Deaths (baseline)
        deaths = rng.binomial(self.size, death_rate)

        # Update size
        self.size = max(1, self.size + births - deaths)

    def suffer_shortfall(self,
                         vulnerability: float,
                         sigma: float,
                         rng: np.random.Generator) -> int:
        """
        Suffer mortality during environmental shortfall.

        Args:
            vulnerability: Strategy-specific vulnerability (α or β)
            sigma: Environmental uncertainty
            rng: Random number generator

        Returns:
            Number of deaths
        """
        # Mortality rate = vulnerability × σ
        mortality_rate = vulnerability * sigma

        # Random deaths
        deaths = rng.binomial(self.size, mortality_rate)

        self.size = max(1, self.size - deaths)

        return deaths


@dataclass
class AggregationSite:
    """
    A location where bands aggregate seasonally.

    The primary aggregation site (Poverty Point) is positioned at
    maximum ecotone advantage. Secondary sites may exist with lower ε.
    """
    site_id: int
    name: str
    location: Tuple[float, float]
    ecotone_advantage: float          # ε for this location

    # Infrastructure
    monument_level: float = 0.0       # Cumulative investment
    monument_history: List[float] = field(default_factory=list)

    # Current aggregation state
    attending_bands: List[int] = field(default_factory=list)
    current_population: int = 0

    # Exotic goods
    total_exotics: int = 0
    exotic_sources: Dict[str, int] = field(default_factory=dict)

    def calculate_cooperation_benefits(self,
                                       params: SimulationParameters) -> float:
        """
        Calculate cooperation benefits for current aggregation size.

        Args:
            params: Simulation parameters

        Returns:
            Cooperation benefit multiplier
        """
        n = len(self.attending_bands)
        return cooperation_benefit(n, params.cooperation)

    def add_attending_band(self, band: Band) -> None:
        """
        Record a band attending this aggregation.

        Args:
            band: Attending band
        """
        if band.band_id not in self.attending_bands:
            self.attending_bands.append(band.band_id)
            self.current_population += band.size
            self.total_exotics += band.exotic_goods

    def record_construction(self, investment: float) -> None:
        """
        Record monument construction for this year.

        Args:
            investment: Total investment this year
        """
        self.monument_level += investment
        self.monument_history.append(self.monument_level)

    def reset_annual_state(self) -> None:
        """Reset attendance for new year."""
        self.attending_bands = []
        self.current_population = 0

    @property
    def n_attending(self) -> int:
        """Number of bands currently attending."""
        return len(self.attending_bands)


def create_bands(n_bands: int,
                 initial_size: int,
                 region_size: float,
                 rng: np.random.Generator) -> List[Band]:
    """
    Create initial population of bands.

    Bands are distributed across the region with random initial strategies.

    Args:
        n_bands: Number of bands to create
        initial_size: Initial size per band
        region_size: Region diameter (km)
        rng: Random number generator

    Returns:
        List of Band objects
    """
    bands = []

    # Initial strategy distribution (slight bias toward independent)
    strategy_probs = [0.4, 0.6]  # [AGGREGATOR, INDEPENDENT]

    for i in range(n_bands):
        # Random location
        x = rng.uniform(0, region_size)
        y = rng.uniform(0, region_size)

        # Random initial strategy
        strategy = (Strategy.AGGREGATOR if rng.random() < strategy_probs[0]
                    else Strategy.INDEPENDENT)

        band = Band(
            band_id=i,
            size=initial_size + rng.integers(-5, 6),  # Some variation
            home_location=(x, y),
            strategy=strategy,
            resources=0.4 + 0.2 * rng.random()  # Initial resources
        )

        bands.append(band)

    return bands


def create_aggregation_site(location: Tuple[float, float],
                            epsilon: float,
                            name: str = "Poverty Point") -> AggregationSite:
    """
    Create the main aggregation site.

    Args:
        location: (x, y) coordinates
        epsilon: Ecotone advantage at this location
        name: Site name

    Returns:
        AggregationSite object
    """
    return AggregationSite(
        site_id=0,
        name=name,
        location=location,
        ecotone_advantage=epsilon
    )
