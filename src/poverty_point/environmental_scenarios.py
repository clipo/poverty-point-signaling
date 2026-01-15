"""
Environmental Scenarios for Poverty Point ABM.

Defines realistic environmental scenarios based on archaeological and
paleoclimatic data. These scenarios create different levels of σ (uncertainty)
through variation in shortfall frequency and magnitude.

Based on calibration data from:
- Rapa Nui: High σ environment (frequent/severe shortfalls)
- Rapa Iti: Low σ environment (rare/mild shortfalls)
- Poverty Point: Moderate σ with ecotone buffering
"""

from dataclasses import dataclass
from typing import Tuple, Optional
import numpy as np

from .environment import EnvironmentConfig


@dataclass
class ShortfallParams:
    """
    Parameters controlling environmental shortfalls.

    These directly influence effective σ in the simulation.
    """
    # Frequency: mean years between shortfall events
    mean_interval: float = 10.0

    # Magnitude: depth of productivity reduction (0-1)
    magnitude_mean: float = 0.5
    magnitude_std: float = 0.15

    # Duration: how long shortfalls persist
    # duration = max(1, int(1 + magnitude * duration_scale))
    duration_scale: float = 2.5


@dataclass
class EnvironmentalScenario:
    """
    Complete environmental scenario definition.

    Combines environment configuration with shortfall parameters to create
    different levels of environmental uncertainty (σ).
    """
    name: str
    description: str

    # Environment configuration
    env_config: EnvironmentConfig

    # Shortfall parameters
    shortfall_params: ShortfallParams

    # Expected σ range (for validation)
    expected_sigma_range: Tuple[float, float]

    # Ecotone advantage (ε) at optimal aggregation location
    expected_epsilon: float


def create_high_sigma_scenario(
    name: str = "High Uncertainty",
    description: str = "Frequent, severe shortfalls like Rapa Nui"
) -> EnvironmentalScenario:
    """
    Create a high-σ scenario similar to Rapa Nui conditions.

    - Shortfalls every ~6 years
    - Severe magnitude (60% reduction)
    - Long duration (2-3 years)
    - Higher inter-annual variability
    """
    env_config = EnvironmentConfig(
        region_size=500.0,
        n_aquatic_patches=8,
        n_terrestrial_patches=10,
        n_mast_patches=6,
        n_ecotone_patches=4,
        # Higher variability
        aquatic_variability=0.25,
        terrestrial_variability=0.20,
        mast_variability=0.45,
        ecotone_variability=0.18,
        # Lower base productivity (stressed environment)
        aquatic_base_productivity=0.60,
        terrestrial_base_productivity=0.50,
        mast_base_productivity=0.40,
        ecotone_base_productivity=0.55,
    )

    shortfall_params = ShortfallParams(
        mean_interval=6.0,      # Every 6 years
        magnitude_mean=0.60,    # 60% productivity loss
        magnitude_std=0.15,
        duration_scale=2.5,     # 2-3 year duration
    )

    return EnvironmentalScenario(
        name=name,
        description=description,
        env_config=env_config,
        shortfall_params=shortfall_params,
        expected_sigma_range=(0.5, 0.8),
        expected_epsilon=0.35,
    )


def create_low_sigma_scenario(
    name: str = "Low Uncertainty",
    description: str = "Rare, mild shortfalls like Rapa Iti"
) -> EnvironmentalScenario:
    """
    Create a low-σ scenario similar to Rapa Iti conditions.

    - Shortfalls every ~18 years
    - Mild magnitude (30% reduction)
    - Short duration (1 year)
    - Lower inter-annual variability
    """
    env_config = EnvironmentConfig(
        region_size=500.0,
        n_aquatic_patches=12,
        n_terrestrial_patches=14,
        n_mast_patches=10,
        n_ecotone_patches=6,
        # Lower variability (stable environment)
        aquatic_variability=0.10,
        terrestrial_variability=0.08,
        mast_variability=0.20,
        ecotone_variability=0.08,
        # Higher base productivity (productive environment)
        aquatic_base_productivity=0.75,
        terrestrial_base_productivity=0.70,
        mast_base_productivity=0.60,
        ecotone_base_productivity=0.70,
    )

    shortfall_params = ShortfallParams(
        mean_interval=18.0,     # Every 18 years
        magnitude_mean=0.30,    # 30% productivity loss
        magnitude_std=0.10,
        duration_scale=1.0,     # 1 year duration
    )

    return EnvironmentalScenario(
        name=name,
        description=description,
        env_config=env_config,
        shortfall_params=shortfall_params,
        expected_sigma_range=(0.15, 0.35),
        expected_epsilon=0.35,
    )


