# Poverty Point Costly Signaling Project: Development Plan

**Created**: January 15, 2026
**Last Updated**: January 15, 2026
**Status**: Initial Development Phase

---

## 1. Executive Summary

This project applies costly signaling theory to explain the Poverty Point phenomenon: why mobile hunter-gatherers invested massively in monumental earthwork construction and long-distance exotic goods acquisition. Unlike the Rapa Nui and Chaco Canyon cases (which involve agricultural societies with territorial signaling), Poverty Point requires a fundamentally different model based on **aggregation dynamics** and **fission-fusion social structure**.

### The Core Puzzle
- Mobile hunter-gatherers typically minimize investment in permanent architecture
- Yet Poverty Point (1700-1100 BCE) shows ~1 million cubic meters of earthwork construction
- Exotic goods sourced from 1,600+ km away (Great Lakes copper, Appalachian steatite)
- Site is orders of magnitude larger than any contemporary site
- Why this location? Why such investment? Why did it end?

### Theoretical Innovation
The model must capture:
1. **Temporal aggregation** (seasonal gathering vs. year-round dispersal)
2. **Spatial optimization** (why this ecotone location)
3. **Benefits of aggregation** that justify the signaling costs
4. **Exotic goods** as individual-level signals within the collective system

---

## 2. Current Project Status

### 2.1 Completed Components

| Component | File | Status | Notes |
|-----------|------|--------|-------|
| Project structure | Directory tree | Complete | Standard layout matching other projects |
| CLAUDE.md | `/CLAUDE.md` | Complete | Comprehensive project specification |
| Feasibility analysis | `/docs/FEASIBILITY_ANALYSIS.md` | Complete | 12 KB detailed assessment |
| Data sources doc | `/data/raw/DATA_SOURCES.md` | Complete | Archaeological data compilation |
| Ecological context | `/data/raw/ECOLOGICAL_CONTEXT.md` | Complete | Multi-zone ecology at Poverty Point |
| Core simulation | `/src/poverty_point/simulation.py` | Draft | Basic fission-fusion model implemented |
| Environment model | `/src/poverty_point/environment.py` | Draft | Multi-zone seasonal productivity |
| Reference library | `/pdfs/` | 17 PDFs | ~71 MB of key sources |

### 2.2 Key Gaps Identified

1. **Climate/Environmental Data**
   - No annual-resolution paleoclimate proxy compiled
   - Need to identify available databases for Late Holocene SE North America
   - Alternative: model stochastic uncertainty based on modern analogs

2. **Spatial Data**
   - No GIS layers for ecotone boundaries, site locations
   - Need Mississippi/Bayou Macon floodplain extent data
   - Regional site distribution map not compiled

3. **Radiocarbon Database**
   - No compiled database of PP dates
   - Kidder publications have dates but not extracted to database format

4. **Model Integration**
   - `environment.py` and `simulation.py` not yet integrated
   - Need unified seasonal cycle connecting both modules

5. **Exotic Goods Modeling**
   - Current model is simplified (probability-based acquisition)
   - Need source-distance-cost relationships
   - Need individual variation in acquisition/display

6. **Validation Framework**
   - No archaeological pattern metrics defined
   - No test suite comparing model output to empirical patterns

---

## 3. Key Differences from Rapa Nui/Chaco Models

This is critical: the Poverty Point model **cannot be a simple adaptation** of the agricultural-territorial model. Fundamental differences:

| Dimension | Rapa Nui/Chaco | Poverty Point |
|-----------|----------------|---------------|
| Subsistence | Agriculture with storage | Foraging with limited storage |
| Settlement | Permanent/semi-permanent | Seasonal aggregation cycles |
| Social unit | Territorial corporate groups | Fluid band networks |
| Signal target | Competitor groups | Potential cooperators |
| Signal function | Deter conflict | Facilitate coordination |
| Time structure | Continuous investment | Episodic (aggregation season) |
| Environmental σ | Crop failure risk | Foraging patch variability |
| Monument function | Territorial marker | Sunk cost + coordination device |
| Collapse driver | Declining σ* | Location optimality change? |

