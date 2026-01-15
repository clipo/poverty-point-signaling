# ABM Architecture: Poverty Point Aggregation Model

## 1. Design Philosophy

The ABM must faithfully implement the theoretical framework while allowing emergent dynamics to validate (or challenge) theoretical predictions. Key design principles:

1. **Theory-Driven Parameters**: All parameters derive from the theoretical derivation
2. **Emergent Outcomes**: Strategy frequencies, aggregation sizes, and investment levels should emerge from individual decisions
3. **Phase Space Exploration**: Model must efficiently explore σ × ε × n parameter space
4. **Validation Metrics**: Output metrics must map to theoretical predictions and archaeological observables

## 2. Model Components

### 2.1 Agents: Bands

**Properties:**
```python
@dataclass
class Band:
    band_id: int
    size: int                      # Number of individuals (15-35)
    home_location: Tuple[float, float]  # Base foraging location
    strategy: Strategy             # AGGREGATOR or INDEPENDENT

    # State variables
    resources: float               # Current resource holdings
    prestige: float               # Accumulated signaling prestige
    monument_contributions: float  # Total monument investment
    exotic_goods: int             # Count of exotic items held

    # Social network
    obligations: Dict[int, float]  # band_id -> obligation strength

    # History
    aggregation_history: List[bool]  # Participated in each year
    fitness_history: List[float]     # Fitness each year
```

**Behaviors:**
- `decide_strategy()`: Choose AGGREGATOR or INDEPENDENT based on expected fitness
- `forage()`: Acquire resources from local patches during dispersal
- `travel_to_aggregation()`: Move to aggregation site (pay travel cost)
- `invest_in_monument()`: Contribute resources to monument (signal)
- `acquire_exotic()`: Obtain exotic goods (individual signal)
- `form_obligation()`: Create reciprocal tie with another band
- `call_obligation()`: Request help during shortfall
- `reproduce()`: Population growth based on resources
- `suffer_mortality()`: Deaths during shortfall

### 2.2 Environment

**Ecological Zones:**
```python
class ResourceZone(Enum):
    AQUATIC = "aquatic"       # Fish, waterfowl - floodplain/bayou
    TERRESTRIAL = "terrestrial"  # Deer, small game - uplands
    MAST = "mast"             # Nuts - hardwood forests
    WETLAND = "wetland"       # Mixed resources - margins
```

**Properties:**
```python
@dataclass
class Environment:
    # Spatial
    region_size: float = 500.0    # km
    zones: List[ResourceZone]
    zone_locations: Dict[ResourceZone, List[Tuple[float, float]]]

    # Productivity
    base_productivity: Dict[ResourceZone, float]
    seasonal_profile: Dict[ResourceZone, Dict[str, float]]

    # Uncertainty
    sigma: float                  # Environmental uncertainty parameter
    zone_covariance: np.ndarray   # Covariance matrix between zones

    # State
    current_year: int
    current_productivity: Dict[ResourceZone, float]
    in_shortfall: bool
    shortfall_remaining: int      # Years remaining in current shortfall
```

**Ecotone Calculation:**
```python
def calculate_ecotone_advantage(location: Tuple[float, float]) -> float:
    """
    Calculate ε for a location based on multi-zone access.

    ε = f(number of zones accessible, zone covariances)

    Higher ε at locations where multiple zones with negative
    covariance are accessible.
    """
    accessible_zones = get_accessible_zones(location, access_radius=50)

    if len(accessible_zones) <= 1:
        return 0.0

    # Calculate variance reduction from multi-zone access
    # Uses covariance matrix to compute portfolio effect
    zone_indices = [z.value for z in accessible_zones]
    sub_cov = zone_covariance[np.ix_(zone_indices, zone_indices)]

    # Variance of equal-weighted portfolio
    n = len(accessible_zones)
    portfolio_var = np.sum(sub_cov) / (n * n)
    single_zone_var = np.mean(np.diag(sub_cov))

    # ε is proportional to variance reduction
    if single_zone_var > 0:
        epsilon = 1.0 - np.sqrt(portfolio_var / single_zone_var)
    else:
        epsilon = 0.0

    return max(0.0, min(0.5, epsilon))
```

### 2.3 Aggregation Site

```python
@dataclass
class AggregationSite:
    site_id: int
    name: str
    location: Tuple[float, float]
    ecotone_advantage: float      # ε for this location

    # Infrastructure
    monument_level: float         # Cumulative investment
    monument_history: List[float] # Investment per year

    # Current aggregation
    attending_bands: List[int]
    current_population: int

    # Exotic goods
    total_exotics: int
    exotic_sources: Dict[str, int]  # source_region -> count
```

