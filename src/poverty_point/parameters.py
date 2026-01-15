"""
Parameter definitions for the Poverty Point ABM.

All parameters derive from the theoretical derivation in:
docs/THEORETICAL_DERIVATION.md

These values produce a critical threshold σ* ≈ 0.53 at ε=0.35, n=25.
"""

from dataclasses import dataclass, field
from typing import Dict
import numpy as np


@dataclass
class CostParameters:
    """Cost parameters for aggregation strategy."""

    # Travel cost (fraction of resources spent traveling to aggregation)
    C_travel: float = 0.12

    # Signaling cost (fraction of resources invested in monuments/exotics)
    C_signal: float = 0.18

    # Opportunity cost (foregone foraging during aggregation season)
    C_opportunity: float = 0.12

    @property
    def C_total(self) -> float:
        """Total cost of aggregation strategy."""
        return self.C_travel + self.C_signal + self.C_opportunity


@dataclass
class VulnerabilityParameters:
    """Vulnerability parameters determining shortfall mortality."""

    # Aggregator vulnerability (buffered by ecotone + risk pooling)
    alpha_agg: float = 0.40

    # Independent vulnerability (exposed, single-zone)
    beta_ind: float = 0.75


@dataclass
class CooperationParameters:
    """Parameters for cooperation benefits from aggregation."""

    # Cooperation benefit coefficient (log-scale returns to aggregation)
    b_coop: float = 0.08

    # Optimal aggregation size before crowding costs
    n_optimal: int = 25

    # Crowding cost coefficient
    c_crowd: float = 0.015

    # Reciprocal obligation benefit rate
    B_recip: float = 0.05

    # Independent strategy reproductive advantage
    R_ind: float = 1.10


@dataclass
class EnvironmentParameters:
    """Environmental parameters."""

    # Region size (km)
    region_size: float = 500.0

    # Zone accessibility radius (km)
    access_radius: float = 50.0

    # Number of patches per zone
    n_aquatic_patches: int = 10
    n_terrestrial_patches: int = 12
    n_mast_patches: int = 8
    n_wetland_patches: int = 5

    # Base productivity by zone (relative units)
    base_productivity: Dict[str, float] = field(default_factory=lambda: {
        'aquatic': 0.70,
        'terrestrial': 0.60,
        'mast': 0.50,
        'wetland': 0.65
    })

    # Inter-annual variability by zone
    variability: Dict[str, float] = field(default_factory=lambda: {
        'aquatic': 0.15,
        'terrestrial': 0.10,
        'mast': 0.30,  # Mast highly variable
        'wetland': 0.12
    })

    # Zone covariance (negative = buffering effect)
    # Format: (zone1, zone2) -> covariance
    zone_covariance: Dict[tuple, float] = field(default_factory=lambda: {
        ('aquatic', 'terrestrial'): -0.3,   # Good buffering
        ('aquatic', 'mast'): 0.1,           # Slight positive
        ('terrestrial', 'mast'): 0.2,       # Moderate positive
        ('aquatic', 'wetland'): 0.3,        # Both water-dependent
        ('terrestrial', 'wetland'): -0.2,   # Some buffering
        ('mast', 'wetland'): 0.0            # Independent
    })


@dataclass
class PopulationParameters:
    """Population dynamics parameters."""

    # Initial number of bands
    n_bands: int = 50

    # Initial band size (individuals)
    initial_band_size: int = 25

    # Demographic rates
    birth_rate: float = 0.03      # Per capita annual
    death_rate: float = 0.02      # Per capita annual (non-shortfall)

    # Band size constraints
    min_band_size: int = 5        # Below this, band dissolves
    max_band_size: int = 50       # Above this, band fissions


@dataclass
class SimulationParameters:
    """Complete parameter set for simulation."""

    # Component parameters
    costs: CostParameters = field(default_factory=CostParameters)
    vulnerability: VulnerabilityParameters = field(default_factory=VulnerabilityParameters)
    cooperation: CooperationParameters = field(default_factory=CooperationParameters)
    environment: EnvironmentParameters = field(default_factory=EnvironmentParameters)
    population: PopulationParameters = field(default_factory=PopulationParameters)

    # Simulation control
    duration: int = 600           # Years (1700-1100 BCE)
    burn_in: int = 100            # Years before recording
    seed: int = 42                # Random seed

    # Phase space parameters (set per run)
    sigma: float = 0.5            # Environmental uncertainty
    epsilon: float = 0.35         # Ecotone advantage at aggregation site