### Key Modeling Decisions Required

1. **Aggregation decision**: What information do bands use to decide whether to aggregate?
2. **Investment timing**: When during aggregation does signaling occur?
3. **Cooperation benefits**: What specific returns justify aggregation costs?
4. **Exotic goods function**: Individual status signal or inter-band obligation creator?
5. **Population dynamics**: How does aggregation affect reproduction/survival?

---

## 4. Research Data Requirements

### 4.1 Temporal/Climate Data (Priority: High)

**Goal**: Characterize environmental uncertainty (σ) for the region 2000-1000 BCE

| Data Source | Type | Availability | Resolution |
|-------------|------|--------------|------------|
| NOAA Paleoclimate Database | Multiple proxies | Public | Variable |
| Gulf of Mexico sediment cores | Sea surface temp | Published | Centennial |
| Speleothem records (DeSoto Caverns) | Precipitation | Published | Decadal-centennial |
| Pollen records (Lake Tulane, FL) | Vegetation/climate | Published | Centennial |
| Mississippi Delta evolution | Geomorphology | Kidder publications | Episodic |

**Alternative approach**: Model stochastic uncertainty using:
- Modern climate variability as baseline
- Sensitivity analysis across σ ranges
- Compare model outcomes to construction chronology

### 4.2 Spatial Data (Priority: High)

**Goal**: Characterize ecotone position and regional site hierarchy

| Data Need | Source | Status |
|-----------|--------|--------|
| Poverty Point site location | 32.63°N, 91.41°W | Known |
| Macon Ridge extent | USGS/LA geological survey | To compile |
| Mississippi floodplain extent (Late Holocene) | Saucier 1994 | Available |
| Bayou Macon drainage | USGS hydrology | Available |
| Regional PP-period sites | LA Division of Archaeology | Requires access |
| Ecotone boundaries | Vegetation maps + Kidder | To construct |

**Key spatial questions**:
1. Is Poverty Point location optimal for multi-zone access?
2. How does PP location compare to Jaketown, Claiborne, other sites?
3. What is the travel cost structure from different regions?

### 4.3 Archaeological Data (Priority: Medium-High)

**Goal**: Calibrate model parameters and validate predictions

| Data Type | Use | Source |
|-----------|-----|--------|
| Radiocarbon dates | Construction chronology | Kidder et al. publications |
| Construction volumes | Labor investment scaling | Ortmann & Kidder 2013 |
| Exotic goods quantities | Individual signaling intensity | Excavation reports |
| Exotic goods provenience | Source-distance relationships | LA-ICP-MS studies |
| Site size distribution | Regional hierarchy test | Site file compilation |
| Faunal/botanical remains | Subsistence scheduling | Excavation reports |

---

## 5. Development Phases

### Phase 1: Data Compilation and Environment Model (Weeks 1-2)

**Objective**: Compile essential data and complete environment model

#### Tasks:
- [ ] **1.1** Extract radiocarbon dates from PDFs into database format
  - Sources: Kidder 2002, Ortmann 2007
  - Format: CSV with provenience, material, lab number, date, error

- [ ] **1.2** Compile climate/environmental proxy data
  - Search NOAA paleoclimate database for SE North America
  - Document available proxies and resolutions
  - Design stochastic uncertainty model if proxies insufficient

- [ ] **1.3** Create spatial data layers
  - Digitize Macon Ridge boundary
  - Map ecological zone extents
  - Calculate distance to exotic sources

- [ ] **1.4** Complete environment model
  - Integrate `environment.py` with `simulation.py`
  - Implement seasonal productivity cycles
  - Add inter-annual correlated shocks

- [ ] **1.5** Extract exotic goods data
  - Quantities by material type
  - Source distances
  - Temporal distribution (if available)

### Phase 2: Core ABM Development (Weeks 3-4)

**Objective**: Fully functional ABM with hunter-gatherer aggregation dynamics