def create_poverty_point_scenario(
    name: str = "Poverty Point",
    description: str = "Moderate uncertainty with strong ecotone buffering"
) -> EnvironmentalScenario:
    """
    Create scenario calibrated to Poverty Point conditions.

    Based on:
    - Multi-zone ecotone at Macon Ridge
    - Variable but buffered environment
    - ~500 year occupation with sustained monument building
    """
    env_config = EnvironmentConfig(
        region_size=500.0,
        n_aquatic_patches=10,   # Bayou Macon, floodplain
        n_terrestrial_patches=12,  # Upland forests
        n_mast_patches=8,       # Hardwood stands
        n_ecotone_patches=5,    # Macon Ridge ecotone
        # Moderate variability
        aquatic_variability=0.15,
        terrestrial_variability=0.12,
        mast_variability=0.30,
        ecotone_variability=0.10,  # Ecotone is most stable
        # Moderate-high productivity (rich environment)
        aquatic_base_productivity=0.70,
        terrestrial_base_productivity=0.60,
        mast_base_productivity=0.50,
        ecotone_base_productivity=0.65,
        # Strong negative covariance (buffering)
        aquatic_terrestrial_cov=-0.35,  # Strong buffering
        aquatic_mast_cov=0.05,
        terrestrial_mast_cov=0.15,
    )

    shortfall_params = ShortfallParams(
        mean_interval=10.0,     # Moderate frequency
        magnitude_mean=0.45,    # Moderate severity
        magnitude_std=0.15,
        duration_scale=2.0,
    )

    return EnvironmentalScenario(
        name=name,
        description=description,
        env_config=env_config,
        shortfall_params=shortfall_params,
        expected_sigma_range=(0.35, 0.55),
        expected_epsilon=0.40,  # Higher ecotone advantage
    )


def create_critical_threshold_scenario(
    target_sigma: float = 0.53,
    name: str = "Critical Threshold",
    description: str = "Calibrated to σ* theoretical prediction"
) -> EnvironmentalScenario:
    """
    Create scenario calibrated to produce σ ≈ σ* (critical threshold).

    This creates conditions where aggregation becomes marginally adaptive,
    useful for testing phase transitions.

    Args:
        target_sigma: Target effective σ value
        name: Scenario name
        description: Scenario description
    """
    # Back-calculate shortfall parameters to achieve target σ
    # Higher target σ -> more frequent, severe shortfalls

    if target_sigma < 0.3:
        interval = 20.0
        magnitude = 0.25
    elif target_sigma < 0.5:
        interval = 12.0
        magnitude = 0.40
    elif target_sigma < 0.7:
        interval = 8.0
        magnitude = 0.55
    else:
        interval = 5.0
        magnitude = 0.70

    # Variability scales with target σ
    variability_scale = 0.5 + target_sigma

    env_config = EnvironmentConfig(
        region_size=500.0,
        n_aquatic_patches=10,
        n_terrestrial_patches=12,
        n_mast_patches=8,
        n_ecotone_patches=5,
        aquatic_variability=0.15 * variability_scale,
        terrestrial_variability=0.10 * variability_scale,
        mast_variability=0.30 * variability_scale,
        ecotone_variability=0.12 * variability_scale,
    )

    shortfall_params = ShortfallParams(
        mean_interval=interval,
        magnitude_mean=magnitude,
        magnitude_std=0.12,
        duration_scale=2.0,
    )

    return EnvironmentalScenario(
        name=name,
        description=description,
        env_config=env_config,
        shortfall_params=shortfall_params,
        expected_sigma_range=(target_sigma - 0.1, target_sigma + 0.1),
        expected_epsilon=0.35,
    )


# Pre-defined scenarios dictionary
SCENARIOS = {
    "high": create_high_sigma_scenario(),
    "low": create_low_sigma_scenario(),
    "poverty_point": create_poverty_point_scenario(),
    "critical": create_critical_threshold_scenario(target_sigma=0.53),
}


def get_scenario(name: str) -> EnvironmentalScenario:
    """Get a pre-defined scenario by name."""
    if name not in SCENARIOS:
        available = ", ".join(SCENARIOS.keys())
        raise ValueError(f"Unknown scenario '{name}'. Available: {available}")
    return SCENARIOS[name]


def list_scenarios() -> None:
    """Print available scenarios."""
    print("Available Environmental Scenarios:")
    print("=" * 50)
    for name, scenario in SCENARIOS.items():
        print(f"\n{name}:")
        print(f"  {scenario.description}")
        print(f"  Expected σ: {scenario.expected_sigma_range[0]:.2f} - "
              f"{scenario.expected_sigma_range[1]:.2f}")
        print(f"  Expected ε: {scenario.expected_epsilon:.2f}")
        print(f"  Shortfall interval: {scenario.shortfall_params.mean_interval:.0f} years")
        print(f"  Shortfall magnitude: {scenario.shortfall_params.magnitude_mean:.0%}")


if __name__ == "__main__":
    list_scenarios()
