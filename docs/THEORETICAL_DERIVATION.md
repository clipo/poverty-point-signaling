# Theoretical Derivation: Multilevel Selection and Aggregation-Based Costly Signaling

## 1. Starting Point: The Modified Price Equation

From the Rapa Nui/Chaco framework, we have the Price equation for multilevel selection with environmental uncertainty:

$$\Delta\bar{p} = \frac{Cov(w_g(\sigma), p_g)}{\bar{w}(\sigma)} + \frac{E(w_g(\sigma) \Delta p_g)}{\bar{w}(\sigma)}$$

Where:
- $p_g$ = frequency of costly signaling trait in group g
- $w_g(\sigma)$ = fitness of group g as a function of environmental uncertainty
- $\sigma$ = environmental uncertainty parameter
- First term = between-group selection (favors signaling under high σ)
- Second term = within-group selection (opposes signaling due to individual costs)

**Key insight**: Costly signaling becomes adaptive when between-group selection is strong enough to overcome within-group costs. This occurs above a critical threshold σ*.

---

## 2. The Rapa Nui/Chaco Model: Territorial Signaling

In the territorial model, groups are **fixed in space** and compete for territory:

### 2.1 Strategy Contrast

| Strategy | Resource Allocation | Mechanism |
|----------|-------------------|-----------|
| Monument Building | 35% to monuments, 65% to reproduction | Signal deters competitors, reduces conflict |
| High Reproduction | 100% to reproduction | Maximize population growth |

### 2.2 Fitness Components

**Monument Builders:**
$$W_{signal}(\sigma) = (1 - C)(1 - \alpha \cdot \sigma)(1 - m_0(1-r))$$

**High Reproduction:**
$$W_{non-signal}(\sigma) = (1 - \beta \cdot \sigma)(1 - m_0)$$

Where:
- C = cost of signaling (0.35)
- α = shortfall vulnerability for signalers (~0.30)
- β = shortfall vulnerability for non-signalers (~0.90)
- m₀ = baseline conflict mortality
- r = conflict reduction from signaling (~0.75)

### 2.3 Critical Threshold

$$\sigma^* \approx \frac{C}{\beta - (1-C)\alpha}$$

With typical values: **σ* ≈ 0.50**

---

## 3. Adapting for Poverty Point: Aggregation Dynamics

The Poverty Point case differs fundamentally from territorial signaling. Instead of **fixed groups competing for territory**, we have **mobile bands deciding whether to aggregate**.

### 3.1 The Fundamental Difference

| Dimension | Territorial Model | Aggregation Model |
|-----------|------------------|-------------------|
| Social unit | Fixed corporate groups | Fluid band networks |
| Spatial dynamics | Compete for territory | Gather/disperse seasonally |
| Signal target | Competitor deterrence | Cooperation facilitation |
| Signal function | "We can defend this" | "We will cooperate reliably" |
| Benefit mechanism | Reduced conflict mortality | Enhanced cooperation returns |
| Cost structure | Continuous investment | Episodic investment during aggregation |

### 3.2 New Strategy Contrast

For Poverty Point, the competing strategies are:

| Strategy | Behavior | Resource Allocation |
|----------|----------|-------------------|
| **Aggregator** | Travels to central site, invests in monuments/exchange | Travel costs + signal costs during aggregation |
| **Independent** | Remains dispersed, avoids aggregation costs | 100% to local foraging/reproduction |

---

## 4. Theoretical Framework for Aggregation-Based Signaling

### 4.1 The Aggregation Decision

A band's decision to aggregate depends on expected net benefits:

$$E[B_{aggregate}] = B_{coop} + B_{info} + B_{risk} + B_{mate} - C_{travel} - C_{signal} - C_{opportunity}$$

Where:
- $B_{coop}$ = benefits from collective activities (fishing, construction labor pooling)
- $B_{info}$ = value of information exchange about resource patches
- $B_{risk}$ = risk pooling through reciprocal obligations
- $B_{mate}$ = mating network maintenance (genetic diversity, alliance formation)
- $C_{travel}$ = energy/time cost of traveling to aggregation site
- $C_{signal}$ = monument investment and exotic goods acquisition during aggregation
- $C_{opportunity}$ = foregone foraging during time at aggregation

### 4.2 Why Costly Signaling at Aggregation?

The puzzle: why invest in monuments and exotics rather than just aggregate?

**Answer**: Signaling solves coordination and commitment problems inherent in aggregation:

1. **Commitment signal**: "I have sunk costs here; I will return"
2. **Capacity signal**: "I can afford this cost; I am a reliable partner"
3. **Coordination mechanism**: "We build together" creates shared identity
4. **Obligation creation**: Exotic exchange creates reciprocal ties