#### Tasks:
- [ ] **2.1** Revise band decision model
  - Implement information-based aggregation decisions
  - Add memory of past aggregation outcomes
  - Model travel cost/benefit calculations

- [ ] **2.2** Implement aggregation season dynamics
  - Arrival timing effects
  - Collective activity benefits (fishing, construction)
  - Information exchange mechanisms

- [ ] **2.3** Develop monument investment model
  - Cost structure (labor diverted from foraging)
  - Visibility and signal value
  - Cumulative infrastructure benefits

- [ ] **2.4** Implement exotic goods system
  - Source-distance-cost relationships
  - Individual acquisition decisions
  - Display and prestige effects
  - Inter-band exchange/obligations

- [ ] **2.5** Add cooperation benefits module
  - Returns to scale from collective fishing
  - Information sharing value
  - Risk pooling through reciprocal obligations
  - Mating network effects

- [ ] **2.6** Population dynamics
  - Seasonal birth/death rates
  - Aggregation effects on survival
  - Band fission/fusion dynamics

### Phase 3: Calibration and Sensitivity Analysis (Weeks 5-6)

**Objective**: Calibrate to archaeological data and identify key parameters

#### Tasks:
- [ ] **3.1** Parameter calibration
  - Match construction chronology
  - Match regional site hierarchy
  - Match exotic goods distributions

- [ ] **3.2** Sensitivity analysis
  - Vary environmental uncertainty (σ)
  - Vary aggregation benefits
  - Vary travel costs
  - Identify critical thresholds (σ*)

- [ ] **3.3** Scenario development
  - Baseline: Full aggregation with signaling
  - No-signaling control
  - No-aggregation alternative
  - Climate shift scenarios

- [ ] **3.4** Replicate simulations
  - Run 100 replicates per scenario (following Chaco protocol)
  - Calculate confidence intervals
  - Statistical validation

### Phase 4: Analysis and Manuscript (Weeks 7-10)

**Objective**: Complete analysis and draft manuscript

#### Tasks:
- [ ] **4.1** Define testable predictions
  - Site location optimality
  - Construction intensity correlations
  - Exotic goods distribution patterns
  - Collapse conditions

- [ ] **4.2** Compare predictions to archaeological record
  - Quantitative pattern matching
  - Statistical tests where possible
  - Qualitative assessment where not

- [ ] **4.3** Create figures
  - Regional map with ecological zones
  - Model dynamics figure
  - Phase space diagram
  - Validation comparison figures

- [ ] **4.4** Draft manuscript sections
  - Introduction: The Poverty Point paradox
  - Theory: Aggregation-based costly signaling
  - Methods: ABM description
  - Results: Model outcomes
  - Discussion: Archaeological implications

- [ ] **4.5** Internal review and revision

---

## 6. Technical Architecture

### 6.1 Proposed Model Structure

```
PovertyPointSimulation
├── Environment
│   ├── ResourceZones (Aquatic, Terrestrial, Mast, Ecotone)
│   ├── SeasonalCycles
│   ├── InterAnnualShocks (correlated across zones)
│   └── EcotoneLocations
│
├── Agents
│   ├── Bands
│   │   ├── Size, Location, Strategy
│   │   ├── FoodStores, SocialObligations
│   │   ├── ExoticGoods, Prestige
│   │   └── AggregationHistory
│   │
│   └── AggregationSite
│       ├── Location, Infrastructure
│       ├── AttendingBands
│       └── ConstructionHistory
│
├── Dynamics
│   ├── DispersalSeason
│   │   ├── IndependentForaging
│   │   ├── PatchProductivity
│   │   └── PopulationDynamics
│   │
│   └── AggregationSeason
│       ├── AggregationDecision
│       ├── CollectiveActivities
│       ├── MonumentInvestment
│       ├── ExoticAcquisition
│       └── SocialObligationFormation
│
└── Analysis
    ├── ConstructionChronology
    ├── RegionalHierarchy
    ├── ExoticDistributions
    └── CollapseConditions
```

### 6.2 Key Parameters

