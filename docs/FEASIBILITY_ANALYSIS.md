# Feasibility Analysis: Poverty Point Costly Signaling Model

## Overview

This document assesses the feasibility of applying the costly signaling framework to Poverty Point and identifies key theoretical and empirical challenges.

---

## 1. Archaeological Data Availability

### 1.1 Chronological Control

**Radiocarbon Dating**
- Substantial corpus of dates from Poverty Point and regional sites
- Kidder and colleagues have published comprehensive date compilations
- Bayesian chronological modeling has refined site history
- Key findings: Mound A construction was rapid (possibly months, not generations)

**Ceramic and Artifact Seriation**
- Poverty Point Objects (PPOs) provide relative dating
- Decorative styles allow inter-site correlation
- But coarse resolution compared to tree-ring dating (no dendro available)

**Assessment**: MODERATE - Good enough for broad patterns, not annual resolution like Chaco

### 1.2 Construction Chronology

**Excavation Data**
- Ortmann & Kidder's work provides detailed stratigraphy
- Mound A shows evidence of planned, rapid construction
- Ridge construction sequence less well understood
- Multiple construction episodes identified but not all dated

**Labor Estimates**
- Mound A: ~238,000 m³ earth moved
- Total site: ~750,000+ m³
- Estimates vary: 1-5 million person-hours
- Challenge: Converting to model parameters

**Assessment**: GOOD - Better than many sites, detailed construction data exists

### 1.3 Exotic Goods Distributions

**Material Sources**
| Material | Source Region | Distance | Quantity at PP |
|----------|---------------|----------|----------------|
| Copper | Great Lakes | ~1,600 km | Rare but present |
| Galena | Missouri | ~800 km | Moderate |
| Steatite | Appalachians | ~900 km | Significant |
| Novaculite | Ouachitas | ~250 km | Abundant |
| Crystal quartz | Arkansas | ~300 km | Common |

**Distribution Data**
- Provenience data available from excavations
- Spatial patterns within site documented
- Workshop areas identified
- Inter-site comparisons possible

**Assessment**: GOOD - Extensive documentation of exotic materials

### 1.4 Regional Site Data

**Known Sites**
- Louisiana Division of Archaeology maintains site files
- Survey coverage varies by region
- Many small Poverty Point-period sites documented
- Size distribution data compilable

**Key Sites for Comparison**
1. **Jaketown, MS**: Smaller contemporary site with similar artifacts
2. **Claiborne, MS**: Shell ring site, coastal adaptation
3. **J.W. Copes, LA**: Small mound complex
4. **Numerous extraction sites**: Source-proximate workshops

**Assessment**: MODERATE - Good for major sites, gaps in survey coverage

---

## 2. Paleoclimate Data Availability

### 2.1 Regional Climate Proxies

**Speleothem Records**
- DeSoto Caverns (Alabama): Some coverage of Late Archaic
- Limited resolution for 1700-1100 BCE specifically
- Challenge: Finding proxies at right temporal scale

**Pollen Records**
- Multiple cores from Gulf Coast region
- Lake sediment records exist
- But typically multi-decadal to centennial resolution

**Floodplain Dynamics**
- Kidder has documented Mississippi floodplain changes
- River channel dynamics affect site location/resources
- Geomorphological rather than annual climate data

**Assessment**: WEAK - Much less precise than tree-ring data used for Chaco/Rapa Nui

### 2.2 Alternative Approaches

Instead of annual climate reconstruction, we could model:
1. **Seasonal variability**: Known patterns of resource availability
2. **Inter-annual stochasticity**: Based on modern analogs
3. **Resource patch uncertainty**: Spatial rather than temporal variability

This is actually more appropriate for hunter-gatherers anyway.

---

## 3. Theoretical Adaptations Required

### 3.1 From Agriculture to Foraging

**Rapa Nui/Chaco Model**
- Annual agricultural cycles
- Permanent or semi-permanent settlements
- Territorial groups with defined boundaries
- Environmental σ from crop failure risk

**Poverty Point Adaptation**
- Seasonal resource cycles (fish runs, nut harvests)
- Mobile residential patterns
- Fluid band membership
- Environmental σ from foraging uncertainty

**Key Changes**
```
Agricultural Model:
  Population → Productivity → [Signaling OR Reproduction]

Hunter-Gatherer Model:
  Bands → Foraging Success → [Aggregate OR Disperse]
                                    ↓
                            [Signal Investment]
                                    ↓
                            [Cooperation Benefits]
```