Without signaling, aggregation faces free-rider problems:
- Bands could extract benefits (information, mating) without contributing
- No mechanism to identify reliable cooperation partners
- No "sunk cost" creating return incentives

---

## 5. Modified Fitness Functions for Aggregation

### 5.1 Aggregator Strategy Fitness

$$W_{aggregator}(\sigma, n) = (1 - C_{travel} - C_{signal})(1 - \alpha_{agg} \cdot \sigma) \cdot f(n) \cdot (1 + B_{recip})$$

Where:
- $C_{travel}$ = travel cost (function of distance to aggregation site)
- $C_{signal}$ = signaling cost at aggregation (monument + exotics)
- $\alpha_{agg}$ = shortfall vulnerability for aggregators (LOWER due to multi-zone access, risk pooling)
- $f(n)$ = cooperation benefits as function of aggregation size n
- $B_{recip}$ = benefits from reciprocal obligations activated during dispersal

### 5.2 Independent Strategy Fitness

$$W_{independent}(\sigma) = (1 - \beta_{ind} \cdot \sigma)$$

Where:
- $\beta_{ind}$ = shortfall vulnerability for independents (HIGHER due to single-zone dependence, no risk pooling)

### 5.3 Key Insight: Vulnerability Asymmetry

**In the territorial model**:
- Vulnerability difference comes from population density (signalers below K, non-signalers at K)

**In the aggregation model**:
- Vulnerability difference comes from **ecological access** and **risk pooling**
- Aggregators at ecotone have multi-zone buffering
- Aggregators have reciprocal obligations to call upon during shortfalls
- Independents depend on single zone, face shortfalls alone

---

## 6. The Ecotone Advantage: A New Mechanism

### 6.1 Multi-Zone Buffering

Poverty Point sits at the intersection of multiple ecological zones:
- Aquatic (Mississippi/Bayou Macon): fish, waterfowl, turtles
- Terrestrial (uplands): deer, small game
- Mast (hardwood forests): pecans, hickory, walnuts
- Wetland margins: diverse resources

**Covariance structure matters**: When zones have **negative covariance** in productivity, the ecotone provides buffering:

$$Var(P_{ecotone}) = Var(P_1) + Var(P_2) + 2 \cdot Cov(P_1, P_2)$$

If $Cov(P_1, P_2) < 0$: ecotone variance is LOWER than single-zone variance.

### 6.2 Ecotone Advantage Parameter (ε)

Define ε as the proportional reduction in effective environmental uncertainty at the ecotone:

$$\sigma_{ecotone} = \sigma_{regional} \cdot (1 - \varepsilon)$$

Where ε depends on:
- Number of accessible zones (more zones = more buffering)
- Covariance structure between zones
- Relative productivity of each zone

**Estimated range**: ε ∈ [0.2, 0.5] (20-50% uncertainty reduction at multi-zone ecotone)

### 6.3 Implications for Aggregation

The ecotone advantage creates a **spatial attractor** for aggregation:
- Aggregation at ecotone locations reduces effective σ experienced by participants
- This extends feasible aggregation duration (can stay longer without starvation)
- Creates primacy for sites with maximum ecotone access

---

## 7. Cooperation Benefits Function

### 7.1 Returns to Scale

Aggregation benefits should show:
- Increasing returns at small n (more partners = more cooperation opportunities)
- Diminishing returns at large n (coordination costs, crowding, disease)

Functional form:

$$f(n) = 1 + b \cdot \log(n) - c \cdot (n - n^*)^2 \cdot \mathbb{1}_{n > n^*}$$

Where:
- b = benefit coefficient (how much cooperation helps)
- c = crowding cost coefficient
- n* = optimal aggregation size before crowding costs kick in

### 7.2 Estimating b (Cooperation Benefits)

Sources of aggregation benefits:

| Benefit Type | Mechanism | Estimated Value |
|--------------|-----------|-----------------|
| Collective fishing | Fish weirs require multiple people | 20-40% productivity boost |
| Information exchange | Knowledge of productive patches | 10-20% search cost reduction |
| Risk pooling | Obligations activated during shortfall | 15-30% mortality reduction |
| Mating networks | Genetic diversity, alliance formation | Long-term fitness effects |

**Composite estimate**: b ≈ 0.3-0.5 (aggregation of n=20 bands provides ~1.9-2.5× baseline productivity)

### 7.3 The Crowding Threshold (n*)

At some point, aggregation becomes costly:
- Resource depletion near site
- Disease transmission
- Social conflict
- Coordination breakdown