| Parameter | Description | Initial Range | Calibration Target |
|-----------|-------------|---------------|-------------------|
| n_bands | Number of regional bands | 30-100 | Regional population estimates |
| band_size | Individuals per band | 15-35 | Ethnographic analogs |
| aggregation_duration | Months at site | 2-6 | Seasonal round data |
| travel_cost | Energy per km | Calibrate | Distance decay in site sizes |
| monument_cost | Fraction of surplus | 0.1-0.3 | Construction scale |
| exotic_cost | Acquisition cost by distance | By source | Source representation |
| cooperation_benefit | Returns to aggregation | To estimate | Model emergence |
| environmental_sigma | Foraging uncertainty | 0.1-0.4 | Climate proxies |
| aggregation_threshold | σ* for aggregation adoption | Emergent | Phase transitions |

### 6.3 Output Metrics

| Metric | Archaeological Analog | Validation |
|--------|----------------------|------------|
| Total construction volume | Mound/ridge volumes | Ortmann & Kidder |
| Construction rate over time | Bayesian construction model | Kidder et al. |
| Aggregation population | Site carrying capacity | Faunal/botanical |
| Exotic goods total | Excavated quantities | Gibson |
| Exotic diversity | Source representation | Provenience studies |
| Regional site hierarchy | Site size distribution | LA site files |
| System duration | Occupation span | Radiocarbon dates |

---

## 7. Unique Aspects for Poverty Point

### 7.1 Ecotone Advantage Hypothesis

**Key insight**: Poverty Point's location may be uniquely optimal because it provides:

1. **Multi-zone buffering**: When aquatic resources fail, terrestrial may not (and vice versa)
2. **Extended aggregation feasibility**: Year-round resource access enables longer gatherings
3. **Central position**: Minimizes aggregate travel costs from dispersed bands

**Model implementation**:
- Calculate location value as sum of accessible zone productivities
- Add diversity bonus for multi-zone access
- Compare PP location to alternatives (Jaketown, Claiborne, etc.)

### 7.2 Exotic Goods as Individual Signals

Unlike Chaco (where exotics signal corporate group capacity), Poverty Point exotics may:
- Signal individual capacity/connections within fluid band system
- Create dyadic obligations that persist beyond aggregation
- Function as "advertising" to potential cooperation partners

**Model implementation**:
- Individual agents acquire exotics (not bands as wholes)
- Acquisition creates prestige that affects partner selection
- Exchange creates reciprocal obligations activated during dispersal

### 7.3 Monument as Coordination Device

Poverty Point monuments may serve dual functions:
1. **Sunk cost**: Creates incentive to return (protect investment)
2. **Coordination mechanism**: "We build together" reinforces collective identity

**Model implementation**:
- Track band-specific contributions to monument
- Return probability increases with past investment
- Collective construction episodes during aggregation

### 7.4 Collapse Mechanisms

Several scenarios could explain system end at ~1100 BCE:
1. **Climate shift**: Reduced environmental uncertainty (lower σ)
2. **Ecotone change**: River/floodplain dynamics alter zone boundaries
3. **Alternative sites**: New aggregation locations become viable
4. **Diminishing returns**: Infrastructure benefits plateau

**Model implementation**:
- Run scenarios with parameter shifts
- Identify which changes produce collapse-like patterns
- Compare to archaeological evidence of abandonment

---

## 8. Data Sources to Explore

### 8.1 Climate Databases

| Database | URL | Content |
|----------|-----|---------|
| NOAA Paleoclimatology | https://www.ncdc.noaa.gov/paleo/ | Multiple proxy types |
| PANGAEA | https://www.pangaea.de/ | Marine/lake sediments |
| Neotoma Paleoecology | https://www.neotomadb.org/ | Pollen, macrofossils |
| PAGES 2k | http://pastglobalchanges.org/science/wg/2k-network | Synthesis data |

### 8.2 Archaeological Databases

| Database | Content | Access |
|----------|---------|--------|
| Louisiana SHPO | Site files | Request required |
| CARD (Canadian) | Radiocarbon dates | Public |
| tDAR | Archaeological data repository | Registration |

