# Poverty Point Project Status

## Project Setup Complete

### Directory Structure
```
/Users/clipo/PycharmProjects/poverty-point-signaling/
├── CLAUDE.md                   # Project instructions and context
├── README.md                   # Project overview
├── src/poverty_point/
│   ├── __init__.py            # Package definition
│   └── simulation.py          # Core simulation (WORKING)
├── data/
│   ├── raw/
│   │   └── DATA_SOURCES.md    # Documented data sources
│   └── processed/
├── docs/
│   ├── manuscript/
│   ├── FEASIBILITY_ANALYSIS.md # Detailed feasibility assessment
│   └── PROJECT_STATUS.md      # This file
├── figures/final/
├── scripts/
│   ├── data_processing/
│   └── figure_generation/
└── tests/
```

### Simulation Model: Initial Implementation

The core simulation is implemented with:

**Agent Types:**
- `Band`: Hunter-gatherer bands with size, strategy, food stores, prestige
- `ResourcePatch`: Foraging patches with variable productivity
- `AggregationSite`: Central gathering location (Poverty Point)

**Dynamics:**
- Seasonal cycle: dispersal (foraging) vs. aggregation (cooperation)
- Band decision-making about aggregation based on costs/benefits
- Monument investment during aggregation
- Exotic goods acquisition
- Cooperation benefits scaling with attendees and infrastructure

**Initial Test Results (100 years):**
- Population: 355 individuals in 30 bands
- Monument investment: 2,552 units accumulated
- Exotic goods: 394 items acquired

## Key Theoretical Framework

### Adaptation from Chaco/Rapa Nui Models

| Aspect | Territorial Model | Aggregation Model |
|--------|------------------|-------------------|
| Units | Permanent groups | Mobile bands |
| Timing | Continuous | Seasonal episodes |
| Signal function | Deter competitors | Attract cooperators |
| Benefit | Conflict reduction | Cooperation gains |
| Decision | Investment level | Whether to aggregate |

### Environmental Uncertainty (σ)

For hunter-gatherers, σ derives from:
- Seasonal resource variability
- Inter-annual fluctuations
- Spatial patchiness
- Unpredictable events

Signaling becomes adaptive when cooperation benefits outweigh aggregation costs.

## Data Sources Identified

### Archaeological
- Radiocarbon chronology (Kidder et al. 2021, American Antiquity)
- Construction data (Ortmann & Kidder 2013, Geoarchaeology)
- Exotic goods provenience (Hill et al. 2016, JAS Reports)

### Paleoclimate
- Limited annual-resolution data for this region/period
- Gulf coast proxies available at coarser resolution
- May need to use stochastic modeling rather than empirical series

## Next Steps

### Phase 1: Model Calibration
1. Compile radiocarbon database from publications
2. Extract labor estimates from Ortmann/Kidder
3. Document exotic goods quantities and distributions
4. Calibrate model parameters to ethnographic ranges

### Phase 2: Scenario Development
1. Baseline: Full aggregation with signaling
2. No-signaling: Aggregation without costly investment
3. No-aggregation: Independent bands, no cooperation
4. Sensitivity analysis on uncertainty parameter

### Phase 3: Analysis
1. Run replicate simulations (following Chaco protocol)
2. Compare predictions to archaeological patterns
3. Statistical validation with confidence intervals

### Phase 4: Manuscript
1. Introduction: The Poverty Point paradox
2. Theory: Aggregation-based costly signaling
3. Methods: Data and model description
4. Results: Simulation outcomes
5. Discussion: Implications

## Comparison with Existing Projects

| Project | Status | Replicates | Manuscript |
|---------|--------|------------|------------|
| Rapa Nui | Complete | 100/scenario | Published |
| Chaco Canyon | Complete | 100/scenario | Draft complete |
| Poverty Point | Started | Pending | Outline only |

## Files Created This Session