**Estimated n***: 20-40 bands (500-1,000 individuals) based on:
- Hunter-gatherer aggregation ethnography
- Poverty Point site carrying capacity estimates
- Archaeological evidence of periodic gatherings

---

## 8. Reciprocal Obligations: The Dispersal Benefit

### 8.1 The Problem of Dispersal

A key puzzle: why do aggregation benefits persist after dispersal?

**Answer**: Signaling during aggregation creates **reciprocal obligations** that provide benefits during dispersal:

- Monument contributions demonstrate commitment to the system
- Exotic goods exchange creates dyadic obligations
- These obligations can be "called in" during dispersal-season shortfalls

### 8.2 Obligation Value Function

$$B_{recip} = \sum_{j \in obligations} p_{call}(j) \cdot V_{help}(j) \cdot d_{trust}(j)$$

Where:
- $p_{call}(j)$ = probability of needing to call on partner j (function of σ)
- $V_{help}(j)$ = value of help from partner j (function of their resources)
- $d_{trust}(j)$ = reliability of partner j (function of their signal investment)

**Key insight**: Higher signaling investment increases d_trust, making reciprocal relationships more valuable.

---

## 9. Modified Critical Threshold for Aggregation

### 9.1 Derivation

Setting $W_{aggregator} = W_{independent}$ and solving for σ:

$$(1 - C_{total})(1 - \alpha_{agg} \cdot \sigma) \cdot f(n) \cdot (1 + B_{recip}) = (1 - \beta_{ind} \cdot \sigma)$$

Where $C_{total} = C_{travel} + C_{signal}$

Simplifying (assuming f(n) and B_recip are at equilibrium values):

$$\sigma^*_{agg} \approx \frac{C_{total} - (f(n)(1+B_{recip}) - 1)}{\beta_{ind} - \alpha_{agg} \cdot f(n)(1+B_{recip})(1-C_{total})}$$

### 9.2 Key Differences from Territorial Model

1. **Cost structure differs**: Travel costs depend on distance; signal costs are episodic
2. **Benefit structure differs**: Cooperation benefits (f(n)) are explicit; conflict reduction is implicit
3. **Vulnerability asymmetry source differs**: Ecotone access vs. population density
4. **Threshold depends on aggregation size n**: Creates feedback loop

### 9.3 Estimated Critical Threshold

With estimated parameters:
- C_total ≈ 0.25-0.35 (travel + signal)
- α_agg ≈ 0.25-0.35 (buffered by ecotone + risk pooling)
- β_ind ≈ 0.70-0.85 (single-zone, no pooling)
- f(n) ≈ 1.5-2.0 (at n = 20-30 bands)
- B_recip ≈ 0.1-0.2

**Estimated σ*_agg ≈ 0.35-0.50**

This is potentially LOWER than the territorial model σ*, meaning aggregation-based signaling may emerge under milder uncertainty conditions than territorial signaling.

---

## 10. Theoretical Predictions

### 10.1 Phase Space Predictions

**Region 1: High σ, Good Ecotone Access (ε high)**
- Aggregation with signaling dominates
- Monument investment scales with aggregation size
- Exotic goods concentrate at aggregation site
- Expected at Poverty Point