## 3. Simulation Dynamics

### 3.1 Annual Cycle

```
YEAR t:
├── SHORTFALL CHECK
│   ├── Determine if shortfall occurs (based on σ)
│   └── Set productivity levels for all zones
│
├── DISPERSAL SEASON (75% of year)
│   ├── Bands forage in home territories
│   ├── Resource acquisition = f(zone productivity, band size)
│   ├── Independent bands: full foraging
│   └── Aggregator bands: reduced foraging (preparing for travel)
│
├── AGGREGATION DECISION
│   ├── Each band calculates expected W_agg vs W_ind
│   ├── Strategy may switch based on comparison
│   └── Aggregators commit to travel
│
├── AGGREGATION SEASON (25% of year)
│   ├── Aggregators travel to site (pay C_travel)
│   ├── Collective activities (cooperation benefits f(n))
│   ├── Monument investment (pay C_signal)
│   ├── Exotic acquisition (individual signals)
│   ├── Obligation formation (social network)
│   └── Independents continue foraging
│
├── SHORTFALL MORTALITY (if shortfall active)
│   ├── Aggregators: mortality = α_agg × σ_eff
│   ├── Independents: mortality = β_ind × σ
│   └── Obligations can be called to reduce mortality
│
├── REPRODUCTION
│   ├── Growth based on net resources
│   ├── Aggregators: reduced by C_total
│   └── Independents: full reproduction (R_ind bonus)
│
└── RECORD STATE
    ├── Population sizes
    ├── Strategy frequencies
    ├── Monument levels
    ├── Exotic distributions
    └── Fitness outcomes
```

### 3.2 Key Mechanisms

#### Shortfall Generation
```python
def generate_shortfall(sigma: float, rng: np.random.Generator) -> Tuple[bool, float, int]:
    """
    Generate shortfall event based on σ parameter.

    σ encodes frequency, magnitude, and duration:
    - Higher σ = more frequent, more severe shortfalls

    Returns: (is_shortfall, magnitude, duration)
    """
    # Frequency: mean inter-arrival time decreases with σ
    frequency_years = int(20 * (1 - sigma) + 5)  # 5-20 years

    # Probability of shortfall this year
    p_shortfall = 1.0 / frequency_years

    if rng.random() < p_shortfall:
        # Magnitude scales with σ
        magnitude = 0.3 + 0.5 * sigma + rng.normal(0, 0.1)
        magnitude = np.clip(magnitude, 0.2, 0.9)

        # Duration increases with magnitude
        duration = max(1, int(1 + magnitude * 2.5))

        return True, magnitude, duration

    return False, 0.0, 0
```

#### Fitness Calculation
```python
def calculate_fitness(band: Band,
                      aggregated: bool,
                      n_aggregating: int,
                      sigma: float,
                      epsilon: float,
                      params: SimulationParameters) -> float:
    """
    Calculate realized fitness for a band this year.
    Implements the theoretical fitness functions.
    """
    if aggregated:
        # Aggregator fitness
        C_total = params.C_travel + params.C_signal + params.C_opportunity

        # Effective uncertainty (reduced by ecotone)
        sigma_eff = sigma * (1.0 - epsilon)

        # Survival
        survival = 1.0 - params.alpha_agg * sigma_eff

        # Cooperation benefits
        f_n = cooperation_benefit(n_aggregating, params)

        # Reciprocal benefits
        recip = 1.0 + params.B_recip * len(band.obligations)

        W = (1.0 - C_total) * survival * f_n * recip

    else:
        # Independent fitness
        survival = 1.0 - params.beta_ind * sigma
        W = params.R_ind * survival

    return max(0.0, W)
```

#### Strategy Decision
```python
def decide_strategy(band: Band,
                    environment: Environment,
                    aggregation_site: AggregationSite,
                    params: SimulationParameters) -> Strategy:
    """
    Band decides whether to aggregate based on expected fitness.

    Includes some stochasticity and memory of past outcomes.
    """
    # Calculate expected fitness for each strategy
    # (Using current estimates of n, σ, ε)

    expected_n = estimate_aggregation_size(aggregation_site, bands)

    E_W_agg = calculate_expected_fitness(
        aggregated=True,
        n=expected_n,
        sigma=environment.sigma,
        epsilon=aggregation_site.ecotone_advantage,
        params=params
    )

    E_W_ind = calculate_expected_fitness(
        aggregated=False,
        sigma=environment.sigma,
        params=params
    )

    # Decision with some noise (bounded rationality)
    fitness_diff = E_W_agg - E_W_ind

    # Memory effect: past aggregation success influences decision
    if len(band.aggregation_history) > 0:
        recent_success = np.mean(band.fitness_history[-5:])
        expected_success = np.mean(band.fitness_history)
        memory_bonus = 0.1 * (recent_success - expected_success)
        fitness_diff += memory_bonus if band.aggregation_history[-1] else -memory_bonus

    # Probabilistic choice (sigmoid)
    p_aggregate = 1.0 / (1.0 + np.exp(-10 * fitness_diff))

    if rng.random() < p_aggregate:
        return Strategy.AGGREGATOR
    else:
        return Strategy.INDEPENDENT
```

