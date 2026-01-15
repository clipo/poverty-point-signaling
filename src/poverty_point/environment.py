"""
Environmental model for Poverty Point simulation.

This module implements:
- Multiple ecologically-distinct resource zones
- Seasonal productivity cycles
- Inter-zone covariance structure (buffering effects)
- Ecotone locations with multi-zone access
"""

import numpy as np
from dataclasses import dataclass
from typing import List, Tuple, Dict, Optional
from enum import Enum


class ResourceZone(Enum):
    """Types of ecological zones around Poverty Point."""
    AQUATIC = "aquatic"  # Fish, waterfowl, turtles - floodplain/bayou
    TERRESTRIAL = "terrestrial"  # Deer, small game - upland forests
    MAST = "mast"  # Nuts (pecans, hickory) - seasonal, variable
    ECOTONE = "ecotone"  # Mixed access - Macon Ridge position


@dataclass
class SeasonalProfile:
    """Seasonal productivity multipliers for a resource zone."""
    spring: float  # Relative productivity (0-2, where 1 = average)
    summer: float
    fall: float
    winter: float

    def get_multiplier(self, month: int) -> float:
        """Get productivity multiplier for given month (1-12)."""
        if month in [3, 4, 5]:
            return self.spring
        elif month in [6, 7, 8]:
            return self.summer
        elif month in [9, 10, 11]:
            return self.fall
        else:
            return self.winter


# Seasonal profiles based on archaeological evidence
SEASONAL_PROFILES = {
    ResourceZone.AQUATIC: SeasonalProfile(
        spring=1.5,  # Fish runs, spawning
        summer=1.3,  # Peak aquatic productivity
        fall=0.8,    # Declining
        winter=0.5   # Low aquatic activity
    ),
    ResourceZone.TERRESTRIAL: SeasonalProfile(
        spring=0.7,  # Lean season for deer
        summer=0.8,  # Fawning, dispersed
        fall=1.4,    # Fat deer, concentrated
        winter=1.1   # Hunting continues
    ),
    ResourceZone.MAST: SeasonalProfile(
        spring=0.0,  # No nuts
        summer=0.1,  # Green nuts forming
        fall=2.0,    # Harvest season!
        winter=0.5   # Stored nuts depleting
    ),
    ResourceZone.ECOTONE: SeasonalProfile(
        spring=1.0,  # Balanced access
        summer=1.0,
        fall=1.2,    # Slight fall peak
        winter=0.8
    )
}


@dataclass
class EcologicalPatch:
    """
    A resource patch with ecological zone characteristics.

    Patches have:
    - A primary resource zone type
    - Base productivity
    - Seasonal variation following zone profile
    - Inter-annual stochastic variation
    """
    patch_id: int
    zone_type: ResourceZone
    location: Tuple[float, float]
    base_productivity: float
    variability: float  # Inter-annual variation (SD)

    # State
    current_productivity: float = 0.0
    annual_shock: float = 0.0  # Year-specific deviation

    def update_annual_shock(self, rng: np.random.Generator) -> None:
        """Set the annual productivity shock for this patch."""
        self.annual_shock = rng.normal(0, self.variability)

    def get_seasonal_productivity(self, month: int) -> float:
        """Calculate productivity for a given month."""
        seasonal_mult = SEASONAL_PROFILES[self.zone_type].get_multiplier(month)
        self.current_productivity = max(0.0,
            self.base_productivity * seasonal_mult + self.annual_shock
        )
        return self.current_productivity


@dataclass
class EnvironmentConfig:
    """Configuration for the environmental model."""
    # Spatial
    region_size: float = 500.0  # km

    # Zone distribution
    n_aquatic_patches: int = 10
    n_terrestrial_patches: int = 12
    n_mast_patches: int = 8
    n_ecotone_patches: int = 5

    # Productivity
    aquatic_base_productivity: float = 0.7
    terrestrial_base_productivity: float = 0.6
    mast_base_productivity: float = 0.5  # But highly seasonal
    ecotone_base_productivity: float = 0.65

    # Variability (inter-annual)
    aquatic_variability: float = 0.15
    terrestrial_variability: float = 0.10
    mast_variability: float = 0.30  # Mast crops highly variable
    ecotone_variability: float = 0.12

    # Covariance structure
    # Negative covariance = buffering (when one fails, another may succeed)
    aquatic_terrestrial_cov: float = -0.3  # Some buffering
    aquatic_mast_cov: float = 0.1  # Slight positive (both weather-dependent)
    terrestrial_mast_cov: float = 0.2  # Moderate positive