### 3.2 Aggregation Dynamics

**Critical Innovation**
The model must capture fission-fusion dynamics:
- Bands disperse during most of year
- Aggregate seasonally at central location
- Aggregation size varies with expected benefits
- Signaling occurs during aggregation episodes

**Decision Points**
1. **Whether to aggregate**: Cost-benefit calculation
2. **Duration of stay**: How long to remain at aggregation
3. **Investment during aggregation**: Monument labor, exchange
4. **Post-aggregation obligations**: Reciprocal relationships

### 3.3 Cooperation Benefits

Unlike territorial signaling that reduces conflict, aggregation signaling may:
- **Facilitate collective action** (communal fishing, construction)
- **Enable information exchange** (resource locations, technologies)
- **Maintain mating networks** (genetic diversity, alliance formation)
- **Pool risk** through reciprocal obligations

These benefits must offset:
- **Travel costs** to aggregation site
- **Subsistence opportunity costs** during aggregation
- **Disease/conflict risks** from crowding

### 3.4 Monument Function

**In Territorial Model (Rapa Nui/Chaco)**
- Signals group capacity to competitors
- Deters conflict through credible threat
- Stationary because territory is fixed

**In Aggregation Model (Poverty Point)**
- Signals commitment to the aggregation system
- Creates "sunk cost" incentivizing return
- Demonstrates capacity to potential cooperators
- May serve as coordination mechanism ("we build together")

### 3.5 Exotic Goods Function

**Similar to Chaco**
- Individual-level signaling
- Demonstrates capacity/connections
- Creates exchange obligations

**Different from Chaco**
- Not embedded in corporate groups
- More fluid individual networks
- May function more like "advertising" to potential partners

---

## 4. Model Architecture

### 4.1 Proposed Agent Types

**Bands**
- Properties: size, location, resource patch, accumulated prestige
- Actions: forage, move, aggregate, invest, exchange
- State: food stores, social obligations, signal investment history

**Aggregation Sites**
- Properties: location, accumulated infrastructure, current attendees
- Dynamics: size fluctuates with band decisions

**Resource Patches**
- Properties: location, productivity, variability
- Dynamics: seasonal cycles + stochastic variation

### 4.2 Temporal Structure

```
Annual Cycle:
├── Dispersal Season (bands forage independently)
│   ├── Foraging success determined by patch + stochasticity
│   └── Bands accumulate resources, information
│
├── Aggregation Season (bands converge)
│   ├── Arrival decision based on expectations
│   ├── Collective activities (fishing, construction)
│   ├── Signal investment (labor, display)
│   └── Exchange and information sharing
│
└── Dispersal (bands depart with new obligations)
```

### 4.3 Key Parameters

| Parameter | Meaning | Estimated Range |
|-----------|---------|-----------------|
| N_bands | Number of bands in region | 20-100 |
| band_size | Individuals per band | 15-30 |
| travel_cost | Energy cost per km | Based on ethnography |
| aggregation_benefit | Returns to cooperation | To be estimated |
| signal_cost | Labor diverted from foraging | ~10-30% |
| patch_variability | Resource uncertainty (σ) | To be calibrated |

### 4.4 Fitness Calculation

For band i:
```
W_i = foraging_success
    + aggregation_benefits * attendance
    - travel_costs * distance
    - signal_costs * investment
    + reciprocal_returns * obligations
```

Signaling becomes adaptive when:
```
aggregation_benefits + reciprocal_returns > travel_costs + signal_costs
```

This depends on:
- How many other bands aggregate (network effects)
- Reliability of reciprocal relationships
- Resource uncertainty making pooling valuable

---

## 5. Testable Predictions

### 5.1 Site Location
**Prediction**: Poverty Point should be optimally located for:
- Minimizing aggregate travel distances across bands
- Maximizing resource concentration for supporting aggregation
- Central position in exchange network

**Test**: Compare actual location to optimal location models

### 5.2 Construction Intensity
**Prediction**: Monument investment should correlate with:
- Number of participating bands (more bands → more labor)
- Resource uncertainty (higher σ → more signaling)
- Expected aggregation benefits (more cooperation → more investment)

**Test**: Compare construction phases to regional site densities and climate proxies