## 4. Parameters

### 4.1 Theoretical Parameters (from derivation)

| Parameter | Symbol | Value | Source |
|-----------|--------|-------|--------|
| Travel cost | C_travel | 0.12 | Theory |
| Signal cost | C_signal | 0.18 | Theory |
| Opportunity cost | C_opportunity | 0.12 | Theory |
| Aggregator vulnerability | α_agg | 0.40 | Theory |
| Independent vulnerability | β_ind | 0.75 | Theory |
| Independent reproductive advantage | R_ind | 1.10 | Theory |
| Cooperation benefit coefficient | b_coop | 0.08 | Theory |
| Optimal aggregation size | n* | 25 | Theory |
| Crowding cost coefficient | c_crowd | 0.015 | Theory |
| Reciprocal benefit rate | B_recip | 0.05 | Theory |

### 4.2 Environmental Parameters (to vary)

| Parameter | Symbol | Range | Notes |
|-----------|--------|-------|-------|
| Environmental uncertainty | σ | 0.2 - 0.8 | Primary phase space dimension |
| Ecotone advantage | ε | 0.0 - 0.5 | Location-dependent |
| Zone covariance | ρ_ij | -0.4 to +0.4 | Determines ε |

### 4.3 Population Parameters

| Parameter | Value | Notes |
|-----------|-------|-------|
| Number of bands | 50 | Regional population |
| Initial band size | 25 | Individuals per band |
| Birth rate | 0.03 | Per capita annual |
| Death rate | 0.02 | Per capita annual (non-shortfall) |
| Minimum band size | 5 | Below this, band dissolves |
| Maximum band size | 50 | Above this, band fissions |

### 4.4 Spatial Parameters

| Parameter | Value | Notes |
|-----------|-------|-------|
| Region size | 500 km | Diameter |
| Access radius | 50 km | Zone accessibility |
| Aggregation site location | Center | Maximum ecotone |
| Number of zones | 4 | AQUATIC, TERRESTRIAL, MAST, WETLAND |

## 5. Output Metrics

### 5.1 Primary Metrics (Theory Validation)

| Metric | Theoretical Prediction | Calculation |
|--------|----------------------|-------------|
| Strategy dominance | Aggregation when σ > σ* | (N_agg - N_ind) / N_total |
| Critical threshold | σ* ≈ 0.53 at ε=0.35 | σ where dominance crosses 0 |
| Aggregation size | n ≈ 25 at optimum | Mean bands at aggregation |
| Monument investment | Proportional to n × σ | Total monument level |

### 5.2 Archaeological Observables

| Metric | Archaeological Analog | Notes |
|--------|----------------------|-------|
| Monument level | Mound/ridge volume | Cumulative investment |
| Construction rate | Bayesian construction model | Annual investment |
| Exotic count | Excavated quantities | Total exotic goods |
| Exotic diversity | Source representation | Number of source regions |
| Site hierarchy | Site size distribution | Investment by location |

### 5.3 Diagnostic Metrics

| Metric | Purpose |
|--------|---------|
| Population trajectory | Stability check |
| Fitness distributions | Selection pressure |
| Strategy switching rate | Equilibrium check |
| Network density | Social structure |

## 6. Simulation Protocol

### 6.1 Phase Space Exploration

```python
# Phase space grid
sigma_values = np.linspace(0.2, 0.8, 13)    # 13 values
epsilon_values = np.linspace(0.0, 0.5, 11)  # 11 values
n_replicates = 50                            # Per parameter combination

# Total runs: 13 × 11 × 50 = 7,150 simulations
```

### 6.2 Single Run Protocol