class Environment:
    """
    Environmental model with multiple ecological zones.

    Implements:
    - Spatially distributed patches of different zone types
    - Seasonal productivity cycles
    - Correlated inter-annual variation (for buffering effects)
    - Ecotone locations with access to multiple zones
    """

    def __init__(self, config: EnvironmentConfig, seed: int = 42):
        self.config = config
        self.rng = np.random.default_rng(seed)
        self.year = 0
        self.month = 1

        # Initialize patches
        self.patches = self._create_patches()

        # Create covariance matrix for annual shocks
        self.cov_matrix = self._build_covariance_matrix()

    def _create_patches(self) -> List[EcologicalPatch]:
        """Create spatially distributed patches of each zone type."""
        patches = []
        patch_id = 0

        # Helper to create patches of a given type
        def add_patches(zone: ResourceZone, n: int, base_prod: float, var: float,
                       center: Optional[Tuple[float, float]] = None,
                       spread: Optional[float] = None) -> None:
            nonlocal patch_id
            for _ in range(n):
                if center is not None and spread is not None:
                    # Clustered around a center point
                    x = center[0] + self.rng.normal(0, spread)
                    y = center[1] + self.rng.normal(0, spread)
                else:
                    # Random distribution
                    x = self.rng.uniform(0, self.config.region_size)
                    y = self.rng.uniform(0, self.config.region_size)

                # Clip to region
                x = max(0, min(self.config.region_size, x))
                y = max(0, min(self.config.region_size, y))

                patches.append(EcologicalPatch(
                    patch_id=patch_id,
                    zone_type=zone,
                    location=(x, y),
                    base_productivity=base_prod + self.rng.normal(0, 0.05),
                    variability=var
                ))
                patch_id += 1

        # Aquatic patches along rivers/bayous (linear distribution)
        center = self.config.region_size / 2
        for _ in range(self.config.n_aquatic_patches):
            x = center + self.rng.normal(0, 50)  # Along central axis
            y = self.rng.uniform(0, self.config.region_size)
            patches.append(EcologicalPatch(
                patch_id=patch_id,
                zone_type=ResourceZone.AQUATIC,
                location=(x, y),
                base_productivity=self.config.aquatic_base_productivity,
                variability=self.config.aquatic_variability
            ))
            patch_id += 1

        # Terrestrial patches (widely distributed in uplands)
        add_patches(
            ResourceZone.TERRESTRIAL,
            self.config.n_terrestrial_patches,
            self.config.terrestrial_base_productivity,
            self.config.terrestrial_variability
        )

        # Mast patches (clustered in hardwood areas)
        add_patches(
            ResourceZone.MAST,
            self.config.n_mast_patches,
            self.config.mast_base_productivity,
            self.config.mast_variability,
            center=(center - 100, center),  # West of center
            spread=80
        )

        # Ecotone patches (at Poverty Point location and similar)
        # These are the prime locations where multiple zones intersect
        pp_location = (center, center)  # Poverty Point at center
        add_patches(
            ResourceZone.ECOTONE,
            self.config.n_ecotone_patches,
            self.config.ecotone_base_productivity,
            self.config.ecotone_variability,
            center=pp_location,
            spread=30
        )

        return patches

    def _build_covariance_matrix(self) -> np.ndarray:
        """
        Build covariance matrix for annual productivity shocks.

        Patches of different zone types can have correlated shocks.
        Negative correlation = buffering effect.
        """
        n = len(self.patches)
        cov = np.eye(n)

        for i, patch_i in enumerate(self.patches):
            for j, patch_j in enumerate(self.patches):
                if i >= j:
                    continue

                # Base covariance on zone types
                zones = {patch_i.zone_type, patch_j.zone_type}

                if zones == {ResourceZone.AQUATIC, ResourceZone.TERRESTRIAL}:
                    cov_val = self.config.aquatic_terrestrial_cov
                elif zones == {ResourceZone.AQUATIC, ResourceZone.MAST}:
                    cov_val = self.config.aquatic_mast_cov
                elif zones == {ResourceZone.TERRESTRIAL, ResourceZone.MAST}:
                    cov_val = self.config.terrestrial_mast_cov
                elif patch_i.zone_type == patch_j.zone_type:
                    # Same zone type: positive correlation
                    cov_val = 0.5
                else:
                    # Ecotone with others: slight positive
                    cov_val = 0.1

                # Scale by variance
                var_i = patch_i.variability ** 2
                var_j = patch_j.variability ** 2
                cov[i, j] = cov_val * np.sqrt(var_i * var_j)
                cov[j, i] = cov[i, j]

        # Ensure positive semi-definite
        eigvals = np.linalg.eigvalsh(cov)
        if eigvals.min() < 0:
            cov += np.eye(n) * (abs(eigvals.min()) + 0.01)

        return cov

    def advance_year(self) -> None:
        """Advance to a new year with correlated productivity shocks."""
        self.year += 1

        # Generate correlated annual shocks
        n = len(self.patches)
        try:
            shocks = self.rng.multivariate_normal(np.zeros(n), self.cov_matrix)
        except np.linalg.LinAlgError:
            # Fallback to independent shocks if covariance issues
            shocks = self.rng.normal(0, 1, n)

        for i, patch in enumerate(self.patches):
            patch.annual_shock = shocks[i] * patch.variability

    def advance_month(self) -> None:
        """Advance to the next month."""
        self.month += 1
        if self.month > 12:
            self.month = 1
            self.advance_year()

    def get_patch_productivity(self, patch_id: int) -> float:
        """Get current productivity for a specific patch."""
        return self.patches[patch_id].get_seasonal_productivity(self.month)

    def get_zone_productivity(self, zone: ResourceZone) -> float:
        """Get average productivity across all patches of a zone type."""
        zone_patches = [p for p in self.patches if p.zone_type == zone]
        if not zone_patches:
            return 0.0
        return float(np.mean([p.get_seasonal_productivity(self.month)
                       for p in zone_patches]))

    def get_location_value(self, location: Tuple[float, float],
                          access_radius: float = 50.0) -> Dict[str, float]:
        """
        Calculate the resource value of a location based on accessible patches.

        Args:
            location: (x, y) coordinates
            access_radius: Maximum distance to access resources

        Returns:
            Dictionary with productivity by zone type and total
        """
        values = {zone.value: 0.0 for zone in ResourceZone}
        n_accessible = {zone.value: 0 for zone in ResourceZone}

        for patch in self.patches:
            dx = patch.location[0] - location[0]
            dy = patch.location[1] - location[1]
            distance = np.sqrt(dx**2 + dy**2)

            if distance <= access_radius:
                # Productivity weighted by proximity
                weight = 1.0 - (distance / access_radius)
                prod = patch.get_seasonal_productivity(self.month)
                values[patch.zone_type.value] += prod * weight
                n_accessible[patch.zone_type.value] += 1

        # Calculate diversity bonus (access to multiple zone types)
        n_zones = sum(1 for v in n_accessible.values() if v > 0)
        diversity_bonus = 0.1 * (n_zones - 1) if n_zones > 1 else 0

        total = sum(values.values()) + diversity_bonus
        values['total'] = total
        values['diversity_bonus'] = diversity_bonus
        values['n_zones_accessible'] = n_zones

        return values

    def find_optimal_aggregation_site(self,
                                      n_candidates: int = 100,
                                      access_radius: float = 50.0
                                      ) -> Tuple[Tuple[float, float], float]:
        """
        Find the optimal location for aggregation based on resource access.

        Returns:
            Tuple of (best_location, value)
        """
        best_location = (self.config.region_size / 2, self.config.region_size / 2)
        best_value = 0.0

        for _ in range(n_candidates):
            x = self.rng.uniform(0, self.config.region_size)
            y = self.rng.uniform(0, self.config.region_size)
            value_dict = self.get_location_value((x, y), access_radius)
            total = value_dict['total']

            if total > best_value:
                best_value = total
                best_location = (x, y)

        return best_location, best_value