### 8.3 Spatial Data

| Source | Content | Format |
|--------|---------|--------|
| USGS National Map | Elevation, hydrology | GeoTIFF, Shapefile |
| LA GIS Hub | State-level spatial data | Various |
| SRTM | Elevation data | GeoTIFF |

---

## 9. Reference Library Status

### 9.1 PDFs Currently Available (17 files)

| Citation | Topic | Priority for Data Extraction |
|----------|-------|------------------------------|
| Ford 1954 | Early site description | Low (historical context) |
| Webb 1956 | Classic site description | Medium (basic data) |
| Webb 1968 | Regional extent | Medium (site distribution) |
| Gagliano & Saucier 1963 | SE Louisiana sites | Medium (regional context) |
| Jackson 1981 | Settlement systems | High (theoretical) |
| Jackson 1986 | Sedentism question | High (theoretical) |
| Dunnell & Greenlee 1999 | Regional patterns | Medium |
| Kidder 2002 | Site mapping | High (spatial data) |
| Sassaman 2005 | Structure/event/process | High (theoretical) |
| Kidder 2006 | Climate and transition | High (environmental data) |
| Ortmann 2007 | Mound construction | Very High (construction data) |
| Hamilton 2009 | JAA article | High (theoretical) |
| Hays 2018 | PPO feasting | Medium (social interpretation) |
| Directional Exchange | Exchange patterns | High (exotic goods) |
| Quaternary paper | Climate/environment | High (paleoclimate) |

### 9.2 Additional References Needed

- [ ] Gibson 2000 - *Ancient Mounds of Poverty Point* (book)
- [ ] Kidder et al. 2008 - "Archaeology of singularity" SAA Record
- [ ] Ortmann & Kidder 2013 - Geoarchaeology article
- [ ] Recent (2020s) publications on construction chronology
- [ ] Provenience studies for exotic materials (LA-ICP-MS)

---

## 10. Open Questions Requiring Decision

### 10.1 Theoretical

1. **What is the aggregation season?**
   - Summer (fishing focus)?
   - Fall (nut harvest + deer)?
   - Variable by year?

2. **How do bands know about aggregation benefits?**
   - Perfect information?
   - Memory of past visits?
   - Information from other bands?

3. **What is the primary cooperation benefit?**
   - Collective fishing?
   - Information exchange?
   - Risk pooling?
   - Mating networks?

### 10.2 Empirical

1. **What paleoclimate proxies are available for 1700-1100 BCE?**
   - Need to search databases

2. **Can we reconstruct ecotone boundaries for Late Archaic?**
   - Geomorphology suggests significant changes

3. **What is the size distribution of regional PP-period sites?**
   - Need site file access

### 10.3 Modeling

1. **Should environment module drive simulation directly?**
   - Or use simplified stochastic model?

2. **What temporal resolution?**
   - Monthly (current environment.py)?
   - Seasonal (2 phases/year)?
   - Annual?

3. **How to model exotic goods source depletion?**
   - Not relevant (geological sources)?
   - Relevant (access rights)?

---

## 11. Success Criteria

### 11.1 Model Requirements

1. Reproduces general construction chronology pattern
2. Generates site hierarchy with clear primacy
3. Shows exotic goods concentration at aggregation site
4. Exhibits sensitivity to environmental uncertainty
5. Identifies collapse conditions

### 11.2 Manuscript Goals

1. Clear theoretical contribution (aggregation-based signaling)
2. Novel application to hunter-gatherer monumentality
3. Testable predictions distinguishable from alternatives
4. Archaeological data comparison (where data allow)

### 11.3 Comparison to Alternatives

Model predictions should be distinguishable from:
- "Big Man" aggrandizer models
- Pilgrimage/ritual models
- Trade center models
- Incipient sedentism models

---