def cooperation_benefit(n: float, params: CooperationParameters) -> float:
    """
    Calculate cooperation benefits as function of aggregation size.

    f(n) = 1 + b * ln(n) - crowding penalty

    Args:
        n: Number of bands aggregating
        params: Cooperation parameters

    Returns:
        Cooperation benefit multiplier (>= 1.0)
    """
    if n <= 1:
        return 1.0

    # Increasing returns from cooperation (logarithmic)
    benefit = 1.0 + params.b_coop * np.log(n)

    # Crowding costs above optimal size
    if n > params.n_optimal:
        crowding = params.c_crowd * (n - params.n_optimal) ** 2
        benefit -= crowding

    return max(1.0, benefit)


def W_aggregator(sigma: float, epsilon: float, n: float,
                 params: SimulationParameters) -> float:
    """
    Calculate fitness for aggregator strategy.

    W_agg = (1 - C_total) * (1 - α * σ_eff) * f(n) * (1 + B_recip)

    Args:
        sigma: Environmental uncertainty
        epsilon: Ecotone advantage
        n: Number of bands aggregating
        params: Full parameter set

    Returns:
        Fitness value
    """
    # Total costs
    C_total = params.costs.C_total

    # Effective uncertainty (reduced by ecotone)
    sigma_eff = sigma * (1.0 - epsilon)

    # Survival component
    survival = 1.0 - params.vulnerability.alpha_agg * sigma_eff

    # Cooperation benefits
    f_n = cooperation_benefit(n, params.cooperation)

    # Reciprocal benefits
    recip = 1.0 + params.cooperation.B_recip

    # Combined fitness
    W = (1.0 - C_total) * survival * f_n * recip

    return max(0.0, W)


def W_independent(sigma: float, params: SimulationParameters) -> float:
    """
    Calculate fitness for independent strategy.

    W_ind = R_ind * (1 - β * σ)

    Args:
        sigma: Environmental uncertainty
        params: Full parameter set

    Returns:
        Fitness value
    """
    # Reproductive advantage (no aggregation costs)
    R_ind = params.cooperation.R_ind

    # Survival component (higher vulnerability)
    survival = 1.0 - params.vulnerability.beta_ind * sigma

    return max(0.0, R_ind * survival)


def critical_threshold(epsilon: float, n: float,
                       params: SimulationParameters) -> float:
    """
    Calculate critical σ* where aggregation becomes adaptive.

    σ* = (R_ind - A) / (R_ind * β - A * α_eff)

    Where A = (1 - C_total) * f(n) * (1 + B_recip)

    Args:
        epsilon: Ecotone advantage
        n: Expected aggregation size
        params: Full parameter set

    Returns:
        Critical threshold σ*
    """
    C_total = params.costs.C_total
    f_n = cooperation_benefit(n, params.cooperation)
    recip = 1.0 + params.cooperation.B_recip
    R_ind = params.cooperation.R_ind

    # Aggregation factor
    A = (1.0 - C_total) * f_n * recip

    # Effective alpha
    alpha_eff = params.vulnerability.alpha_agg * (1.0 - epsilon)

    # Denominator
    denom = R_ind * params.vulnerability.beta_ind - A * alpha_eff

    if denom <= 0:
        return 0.0  # Aggregation always wins

    # Numerator
    numerator = R_ind - A

    if numerator <= 0:
        return 0.0  # Aggregation always wins

    sigma_star = numerator / denom
    return max(0.0, min(1.0, sigma_star))


# Convenience function to create default parameters
def default_parameters(sigma: float = 0.5, epsilon: float = 0.35,
                       seed: int = 42) -> SimulationParameters:
    """Create parameter set with specified phase space position."""
    params = SimulationParameters(seed=seed)
    params.sigma = sigma
    params.epsilon = epsilon
    return params