**Region 2: High σ, Poor Ecotone Access (ε low)**
- Aggregation may occur but unstable (can't sustain long gatherings)
- Smaller aggregation sites, less monument investment
- Expected at secondary sites (Jaketown, Claiborne)

**Region 3: Low σ, Any Ecotone**
- Independent strategy dominates (aggregation costs not justified)
- Minimal monument investment
- Dispersed settlement pattern

**Region 4: Moderate σ, Good Ecotone**
- Bistable: either strategy can dominate depending on initial conditions
- May explain temporal variation in aggregation intensity

### 10.2 Spatial Predictions

1. **Primacy**: The site with maximum ecotone access (multi-zone buffering) should become the regional aggregation center
2. **Hierarchy**: Secondary sites at intermediate ecotone positions
3. **Distance decay**: Participation declines with distance from center (travel costs)
4. **Source proximity**: Exotic goods should come from multiple directions (wide network)

### 10.3 Temporal Predictions

1. **Seasonality**: Aggregation should coincide with resource peaks at ecotone (late summer/fall?)
2. **Construction pulses**: Monument investment concentrated during aggregation seasons
3. **Exotic accumulation**: Gradual increase as network stabilizes
4. **Collapse conditions**: System fails if σ drops OR ecotone advantage declines OR alternative sites emerge

### 10.4 Individual-Level Predictions

1. **Exotic goods variation**: Individual bands should show variation in exotic holdings (individual signals)
2. **Contribution variation**: Bands should vary in monument contributions (based on surplus and strategy)
3. **Network structure**: Reciprocal obligations should create non-random social network

---

## 11. Testable Hypotheses

### H1: Ecotone Optimality
Poverty Point location should be demonstrably optimal for multi-zone access compared to alternative locations.

**Test**: Calculate ecotone index for PP vs. Jaketown, Claiborne, other locations.

### H2: Construction-Uncertainty Correlation
Monument investment should increase during periods of higher environmental uncertainty.

**Test**: Compare construction chronology to paleoclimate proxies (if available).

### H3: Exotic Goods Concentration
Exotic materials should be disproportionately concentrated at aggregation sites vs. dispersal camps.

**Test**: Compare exotic density at PP vs. small camps in the region.

### H4: Distance Decay
Site size/complexity should decline with distance from the ecotone optimum.

**Test**: Regress site size on distance from PP and ecotone access index.

### H5: Collapse Conditions
System abandonment should correlate with:
- Declining environmental uncertainty (climate stabilization)
- Ecotone shift (river channel changes)
- Alternative site emergence

**Test**: Examine conditions at ~1100 BCE.

---

## 12. Model Parameters to Explore

### 12.1 Environmental Parameters

| Parameter | Symbol | Range | Notes |
|-----------|--------|-------|-------|
| Regional uncertainty | σ | 0.2-0.8 | Composite of frequency, magnitude, duration |
| Ecotone buffering | ε | 0.0-0.6 | Multi-zone variance reduction |
| Zone covariance | ρ_ij | -0.5 to +0.5 | Negative = buffering |
| Seasonal amplitude | s | 0.3-0.7 | Productivity variation within year |

### 12.2 Cost Parameters

| Parameter | Symbol | Range | Notes |
|-----------|--------|-------|-------|
| Travel cost rate | c_t | 0.001-0.01 | Per km energy cost |
| Signal cost rate | c_s | 0.10-0.30 | Fraction of surplus to monuments |
| Exotic acquisition cost | c_e | 0.05-0.20 | Cost per exotic item |
| Aggregation opportunity cost | c_o | 0.10-0.25 | Foregone foraging |

### 12.3 Benefit Parameters

| Parameter | Symbol | Range | Notes |
|-----------|--------|-------|-------|
| Cooperation coefficient | b | 0.2-0.6 | Returns to aggregation size |
| Crowding threshold | n* | 15-40 | Bands before crowding costs |
| Crowding cost rate | c_c | 0.01-0.05 | Per-band crowding penalty |
| Reciprocal benefit rate | r | 0.05-0.25 | Value of obligations during dispersal |

### 12.4 Vulnerability Parameters

| Parameter | Symbol | Range | Notes |
|-----------|--------|-------|-------|
| Aggregator vulnerability | α | 0.20-0.40 | Buffered by ecotone + pooling |
| Independent vulnerability | β | 0.60-0.90 | Single-zone, no pooling |

---

## 13. Predictions for ABM Development

Based on this theoretical derivation, the ABM should demonstrate:

1. **Emergence of aggregation** when σ > σ*_agg and ε > ε_min
2. **Primacy of ecotone sites** through competitive exclusion of non-ecotone aggregations
3. **Scaling of monument investment** with aggregation size and σ
4. **Exotic goods concentration** at aggregation sites
5. **Collapse** under parameter shifts (declining σ, reduced ε, increased travel costs)
6. **Bistability** in transition zones of parameter space

The ABM should explore the full phase space to identify:
- Where aggregation-based signaling emerges
- How sensitive the system is to each parameter
- What conditions produce Poverty Point-like patterns
- What conditions produce collapse

---

## 14. Summary: Poverty Point as Aggregation-Based Costly Signaling

The theoretical framework predicts that Poverty Point represents an adaptive system where:

1. **Environmental uncertainty** (σ) created conditions favoring cooperation
2. **Ecotone location** (ε) reduced effective uncertainty and enabled extended aggregation
3. **Costly signaling** (monuments + exotics) solved commitment and coordination problems
4. **Cooperation benefits** (f(n)) justified aggregation costs
5. **Reciprocal obligations** extended benefits into dispersal season

This differs from territorial signaling (Rapa Nui/Chaco) by:
- Emphasizing **aggregation dynamics** over territorial competition
- Adding **ecotone advantage** as a spatial attractor
- Modeling **cooperation benefits** explicitly rather than conflict reduction
- Including **reciprocal obligations** that persist beyond aggregation

The framework generates testable predictions about site location, construction chronology, exotic distributions, regional hierarchy, and collapse conditions.

---

*Next step: Design ABM architecture to explore this phase space systematically.*