## 12. Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Insufficient paleoclimate data | High | Medium | Use stochastic model with sensitivity analysis |
| No access to site files | Medium | Medium | Use published site data from PDFs |
| Model doesn't converge | Low | High | Start with simplified version, add complexity |
| Archaeological data contradicts model | Medium | High | Revise model or interpret as falsification |
| Too similar to Chaco model | Medium | Medium | Emphasize aggregation vs. territorial distinction |

---

## 13. Next Immediate Actions

### This Week (January 15-22, 2026)

1. **Extract key data from PDFs**
   - Radiocarbon dates from Kidder 2002, Ortmann 2007
   - Construction volumes from Ortmann 2007
   - Exotic goods data from available sources

2. **Search paleoclimate databases**
   - NOAA Paleoclimatology for SE North America
   - Document available proxies and resolutions

3. **Integrate environment and simulation modules**
   - Connect `environment.py` to `simulation.py`
   - Run test with full seasonal cycle

4. **Create data extraction templates**
   - CSV format for radiocarbon dates
   - CSV format for exotic goods
   - Spatial data specifications

5. **Review PDFs for key parameters**
   - Population estimates
   - Aggregation duration estimates
   - Travel/mobility patterns

---

## 14. Session Log

### January 15, 2026 - Morning Session
- Created initial plan.md
- Reviewed existing project structure and code
- Identified key gaps (climate data, spatial data, model integration)
- Outlined development phases
- Documented unique aspects of Poverty Point case

### January 15, 2026 - Afternoon Session (ABM Development & Validation)

#### Theoretical Framework
- Created comprehensive theoretical derivation (`docs/THEORETICAL_DERIVATION.md`)
- Derived fitness functions for aggregator vs independent strategies
- Introduced ecotone advantage parameter (ε) as key mechanism
- Derived critical threshold formula: σ* = (R_ind - A) / (R_ind * β - A * α_eff)
- Calibrated parameters to achieve σ* ≈ 0.53 at ε=0.35, n=25

#### ABM Development
- Created modular ABM architecture:
  - `src/poverty_point/parameters.py` - All theoretical parameters
  - `src/poverty_point/agents.py` - Band and AggregationSite classes
  - `src/poverty_point/core_simulation.py` - Main simulation loop
- Implemented annual cycle: shortfall → dispersal → strategy decision → aggregation → mortality → reproduction

#### Phase Space Exploration & Validation
- Created `scripts/exploration/run_phase_space.py` for comprehensive parameter space exploration
- Running 4,290 simulations (13 σ × 11 ε × 30 replicates)
- Found strong correlation (r = 0.978) between theory and ABM

#### Theory-ABM Offset Analysis
- **Key Finding**: Consistent +0.115 offset (ABM threshold higher than theory)
- Sources identified:
  - Emergent n varies with σ (13% of offset)
  - Decision stochasticity (39%)
  - Memory/hysteresis effects (22%)
  - Shortfall timing (17%)
  - Other/unexplained (10%)
- Created comprehensive documentation in `docs/OFFSET_ANALYSIS_FINDINGS.md`

#### Monument Trajectory Analysis
- Created `scripts/figure_generation/monument_trajectories.py`
- Key insight: Monument building shows strong positive feedback (r=0.80-0.96)
- Higher σ → more aggregation → faster cumulative monument growth
- This captures the self-reinforcing nature of Poverty Point's development

#### Population Dynamics Analysis
- Created `scripts/figure_generation/population_dynamics.py`
- Confirmed expected patterns:
  - Higher σ → lower equilibrium population
  - Strategy composition shifts with σ
  - Fitness differential crosses zero near threshold

#### Figures Generated
- `figures/diagnostics/offset_diagnostics.png` - Offset analysis
- `figures/diagnostics/calibration_analysis.png` - Calibration correction
- `figures/diagnostics/monument_trajectories.png` - Cumulative signaling dynamics
- `figures/diagnostics/population_dynamics.png` - Strategy and population dynamics

#### Status
- Comprehensive phase space exploration running (4,290 simulations)
- Theory-ABM relationship well characterized
- Ready to proceed with archaeological pattern validation

---

*This document should be updated regularly as the project progresses.*