### 5.3 Exotic Goods Distribution
**Prediction**: Exotic goods should:
- Concentrate at aggregation sites
- Show individual variation in quantities
- Come from diverse directions (wide network)
- Increase during periods of high aggregation

**Test**: Compare exotic distributions across site types and through time

### 5.4 Regional Site Hierarchy
**Prediction**: Site size distribution should show:
- Strong primacy (one dominant site)
- Secondary sites at network nodes
- Many small extraction/foraging camps

**Test**: Compare predicted to observed site size distributions

### 5.5 Collapse Pattern
**Prediction**: System collapse should occur when:
- Resource uncertainty drops (less need for cooperation)
- Travel costs increase relative to benefits
- Alternative aggregation options emerge
- Environmental change makes location suboptimal

**Test**: Examine conditions at ~1100 BCE when site was abandoned

---

## 6. Comparison with Alternative Explanations

### 6.1 "Big Man" Models
**Claim**: Aggrandizing individuals mobilized labor for prestige
**Problem**: Doesn't explain why others participated; assumes coercion or deference
**Our model**: Signaling provides adaptive benefits to participants, not just leaders

### 6.2 Pilgrimage Models
**Claim**: Religious motivation drew people to sacred center
**Problem**: Descriptive, doesn't explain why this location or why signaling adaptive
**Our model**: "Pilgrimage" is the aggregation, but function is cooperation not just ritual

### 6.3 Sedentism Models
**Claim**: Poverty Point represents incipient sedentism
**Problem**: Artifact distributions suggest continued mobility for most participants
**Our model**: Seasonal aggregation, not permanent settlement

### 6.4 Trade Center Models
**Claim**: Site functioned primarily as exchange hub
**Problem**: Exchange alone doesn't require monumental construction
**Our model**: Exchange is one benefit of aggregation; monuments signal commitment

---

## 7. Implementation Plan

### Phase 1: Data Compilation
1. Compile radiocarbon dates from published sources
2. Extract construction chronology from Ortmann/Kidder
3. Document exotic goods distributions
4. Gather regional site data

### Phase 2: Model Development
1. Adapt Chaco model framework for aggregation dynamics
2. Implement fission-fusion band movement
3. Add cooperation benefit calculations
4. Calibrate parameters to ethnographic ranges

### Phase 3: Analysis
1. Run replicate simulations across scenarios
2. Compare predictions to archaeological record
3. Sensitivity analysis on key parameters
4. Statistical validation with confidence intervals

### Phase 4: Manuscript
1. Write theoretical framework section
2. Present model results
3. Compare with archaeological data
4. Discuss implications

---

## 8. Key Challenges

### 8.1 Calibration
Unlike Chaco (with tree-ring dating) or Rapa Nui (with well-documented population), Poverty Point lacks:
- Annual-resolution chronology
- Population estimates at specific times
- Quantified resource productivity

**Solution**: Broader parameter ranges, sensitivity analysis, qualitative pattern matching

### 8.2 Aggregation Dynamics
Modeling fission-fusion is computationally more complex than territorial groups:
- Variable group sizes
- Dynamic social networks
- Non-linear returns to aggregation size

**Solution**: Agent-based model with emergent aggregation patterns

### 8.3 Multi-Century Time Depth
Poverty Point spans ~600 years - longer than Chaco or Rapa Nui:
- System may have changed significantly over time
- Multiple construction phases suggest evolution
- Climate and resources likely shifted

**Solution**: Model regime transitions, not just equilibrium

---

## 9. Verdict: FEASIBLE WITH MODIFICATIONS

The project is feasible but requires:
1. **Modified theoretical framework**: Aggregation dynamics, not territorial signaling
2. **Different data resolution**: Pattern-matching rather than correlation testing
3. **New model mechanics**: Fission-fusion dynamics, cooperation benefits
4. **Broader uncertainty ranges**: Reflect less precise chronological control

The case is actually theoretically compelling because:
- Hunter-gatherer monumentality is genuinely puzzling
- Aggregation-based signaling is understudied
- The framework makes specific, testable predictions
- Alternative explanations are less satisfying

---

## 10. Next Steps

1. **Search for paleoclimate proxies** covering 2000-1000 BCE in the region
2. **Compile radiocarbon database** for Poverty Point and regional sites
3. **Design model architecture** for aggregation dynamics
4. **Write theoretical framework** section of manuscript
5. **Create initial figures** showing site and regional context