def test_environment():
    """Test the environmental model."""
    config = EnvironmentConfig()
    env = Environment(config, seed=42)

    print("Environment initialized:")
    print(f"  Total patches: {len(env.patches)}")

    for zone in ResourceZone:
        zone_patches = [p for p in env.patches if p.zone_type == zone]
        print(f"  {zone.value}: {len(zone_patches)} patches")

    # Test seasonal variation
    print("\nSeasonal productivity by zone:")
    for month in [3, 6, 9, 12]:  # Spring, Summer, Fall, Winter
        env.month = month
        print(f"  Month {month}:")
        for zone in ResourceZone:
            prod = env.get_zone_productivity(zone)
            print(f"    {zone.value}: {prod:.3f}")

    # Test location value
    center = config.region_size / 2
    print(f"\nLocation value at center ({center}, {center}):")
    values = env.get_location_value((center, center))
    for k, v in values.items():
        print(f"  {k}: {v:.3f}")

    # Find optimal aggregation site
    print("\nSearching for optimal aggregation site...")
    best_loc, best_val = env.find_optimal_aggregation_site()
    print(f"  Best location: ({best_loc[0]:.1f}, {best_loc[1]:.1f})")
    print(f"  Value: {best_val:.3f}")

    return env


if __name__ == "__main__":
    test_environment()