```python
def run_simulation(sigma: float, epsilon: float, seed: int) -> SimulationResults:
    """
    Run single simulation with given parameters.

    Duration: 600 years (matching Poverty Point span)
    Burn-in: 100 years (allow strategy equilibration)
    Analysis window: 500 years
    """
    # Initialize
    config = SimulationConfig(
        sigma=sigma,
        epsilon=epsilon,
        seed=seed,
        duration=600,
        burn_in=100
    )

    sim = PovertyPointSimulation(config)

    # Run
    results = sim.run()

    # Extract metrics
    return SimulationResults(
        sigma=sigma,
        epsilon=epsilon,
        seed=seed,
        strategy_dominance=calculate_dominance(results),
        mean_aggregation_size=calculate_mean_n(results),
        final_monument_level=results.monument_level,
        total_exotics=results.exotic_count,
        population_trajectory=results.population_history,
        # ... additional metrics
    )
```

### 6.3 Analysis Protocol

```python
def analyze_phase_space(results: List[SimulationResults]) -> PhaseSpaceAnalysis:
    """
    Analyze results across phase space.

    1. Calculate mean dominance at each (σ, ε) point
    2. Identify empirical critical threshold
    3. Compare with theoretical prediction
    4. Calculate confidence intervals
    """
    # Group by parameters
    grouped = group_by_params(results)

    # Calculate statistics at each point
    dominance_mean = {}
    dominance_std = {}

    for (sigma, epsilon), runs in grouped.items():
        dominances = [r.strategy_dominance for r in runs]
        dominance_mean[(sigma, epsilon)] = np.mean(dominances)
        dominance_std[(sigma, epsilon)] = np.std(dominances)

    # Find empirical critical threshold
    sigma_star_empirical = find_threshold(dominance_mean)

    # Compare with theory
    sigma_star_theory = critical_threshold(epsilon, n=25, params)

    return PhaseSpaceAnalysis(
        dominance_mean=dominance_mean,
        dominance_std=dominance_std,
        sigma_star_empirical=sigma_star_empirical,
        sigma_star_theory=sigma_star_theory,
        correlation=calculate_correlation(sigma_star_empirical, sigma_star_theory)
    )
```

## 7. Validation Criteria

### 7.1 Theory-ABM Agreement

The ABM validates the theory if:

1. **Phase transition exists**: Clear boundary between strategy dominance regions
2. **Threshold location**: Empirical σ* within 0.1 of theoretical σ*
3. **Ecotone effect**: Higher ε shifts threshold to lower σ (as predicted)
4. **Aggregation size**: Emergent n near theoretical optimum (n* ≈ 25)

### 7.2 Emergent Patterns

The ABM should show emergent patterns consistent with archaeology:

1. **Site primacy**: One dominant aggregation site at high-ε location
2. **Distance decay**: Participation declines with distance
3. **Construction pulses**: Monument investment varies with σ
4. **Exotic concentration**: Exotics accumulate at aggregation site

### 7.3 Sensitivity Analysis

Key sensitivities to test:

1. **σ perturbation**: How much does ±0.1 σ change outcomes?
2. **ε perturbation**: How much does ±0.1 ε change outcomes?
3. **Initial conditions**: Do different initial strategy mixes converge?
4. **Stochasticity**: How much run-to-run variation?

## 8. Implementation Plan

### Phase 1: Core Simulation
- [ ] Refactor `simulation.py` to match architecture
- [ ] Implement theoretical fitness functions
- [ ] Add shortfall generation
- [ ] Add strategy decision logic

### Phase 2: Environment
- [ ] Update `environment.py` with zone covariance
- [ ] Implement ecotone calculation
- [ ] Add seasonal productivity profiles

### Phase 3: Phase Space Exploration
- [ ] Create exploration script
- [ ] Implement parallel execution
- [ ] Add results aggregation

### Phase 4: Analysis
- [ ] Calculate all output metrics
- [ ] Compare with theoretical predictions
- [ ] Generate validation figures

### Phase 5: Sensitivity Analysis
- [ ] Parameter perturbation runs
- [ ] Initial condition tests
- [ ] Stochasticity analysis

---

## Appendix: File Structure

```
src/poverty_point/
├── __init__.py
├── simulation.py         # Main simulation class
├── environment.py        # Environmental model
├── agents.py            # Band and AggregationSite classes
├── parameters.py        # Parameter dataclasses
├── metrics.py           # Output metric calculations
└── analysis.py          # Phase space analysis

scripts/
├── figure_generation/
│   ├── theoretical_predictions.py
│   └── abm_validation.py
├── exploration/
│   ├── run_phase_space.py
│   └── analyze_results.py
└── sensitivity/
    └── perturbation_analysis.py

results/
├── phase_space/         # Raw simulation outputs
├── analysis/            # Aggregated statistics
└── figures/             # Generated figures
```