1. `/Users/clipo/PycharmProjects/poverty-point-signaling/CLAUDE.md`
2. `/Users/clipo/PycharmProjects/poverty-point-signaling/README.md`
3. `/Users/clipo/PycharmProjects/poverty-point-signaling/docs/FEASIBILITY_ANALYSIS.md`
4. `/Users/clipo/PycharmProjects/poverty-point-signaling/data/raw/DATA_SOURCES.md`
5. `/Users/clipo/PycharmProjects/poverty-point-signaling/src/poverty_point/__init__.py`
6. `/Users/clipo/PycharmProjects/poverty-point-signaling/src/poverty_point/simulation.py`
7. `/Users/clipo/PycharmProjects/poverty-point-signaling/docs/PROJECT_STATUS.md`
8. `/Users/clipo/PycharmProjects/poverty-point-signaling/data/raw/ECOLOGICAL_CONTEXT.md`
9. `/Users/clipo/PycharmProjects/poverty-point-signaling/src/poverty_point/environment.py`

## Recent Updates

### Environment Module (environment.py)

Implemented multi-zone ecological model based on ecotone hypothesis:

**Resource Zones:**
- AQUATIC: Fish, waterfowl, turtles (spring/summer peak)
- TERRESTRIAL: Deer, small game (fall/winter peak)
- MAST: Nuts - pecans, hickory (fall harvest only)
- ECOTONE: Mixed access (balanced year-round)

**Key Features:**
- Seasonal productivity cycles for each zone type
- Inter-annual stochastic variation with covariance structure
- Negative covariance between zones = buffering effect
- Location value calculation based on accessible patches
- Diversity bonus for multi-zone access
- Optimal aggregation site finder

**Test Results:**
- 35 patches distributed across 4 zone types
- Seasonal variation working correctly
- Center location provides access to 2 zones with diversity bonus
- Optimal site search identifies best aggregation locations

### Waiting For
- PDFs to be added to `/pdfs` directory for detailed calibration
- ~~Integration of environment.py with simulation.py~~ **COMPLETED**

## Major Updates (January 2026)

### Integrated Simulation Complete

Successfully integrated all modules into a comprehensive simulation framework:

**New Files Created:**
- `/src/poverty_point/integrated_simulation.py` - Main integrated simulation
- `/src/poverty_point/environmental_scenarios.py` - Pre-defined environmental scenarios
- `/src/poverty_point/parameters.py` - Theoretical parameter definitions
- `/src/poverty_point/agents.py` - Band and AggregationSite agents
- `/scripts/run_comprehensive_analysis.py` - Systematic analysis script
- `/scripts/figure_generation/integrated_results_figures.py` - Publication figures

### Key Results

**Phase Transition Validated:**
- Model produces sharp transition at σ_eff ≈ 0.54
- Matches theoretical prediction of σ* ≈ 0.53
- Below threshold: 96% independent strategy dominance
- Above threshold: 24% independent (aggregation competitive)

**Scenario Comparison (500-year simulations):**

| Scenario | Mean σ_eff | Dominance | Monument | Exotics |
|----------|------------|-----------|----------|---------|
| Low | 0.081 | -0.96 | 5,521 | 895 |
| Poverty Point | 0.197 | -0.91 | 5,920 | 1,909 |
| High | 0.426 | -0.60 | 7,193 | 5,265 |
| Critical | 0.282 | -0.84 | 8,744 | 3,289 |

**Archaeological Calibration:**
- Monument scaling factor: 142.6 (model units → m³)
- Scaled monument: ~750,000 m³ (matches archaeological estimate)
- Exotic goods within plausible range

### Figures Generated

Publication-quality figures saved to `/figures/integrated/`:
1. `fig_phase_transition.png/pdf` - Phase transition validation
2. `fig_phase_space.png/pdf` - σ × ε phase space structure
3. `fig_scenario_comparison.png/pdf` - Time series by scenario
4. `fig_calibration.png/pdf` - Archaeological comparison
5. `fig_summary.png/pdf` - Comprehensive results summary

### Manuscript Status

- **Theoretical framework**: Complete (`docs/manuscript/theoretical_framework.md`)
- **Simulation results**: Complete (`docs/manuscript/simulation_results.md`)
- **Figures**: Generated and saved
- **Remaining**: Final manuscript assembly and submission

### Technical Notes

- Fixed numpy type serialization issues for JSON output
- All simulation results reproducible with seed=42
- Analysis takes ~5 minutes to run full parameter sweep
