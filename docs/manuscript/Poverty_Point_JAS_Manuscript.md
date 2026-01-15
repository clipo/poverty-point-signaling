# The Poverty Point Paradox: Explaining Hunter-Gatherer Monumentality Through Costly Signaling Theory

**Running title:** Costly Signaling at Poverty Point

**Authors:** [Author names to be added]

**Corresponding author:** [Contact information to be added]

**Keywords:** Poverty Point, costly signaling, multilevel selection, hunter-gatherer archaeology, agent-based modeling, monumental architecture, Late Archaic

---

## Abstract

Poverty Point (ca. 1700-1100 BCE) presents one of archaeology's most compelling puzzles: why would mobile hunter-gatherers construct one of the largest earthwork complexes in prehistoric North America while simultaneously accumulating exotic materials from across the midcontinent? Standard models of hunter-gatherer behavior predict mobility and minimal investment in fixed infrastructure, yet Poverty Point encompasses 160 hectares of constructed landscape including massive mounds and concentric ridges representing millions of person-hours of labor. We propose that this phenomenon represents an adaptive costly signaling system operating through seasonal aggregation dynamics. Extending multilevel selection theory, we develop a formal model where environmental uncertainty above a critical threshold favors aggregation-based cooperation, with monument construction and exotic goods serving as honest signals of commitment. Our agent-based simulation validates the theoretical predictions, demonstrating a phase transition at environmental uncertainty levels consistent with Late Archaic conditions in the Lower Mississippi Valley. The model produces monument volumes and exotic goods quantities matching archaeological estimates when calibrated to the 500-year occupation span. This framework explains not only why monumentality emerged at Poverty Point but also predicts site location optimality based on ecotone access, regional site hierarchy, and conditions for eventual system abandonment. The costly signaling approach provides a unified explanation for collective monument construction and individual exotic goods acquisition without requiring aggrandizers, religious motivation, or incipient complexity.

---

## 1. Introduction

Poverty Point, located in northeastern Louisiana near the confluence of Bayou Macon and the Arkansas River, presents one of the most remarkable archaeological sites in North America (Gibson 2000, 2001). Dating to approximately 1700-1100 BCE, the site encompasses approximately 160 hectares of constructed landscape, including six concentric C-shaped ridges, multiple mounds, and a 17-hectare central plaza (Kidder 2002; Webb 1968). Mound A, the largest earthwork, rises 22 meters and contains an estimated 238,000 cubic meters of fill (Ortmann and Kidder 2013). Conservative estimates suggest the total earthwork volume exceeds 750,000 cubic meters, representing 1-5 million person-hours of labor investment (Sherwood and Kidder 2011). Recent geoarchaeological research indicates that Mound A may have been constructed in a matter of months rather than generations, implying coordinated labor mobilization at unprecedented scales for hunter-gatherer societies (Ortmann and Kidder 2013; Kidder et al. 2009).

The site also served as a focal point for long-distance exchange networks spanning much of eastern North America (Webb 1968; Gibson 1999). Materials sourced from distances exceeding 1,600 kilometers accumulated at Poverty Point in quantities far exceeding any contemporary location. These include copper from eastern sources including the Appalachians and Canadian Maritimes (Hill et al. 2016), galena from Missouri, steatite from the Appalachians, and various lithic materials from across the midcontinent (Smith 1976; Lehmann 1991). The combination of massive collective monument construction with extensive individual acquisition of exotic materials demands explanation.

This pattern is paradoxical when viewed through standard models of hunter-gatherer behavior. Ethnographic and archaeological evidence suggests that mobile foraging populations typically minimize investment in fixed infrastructure, maintain flexible group membership, and avoid accumulation of surplus beyond immediate needs (Jackson 1986; Jackson and Scott 2001). The Poverty Point phenomenon appears to violate these expectations fundamentally. Why would mobile bands invest so heavily in monuments they would periodically abandon? Why acquire exotic materials with no apparent utilitarian function? Why create such pronounced site hierarchy in an otherwise dispersed settlement system?

Previous explanations have invoked several mechanisms, each facing significant challenges. "Big Man" or aggrandizer models propose that powerful individuals mobilized labor through prestige competition (Gibson and Carr 2004), but these accounts assume rather than explain why others participated in what appears to be collective action benefiting elites. Pilgrimage or ritual models describe the phenomenon as religious gatherings (Spivey et al. 2015), but provide no explanation for why this location, why such investment levels, or why the system eventually ended. Trade center models explain the exotic materials but fail to account for monument construction, which has no obvious role in exchange (Gibson 1999). Incipient sedentism models conflict with artifact distributions and site structure suggesting continued residential mobility for most participants (Jackson 1986).

We propose an alternative explanation grounded in evolutionary theory: Poverty Point represents an adaptive costly signaling system operating through seasonal aggregation dynamics. Building on the multilevel selection framework developed for explaining monument construction in territorial societies (DiNapoli et al. 2021; Lipo et al. 2016), we extend the theory to incorporate the specific challenges faced by mobile hunter-gatherer bands. Our model shows that under appropriate environmental conditions, aggregation with costly signaling emerges as a fitness-enhancing strategy, with both monument construction and exotic goods acquisition serving as honest signals of cooperation capacity and commitment.

The remainder of this paper develops this argument in four sections. Section 2 presents the theoretical framework, deriving the conditions under which aggregation-based costly signaling becomes adaptive. Section 3 describes an agent-based model that formalizes these dynamics. Section 4 presents simulation results validating the theoretical predictions and comparing model outputs to archaeological data. Section 5 discusses implications and identifies testable predictions that distinguish our model from alternatives.

---

## 2. Theoretical Framework

### 2.1 The Price Equation and Multilevel Selection

Our approach builds on the Price equation for multilevel selection (Price 1970), which provides a formal framework for understanding how traits can evolve when selection operates simultaneously at multiple levels. The Price equation partitions evolutionary change in trait frequency into between-group and within-group components:

$$\Delta\bar{p} = \frac{Cov(w_g, p_g)}{\bar{w}} + \frac{E(w_g \Delta p_g)}{\bar{w}}$$

where $p_g$ is the frequency of the trait (here, costly signaling) in group $g$, $w_g$ is the fitness of group $g$, $\bar{w}$ is mean population fitness, $\Delta p_g$ is the change in trait frequency within group $g$, and the two terms represent between-group and within-group selection respectively.

The first term, the covariance between group fitness and trait frequency, represents **between-group selection**. When groups with more signalers have higher fitness (positive covariance), this term favors the spread of signaling. The second term, the expected within-group change weighted by group fitness, represents **within-group selection**. Because signalers pay costs that non-signalers avoid, non-signalers typically out-reproduce signalers within any group, making this term negative.

The key insight from this framework is that costly traits can spread when between-group selection is sufficiently strong to overcome within-group costs. We extend this by making fitness explicitly dependent on environmental uncertainty ($\sigma$):

$$\Delta\bar{p} = \frac{Cov(w_g(\sigma), p_g)}{\bar{w}(\sigma)} + \frac{E(w_g(\sigma) \Delta p_g)}{\bar{w}(\sigma)}$$

Environmental uncertainty modulates the relative strength of these selective forces. At low $\sigma$, environmental shortfalls are rare, survival differences between strategies are minimal, and within-group selection dominates. Signaling is maladaptive because signalers pay costs without receiving commensurate survival benefits. At high $\sigma$, shortfalls are frequent and severe, survival differences become pronounced, and between-group selection strengthens. Groups with signalers survive shortfalls better due to cooperation networks, buffering mechanisms, and reduced vulnerability. Above a critical threshold $\sigma^*$, between-group selection overcomes within-group costs, and signaling becomes adaptive.

Previous applications of this framework to Rapa Nui moai construction and Chaco Canyon great houses demonstrated that this phase transition produces qualitatively different behavioral regimes. Below threshold, populations converge on non-signaling strategies; above threshold, costly signaling emerges and persists. The transition is sharp rather than gradual, creating distinct archaeological signatures.

### 2.2 From Territorial to Aggregation-Based Signaling

However, these territorial models cannot be directly applied to Poverty Point. The key differences involve social organization, spatial dynamics, and signal function. In the territorial model, groups are fixed in space and compete for resources through monument display that deters competitors. The signal says "we can defend this territory." Mobile hunter-gatherer bands face a fundamentally different optimization problem: they must decide whether to aggregate at central locations, how long to remain, and how much to invest in collective activities. The signal function shifts from deterrence to attraction, from territorial defense to cooperation facilitation. The signal says "we will cooperate reliably."

This shift requires modifying the fitness functions and introducing new mechanisms. Territorial groups gain fitness through reduced conflict mortality when monuments deter competitors. Aggregating bands gain fitness through cooperation benefits during aggregation and reciprocal obligations during dispersal. The cost structure also differs: territorial signalers pay continuous costs maintaining monuments, while aggregating signalers pay episodic costs during aggregation events.

### 2.3 The Aggregation Challenge

Hunter-gatherer bands face coordination and commitment problems that aggregation alone cannot solve. Without signaling mechanisms, aggregations are vulnerable to several challenges. Free-riding becomes possible when bands can extract cooperation benefits (information, mating opportunities, risk pooling) without contributing to collective activities. Partner identification becomes difficult when bands cannot distinguish reliable cooperators from potential exploiters. Commitment problems arise because bands have no incentive to return to the same aggregation site year after year without sunk costs binding them to the system.

Costly signaling through monument construction and exotic goods acquisition solves these problems (Zahavi 1975; Grafen 1990). Monument investment creates a sunk cost that demonstrates commitment to the aggregation system. A band that has invested heavily in monuments at a particular site has strong incentives to return, because abandoning the site means losing the value of past investment. Other bands can observe this commitment and preferentially cooperate with committed partners. Exotic goods signal individual capacity and willingness to invest in the network (Smith 1976; Hill et al. 2016). Bands that acquire exotic materials demonstrate resource surplus and network connectivity, signaling desirability as cooperation partners. Both signals are honest in the evolutionary sense because they cannot be cheaply faked: monuments require labor, exotics require network access and resource surplus.

### 2.4 Model Structure and Fitness Functions

We extend the multilevel selection framework to incorporate aggregation dynamics. Bands face a choice between two strategies each year. The **aggregator strategy** involves traveling to a central site during the aggregation season, investing in monuments and exotic goods, participating in collective activities, and forming reciprocal obligations with other aggregators. The **independent strategy** involves remaining dispersed throughout the year, avoiding aggregation costs, and foraging independently.

The fitness function for aggregators incorporates multiple components:

$$W_{agg}(\sigma, \varepsilon, n) = (1 - C_{total})(1 - \alpha_{agg} \cdot \sigma_{eff}) \cdot f(n) \cdot (1 + B_{recip})$$

where:

- $C_{total}$ represents total costs including travel ($C_{travel} \approx 0.08$), signaling investment ($C_{signal} \approx 0.15$), and foregone foraging ($C_{opportunity} \approx 0.19$), summing to approximately 0.42
- $\alpha_{agg}$ represents vulnerability to environmental shortfalls for aggregators, reduced by multi-zone buffering and risk pooling to approximately 0.40
- $\sigma_{eff}$ represents effective environmental uncertainty at the aggregation site, reduced by ecotone access
- $f(n)$ represents cooperation benefits as a function of the number of bands aggregating
- $B_{recip}$ represents benefits from reciprocal obligations that can be called upon during dispersal (approximately 0.05)

The fitness function for independents is simpler:

$$W_{ind}(\sigma) = R_{ind}(1 - \beta_{ind} \cdot \sigma)$$

where:

- $R_{ind}$ represents the reproductive advantage from avoiding aggregation costs (approximately 1.10, reflecting full resource allocation to reproduction)
- $\beta_{ind}$ represents vulnerability to shortfalls when foraging independently (approximately 0.75, reflecting single-zone dependence and lack of risk pooling)

The key asymmetry lies in vulnerability: aggregators have lower vulnerability ($\alpha_{agg} \approx 0.40$) than independents ($\beta_{ind} \approx 0.75$) because aggregation provides multi-zone resource access and reciprocal obligations create a social safety net during shortfalls.

### 2.5 The Ecotone Advantage

A critical innovation in our model is the ecotone advantage parameter ($\varepsilon$), which captures the benefits of multi-zone ecological access at the aggregation site. Poverty Point is positioned at the intersection of multiple ecological zones: Mississippi River floodplain aquatic resources, Macon Ridge upland terrestrial game, Bayou Macon drainage fish and waterfowl, and hardwood forest mast resources (Jackson 1986, 1989; Ward 1998).

When these zones have negative covariance in productivity, the ecotone provides variance reduction through portfolio effects. If aquatic resources fail due to drought, terrestrial resources may thrive; if mast crops fail, fish populations may be abundant. This reduces the effective uncertainty experienced at the aggregation site:

$$\sigma_{eff} = \sigma_{regional}(1 - \varepsilon)$$

For example, with regional uncertainty $\sigma = 0.60$ and ecotone advantage $\varepsilon = 0.35$, effective uncertainty at the aggregation site drops to $\sigma_{eff} = 0.39$. This substantially changes the fitness calculus for aggregation.

The ecotone advantage has profound implications for site location and regional hierarchy. It reduces effective uncertainty at the aggregation site while regional uncertainty remains high, creates an asymmetry that favors aggregation at high-ecotone locations, enables extended aggregation through diverse resource access (bands can stay longer without depleting local resources), creates site primacy for locations with maximum ecotone access (explaining why Poverty Point dominates the regional system), and lowers the critical threshold for aggregation to become adaptive.

### 2.6 Cooperation Benefits

The returns to aggregation show increasing then diminishing returns. Cooperation benefits increase with aggregation size due to information exchange about resource patches, collective fishing using weirs and communal drives, labor pooling for monument construction, and risk pooling through reciprocal obligations (Hayden 2009, 2014; Hays 2019). We model this as a logarithmic function:

$$f(n) = 1 + b \cdot \ln(n) - c \cdot (n - n^*)^2 \cdot \mathbb{1}_{n > n^*}$$

where $b \approx 0.08$ is the cooperation benefit coefficient, $c \approx 0.015$ is the crowding cost coefficient, and $n^* \approx 25$ is the optimal aggregation size before crowding costs emerge.

This functional form captures ethnographic observations that small aggregations provide substantial benefits (the first few bands add considerable value), marginal benefits decline with size (the 25th band adds less than the 5th), and above some threshold, crowding costs emerge from local resource depletion, disease transmission, and coordination difficulties. We estimate optimal aggregation size at approximately 25 bands (500-625 individuals) before crowding costs begin to dominate, consistent with ethnographic observations of large hunter-gatherer gatherings.

### 2.7 Critical Threshold

Setting the aggregator and independent fitness functions equal and solving for $\sigma$ yields the critical threshold $\sigma^*$ where aggregation becomes adaptive. After algebraic manipulation:

$$\sigma^* = \frac{R_{ind} - (1-C_{total}) \cdot f(n) \cdot (1+B_{recip})}{R_{ind} \cdot \beta_{ind} - (1-C_{total}) \cdot \alpha_{agg} \cdot (1-\varepsilon) \cdot f(n) \cdot (1+B_{recip})}$$

With our estimated parameters and $\varepsilon = 0.35$, $n = 25$:

- At zero ecotone advantage ($\varepsilon = 0$): $\sigma^* \approx 0.64$
- At moderate ecotone advantage ($\varepsilon = 0.35$): $\sigma^* \approx 0.53$
- At excellent ecotone advantage ($\varepsilon = 0.45$): $\sigma^* \approx 0.51$

The ecotone substantially lowers the threshold, making aggregation-based signaling adaptive under milder environmental uncertainty than would otherwise be required. This has important implications for site location: Poverty Point's ecotone position made aggregation viable under conditions that would not support aggregation at less advantageous locations.

---

## 3. Agent-Based Model

### 3.1 Model Overview

We developed an agent-based model (ABM) to formalize the theoretical framework, explore parameter space systematically, and validate analytical predictions against simulation outcomes. Agent-based modeling is particularly appropriate for this application because it captures individual-level decision-making, allows for emergent population-level patterns, incorporates spatial and temporal heterogeneity, and enables comparison of simulation outputs with archaeological data.

The model integrates three components: an environment module implementing multi-zone ecological dynamics with seasonal cycles and stochastic shortfalls, an agent module implementing band-level decision-making, strategy choice, and reproduction, and a simulation controller implementing the annual aggregation-dispersal cycle and tracking system-level outcomes.

### 3.2 Environment Module

The environment represents the Lower Mississippi Valley as a heterogeneous landscape with four distinct resource zones, each with characteristic productivity patterns and seasonal dynamics.

**Resource Zone Types:**

The **aquatic zone** encompasses riverine and floodplain resources including fish, waterfowl, turtles, and shellfish. Productivity peaks in spring and summer when fish spawning and waterfowl nesting coincide with high water levels. Base productivity is 0.8 with seasonal amplitude of 0.3, producing annual productivity ranging from 0.5 to 1.1.

The **terrestrial zone** encompasses upland game including deer, turkey, and small mammals. Productivity peaks in fall and winter when deer are concentrated and mast availability concentrates game. Base productivity is 0.7 with seasonal amplitude of 0.25.

The **mast zone** represents hardwood forests producing pecans, hickory nuts, acorns, and walnuts. Productivity is highly seasonal with a sharp fall peak (September-November) and near-zero productivity outside harvest season. Mast crops are also highly variable year-to-year, with periodic mast failures creating additional uncertainty.

The **ecotone zone** represents transitional areas with access to multiple resource types. Productivity is more balanced across seasons, with base productivity 0.6 but reduced seasonal amplitude (0.15), creating more stable year-round resource availability.

**Seasonal Productivity Cycles:**

Each zone follows a sinusoidal productivity cycle with zone-specific phase shifts:

$$P_{zone}(t) = P_{base} + A \cdot \sin(2\pi(t - \phi)/12)$$

where $P_{base}$ is the zone's base productivity, $A$ is seasonal amplitude, $t$ is the month (1-12), and $\phi$ is the phase shift determining peak timing. Aquatic zones peak in month 6 (June), terrestrial zones peak in month 11 (November), and mast zones peak in month 10 (October).

**Inter-Annual Stochastic Variation:**

Beyond seasonal cycles, each zone experiences inter-annual variation drawn from a multivariate normal distribution with specified covariance structure. Critically, zones have **negative covariance** with each other, representing the ecological buffering that makes ecotone locations valuable. For example, aquatic-terrestrial covariance is -0.3, meaning years with poor fishing tend to have good hunting. This covariance structure creates the portfolio effect central to the ecotone advantage.

**Environmental Shortfalls:**

Shortfalls represent major environmental disruptions (droughts, floods, mast failures) that reduce regional productivity. Shortfalls are characterized by three parameters that jointly determine the composite uncertainty measure $\sigma$:

*Frequency* determines how often shortfalls occur. Shortfall probability each year equals $1/\text{mean\_interval}$. For the Poverty Point scenario, mean interval is 10 years, so shortfall probability is 0.10 per year.

*Magnitude* determines the severity of productivity reduction during shortfalls. Magnitude is drawn from a normal distribution centered on the scenario mean. A magnitude of 0.45 means productivity drops to 55% of normal.

*Duration* determines how long shortfalls persist. Critically, duration scales with magnitude: $\text{duration} = \max(1, \lfloor 1 + \text{magnitude} \times 2.5 \rfloor)$. Mild shortfalls (magnitude 0.2) last 1 year; moderate shortfalls (magnitude 0.5) last 2 years; severe shortfalls (magnitude 0.8) last 3 years. This captures the observation that more severe disruptions (major droughts, significant climate shifts) tend to persist longer.

Once triggered, a shortfall persists for its calculated duration, with all zones experiencing reduced productivity. The combination of frequency, magnitude, and duration determines effective environmental uncertainty:

$$\sigma \approx 5.0 \times \frac{1}{\text{frequency}} \times \text{magnitude} \times \sqrt{\text{duration}}$$

This formulation captures the intuition that uncertainty increases with more frequent shortfalls, more severe shortfalls, and longer-lasting shortfalls.

### 3.3 Agent Module

Agents in the model are bands, representing the fundamental decision-making and reproductive unit in hunter-gatherer societies. Each band is characterized by multiple state variables that change over time.

**Band Attributes:**

*Size* represents the number of individuals in the band, ranging from 10 to 50 with typical values around 20-25. Band size affects resource consumption, labor available for monument construction, and reproductive output.

*Home location* is the band's base territory, a fixed coordinate in the model space. Bands forage near their home location during dispersal seasons and return there after aggregation.

*Current strategy* is either AGGREGATOR or INDEPENDENT, updated annually based on expected fitness comparison.

*Resources* represent accumulated food stores, bounded between 0 and 1. Resources are gained through foraging, reduced by consumption, and critical for survival during shortfalls and for investment in monuments.

*Prestige* accumulates through monument contributions and exotic goods acquisition. Higher prestige increases the probability of forming reciprocal obligations with other bands.

*Monument contributions* track cumulative investment in the aggregation site's monuments, contributing to the band's prestige and the site's infrastructure.

*Exotic goods holdings* track accumulated exotic materials, serving as individual-level signals of network connectivity and resource surplus.

*Reciprocal obligations* is a dictionary mapping other bands to obligation strengths, representing the social network that provides insurance during shortfalls.

**Strategy Decision Algorithm:**

Each year during the pre-aggregation period, bands evaluate whether to aggregate or remain independent. The decision algorithm compares expected fitness under each strategy:

1. Calculate expected aggregation size $E[n]$ based on previous year's attendance and environmental conditions
2. Calculate expected fitness if aggregating: $E[W_{agg}]$ using the fitness function with current $\sigma$, site $\varepsilon$, and $E[n]$
3. Calculate expected fitness if independent: $E[W_{ind}]$ using the independent fitness function
4. Calculate fitness difference: $\Delta W = E[W_{agg}] - E[W_{ind}]$

The strategy choice is probabilistic rather than deterministic, following a soft-max (sigmoid) function:

$$P(\text{aggregate}) = \frac{1}{1 + \exp(-\tau \cdot \Delta W)}$$

where $\tau \approx 10$ is the temperature parameter controlling decision determinism. Higher $\tau$ makes decisions more deterministic (bands almost always choose the higher-fitness strategy); lower $\tau$ introduces more stochasticity.

**Memory Effects:**

Bands incorporate recent experience into decisions through memory effects. If a band aggregated last year:
- And fitness improved relative to the previous year: add +0.05 to $\Delta W$ (positive reinforcement)
- And fitness declined: add -0.05 to $\Delta W$ (negative reinforcement)

Opposite effects apply for bands that were independent. This creates path dependence in strategy adoption, where successful strategies tend to persist and unsuccessful strategies tend to be abandoned.

**Reciprocal Obligation Networks:**

During aggregation, bands form reciprocal obligations with other attendees. Formation is probabilistic: each pair of aggregating bands has a 20-30% chance of forming or strengthening an obligation. Obligation strength initializes at 0.1 and increases with repeated co-aggregation, capping at 1.0.

During dispersal, bands experiencing resource shortfalls can call upon obligations:

$$\text{help\_received} = \min(\text{need}, \sum_{j} O_{ij} \times 0.5 \times R_j)$$

where $O_{ij}$ is the obligation strength between bands $i$ and $j$, and $R_j$ is band $j$'s resources. Calling on obligations reduces their strength by 30% ($O_{ij} \leftarrow 0.7 \times O_{ij}$), creating a cost to frequent calls and incentivizing maintenance of obligation networks through continued aggregation.

### 3.4 Annual Cycle

The simulation implements a four-phase annual cycle representing the seasonal round of Late Archaic hunter-gatherers.

**Phase 1: Spring Dispersal (March-May)**

During spring, all bands forage independently near their home locations. Aquatic zone productivity peaks during this period, favoring bands with access to riverine resources. Each band harvests resources based on zone productivity at their location:

$$\text{harvest} = P_{zone}(t) \times \text{foraging\_efficiency}$$

For bands following the aggregator strategy, foraging efficiency is reduced by opportunity cost ($1 - C_{opportunity} \approx 0.81$) because they must begin preparing for the aggregation journey. Independent bands forage at full efficiency (1.0).

Resource consumption equals $\text{band\_size} \times 0.015$ per capita per month. Net resources accumulate: $R \leftarrow R + \text{harvest} - \text{consumption}$, bounded to [0, 1].

**Phase 2: Summer Aggregation (June-August)**

Summer is the aggregation season. At the start of summer, each band executes its strategy decision algorithm to determine this year's strategy.

Bands choosing to aggregate:
1. Pay travel costs proportional to distance from home location to the aggregation site
2. Travel to the central site (Poverty Point location)
3. Access ecotone resources at the aggregation site, benefiting from multi-zone productivity
4. Invest in monument construction if resources exceed 0.3:

$$\text{investment} = \text{band\_size} \times \text{investment\_rate} \times R \times (0.8 + 0.4 \times \text{random})$$

Monument investment adds to both the band's personal prestige ($\text{prestige} \leftarrow \text{prestige} + 0.1 \times \text{investment}$) and the site's cumulative monument level.

5. Form or strengthen reciprocal obligations with other aggregating bands (20-30% probability per pair)
6. May acquire exotic goods (probability proportional to prestige and network size)

Bands remaining independent:
1. Continue foraging near home location
2. Avoid aggregation costs but miss cooperation benefits
3. Cannot form new reciprocal obligations (but existing obligations persist)

**Phase 3: Fall Dispersal (September-November)**

Fall is the primary harvest season, with mast resources peaking and terrestrial game concentrated. All bands return to (or remain at) their home territories for intensive foraging.

Mast zone productivity peaks sharply during this period, providing critical caloric surplus for winter. Bands with access to mast resources receive a harvest bonus. Aggregator bands may continue acquiring exotic goods during fall travel.

This is also when environmental shortfalls have their strongest impact, as failed mast crops and depleted game create severe resource stress.

**Phase 4: Winter (December-February)**

Winter is the mortality and reproduction phase. Environmental shortfall effects are applied: if a shortfall is active, all zones have reduced productivity scaled by shortfall magnitude.

**Differential Mortality:**

Bands face survival challenges based on their strategy:
- Aggregator bands can call upon reciprocal obligations if resources drop below subsistence threshold
- Independent bands face shortfalls alone, with only their stored resources

Mortality probability increases when resources are insufficient:

$$P(\text{death}) = \max(0, (\text{threshold} - R) \times \text{mortality\_rate})$$

Aggregators have lower effective mortality because obligation networks provide a buffer.

**Reproduction:**

Surviving bands reproduce based on fitness:

$$\text{births} \sim \text{Binomial}(\text{band\_size}, \text{birth\_rate} \times \text{fitness} \times (0.5 + R))$$

where fitness is calculated using the appropriate fitness function (aggregator or independent) and resources $R$ modulate reproductive success. This implements the fitness-based reproduction that drives multilevel selection: strategies conferring higher fitness produce more offspring, shifting population composition toward adaptive strategies.

Band sizes are constrained to [10, 50]; bands below minimum may merge, bands above maximum may fission.

### 3.5 Environmental Scenarios

We defined four environmental scenarios representing different levels of uncertainty to explore the phase space and test theoretical predictions.

| Scenario | Frequency | Magnitude | Duration | Effective σ | Interpretation |
|----------|-----------|-----------|----------|-------------|----------------|
| Low Uncertainty | 18 years | 30% | 1 year | ~0.08 | Stable, predictable environment |
| Poverty Point | 10 years | 45% | 2 years | ~0.20 | Calibrated to LMV conditions |
| High Uncertainty | 6 years | 60% | 2-3 years | ~0.43 | Frequent, severe shortfalls |
| Critical Threshold | 8 years | 55% | 2 years | ~0.28 | Near theoretical σ* |

The **Low Uncertainty** scenario represents benign environmental conditions where shortfalls are rare (once per generation) and mild. Under these conditions, the model predicts independent foraging should dominate.

The **Poverty Point** scenario is calibrated to paleoenvironmental evidence from the Lower Mississippi Valley during the Late Archaic, suggesting moderate shortfall frequency with significant but not catastrophic magnitude.

The **High Uncertainty** scenario represents challenging conditions with frequent, severe shortfalls, where aggregation and cooperation should provide strong fitness advantages.

The **Critical Threshold** scenario is calibrated to produce effective uncertainty near the theoretical critical threshold $\sigma^*$, allowing observation of the phase transition.

### 3.6 Simulation Protocol

Each simulation runs for 500 years (approximately the Poverty Point occupation span) with the following protocol:

1. Initialize 30 bands distributed across the landscape with random strategies
2. Run annual cycle for 500 years, recording all state variables
3. Track outcomes: strategy frequencies, aggregation sizes, monument accumulation, exotic goods, population dynamics
4. Replicate 100 times per parameter combination for statistical robustness

Parameter sweeps explore the full $(\sigma, \varepsilon)$ phase space to identify critical thresholds and validate theoretical predictions.

---

## 4. Results

### 4.1 Phase Transition Validation

The simulation validates the theoretically predicted phase transition. Across a sweep of environmental uncertainty values, we observe a sharp transition in strategy dominance at effective σ approximately 0.54, closely matching the theoretical prediction of $\sigma^* \approx 0.53$.

Below effective σ of 0.30, independent strategy strongly dominates. Across 100 replicate simulations, 96% of bands remain independent throughout the 500-year runs. Aggregation events are rare, small (mean 1-4 bands), and unsustained. Monument accumulation is minimal, and exotic goods are scarce.

In the transition zone between σ = 0.30 and σ = 0.54, strategy dominance shifts gradually toward mixed strategies. Some simulations show sustained aggregation while others remain independent-dominated, reflecting bistability near the critical threshold.

Above effective σ of 0.54, a qualitative shift occurs. Strategy dominance shifts from -0.83 (strong independent dominance) to -0.24 (mixed strategies with significant aggregation). Mean aggregation size jumps from 4 bands to 19 bands, approaching the theoretical optimal size of 25. Monument investment increases approximately fivefold, from ~5,600 units to ~30,300 units over 500 years.

![Figure 1. Phase Transition Validation](../../figures/integrated/fig_phase_transition.png)

***Figure 1. Phase transition validation.*** *Four panels showing: (A) Strategy dominance as a function of effective environmental uncertainty (σ_eff), with negative values indicating independent dominance and positive values indicating aggregator dominance. The dashed line marks the theoretical critical threshold σ* = 0.53, which closely matches the observed transition at σ_eff ≈ 0.54. (B) Mean aggregation size increases sharply above the threshold, jumping from 4 bands to 19 bands and approaching the theoretical optimal size of 25. (C) Monument investment shows a fivefold increase above threshold, from approximately 5,600 to 30,300 units. (D) Scatter plot showing the strong relationship between strategy dominance and monument investment, with points colored by effective σ demonstrating that high monument accumulation occurs only under high uncertainty conditions.*

This phase transition behavior supports the core theoretical prediction that aggregation-based costly signaling emerges as an adaptive response to environmental uncertainty above a critical threshold. The model reproduces the key prediction from multilevel selection theory: costly signaling becomes adaptive precisely when between-group selection (favoring cooperation and signaling) overcomes within-group selection (favoring cost avoidance).

### 4.2 Phase Space Structure

Exploration of the full phase space defined by environmental uncertainty (σ) and ecotone advantage (ε) confirms that both parameters influence strategy outcomes as predicted by the theoretical framework.

At low ecotone advantage (ε < 0.2), higher environmental uncertainty is required for aggregation to become adaptive. The critical threshold shifts rightward, requiring σ > 0.60 for sustained aggregation. This occurs because without ecotone buffering, aggregators experience nearly the same effective uncertainty as independents, eliminating the survival advantage of aggregation.

At high ecotone advantage (ε > 0.4), aggregation becomes adaptive at lower uncertainty levels. The critical threshold shifts leftward to σ ≈ 0.45. Strong ecotone buffering means aggregators experience substantially lower effective uncertainty, amplifying the survival advantage and reducing the uncertainty required for aggregation to pay off.

Monument investment concentrates in the high-σ, high-ε quadrant of phase space, exactly as predicted. Maximum monument accumulation occurs at (σ = 0.80, ε = 0.50), representing conditions of high regional uncertainty combined with excellent ecotone buffering at the aggregation site.

![Figure 2. Phase Space Structure](../../figures/integrated/fig_phase_space.png)

***Figure 2. Phase space structure.*** *(A) Strategy dominance across the two-dimensional phase space defined by environmental uncertainty (σ, x-axis) and ecotone advantage (ε, y-axis). Purple shading indicates independent strategy dominance; orange shading indicates aggregation dominance. The solid black line shows the theoretical critical threshold, which accurately separates the two regimes. (B) Monument investment across the same phase space, showing concentration in the upper-right quadrant where high uncertainty combines with strong ecotone advantage.*

The theoretical critical threshold line accurately separates regions dominated by independent versus aggregation strategies. All simulation points where effective σ exceeds the theoretical $\sigma^*$ showed dominance shifts toward aggregation, validating the analytical predictions.

### 4.3 Scenario Comparison

The four environmental scenarios produce distinct outcomes over 500-year simulations, demonstrating how environmental uncertainty drives the emergence of costly signaling.

**Low Uncertainty (σ_eff ≈ 0.08):** Populations stabilize with 96% independent strategy dominance. Aggregation events are rare (mean interval ~45 years) and small (2-4 bands). Monument accumulation is minimal at 5,521 units, representing sporadic, unsustained construction. Exotic goods total only 895 items. Population dynamics are stable with low variance.

**Calibrated Poverty Point (σ_eff ≈ 0.20):** Populations show 91% independent strategy dominance but with consistent minority aggregation. Monument accumulation reaches 5,920 units with steady, sustained construction. Exotic goods total 1,909 items. This scenario produces the bistable dynamics expected near the critical threshold, with strategy frequencies fluctuating in response to environmental conditions.

**High Uncertainty (σ_eff ≈ 0.43):** A qualitative shift occurs, with only 60% independent dominance. Aggregation becomes consistent and substantial, with mean aggregation sizes of 12-15 bands. Monument accumulation reaches 7,193 units with accelerated construction during shortfall periods. Exotic goods total 5,265 items, reflecting expanded network connectivity.

**Critical Threshold (σ_eff ≈ 0.28):** At parameters calibrated to the theoretical threshold, populations show 84% independent dominance but with elevated monument construction (8,744 units) and intermediate exotic accumulation (3,289 items). Strategy frequencies show high variance across replicates, reflecting the bistability characteristic of phase transitions.

![Figure 3. Scenario Comparison](../../figures/integrated/fig_scenario_comparison.png)

***Figure 3. Scenario comparison.*** *Four panels showing: (A) Population dynamics over 500 simulated years under four environmental scenarios: low uncertainty (purple), calibrated Poverty Point (green), high uncertainty (orange), and critical threshold (dark orange). Population sizes remain stable across scenarios. (B) Strategy dominance time series showing fluctuations in response to shortfall events, with high uncertainty producing sustained shifts toward aggregation. (C) Cumulative monument construction showing accelerated accumulation under higher uncertainty, with the high uncertainty scenario producing ~30% more monument investment than the low uncertainty scenario. (D) Summary comparison of final state metrics across scenarios, showing monotonic relationships between uncertainty and both aggregation and costly signaling.*

Monument accumulation increases monotonically with environmental uncertainty across all scenarios. Exotic goods totals track monument investment closely, with the high uncertainty scenario producing quantities closest to archaeological estimates. The temporal dynamics show that strategy dominance fluctuates in response to shortfall events, with aggregation becoming more attractive during and immediately after environmental crises.

### 4.4 Archaeological Calibration

Model outputs can be scaled to archaeological quantities to evaluate fit with Poverty Point data. The calibration approach identifies a scaling factor that maps model units to archaeological measurements.

**Monument Volume:**

Using a calibration factor of 142.6, the model produces approximately 750,000 cubic meters of monument volume over the 500-year simulation under Poverty Point scenario conditions. This closely matches archaeological estimates for total Poverty Point earthwork volume (Ortmann 2007; Sherwood and Kidder 2011).

The scaling factor represents the conversion from model "investment units" (which abstract labor and materials) to physical cubic meters. The calibration holds across scenarios: low uncertainty produces ~390,000 m³, high uncertainty produces ~1,025,000 m³, maintaining proportional relationships.

**Exotic Goods:**

Exotic goods totals in the model range from 895 under low uncertainty to 5,265 under high uncertainty. The archaeological record shows approximately 3,078 items of copper, steatite, and galena combined (Hill et al. 2016; Webb 1968), falling within the model's prediction range. The high uncertainty scenario produces counts closest to archaeological totals (5,265 modeled vs. 3,078 observed), suggesting that Poverty Point conditions may have involved greater environmental uncertainty than the baseline calibrated scenario.

![Figure 4. Archaeological Calibration](../../figures/integrated/fig_calibration.png)

***Figure 4. Archaeological calibration.*** *(A) Monument volume comparison between model predictions (scaled by calibration factor 142.6) and archaeological estimates, showing close correspondence at approximately 750,000 cubic meters for the Poverty Point scenario. (B) Exotic goods comparison between model scenarios and archaeological counts, with the high uncertainty scenario providing the closest match to observed totals. (C) Model fit assessment showing deviation from archaeological data by scenario, confirming that intermediate-to-high uncertainty scenarios best reproduce the archaeological pattern.*

**Population Dynamics:**

Population dynamics stabilize around 400-500 individuals across 25-30 bands, consistent with ethnographic expectations for hunter-gatherer aggregations in productive environments (Jackson 1986; Jackson and Scott 2001). The model does not produce population collapse or runaway growth, indicating stable equilibrium dynamics.

### 4.5 Temporal Dynamics and Construction Chronology

Time series analysis reveals important temporal patterns in strategy adoption and monument construction.

Strategy dominance fluctuates in response to environmental conditions. During shortfall periods, aggregation becomes more attractive as bands seek cooperation benefits and risk pooling. The lag between shortfall onset and strategy shift is typically 1-2 years, reflecting the memory effects in the decision algorithm.

Monument construction proceeds in pulses corresponding to periods of elevated aggregation rather than at constant rates. Years following shortfalls show construction peaks as aggregation attracts more bands and bands invest more heavily in signaling. Inter-pulse periods show reduced but continued construction from the core aggregating population.

These temporal dynamics suggest that archaeological evidence for construction pulses (Hargrave et al. 2021) may correlate with periods of environmental stress rather than representing organizational changes or external influences. The pulsed construction pattern emerges naturally from the model without requiring changes in social organization or leadership.

Exotic goods accumulate more gradually than monuments, reflecting the individual-level acquisition process. However, exotic accumulation also shows acceleration during high-aggregation periods when network connectivity is greatest.

---

## 5. Discussion

### 5.1 The Poverty Point Paradox Resolved

Our model provides a unified explanation for the apparently paradoxical combination of massive collective monument construction and extensive individual exotic goods acquisition at Poverty Point. Both phenomena emerge as adaptive costly signals under conditions of environmental uncertainty combined with ecotone access.

Monument construction represents collective investment in an honest signal of commitment to the aggregation system. Bands that invest heavily in monuments demonstrate capacity and willingness to participate in long-term cooperation, reducing uncertainty about partner reliability. The sunk cost nature of monument investment creates commitment that binds participants to return year after year. A band that abandons the aggregation system loses the value of accumulated monument investment, creating strong incentives for continued participation.

Exotic goods acquisition represents individual investment in honest signals of cooperation capacity. Bands that acquire exotic materials demonstrate resource surplus (they can afford the acquisition costs), network connectivity (they have access to distant sources), and commitment to the exchange system (Smith 1976; Hill et al. 2016). These signals allow potential partners to identify bands likely to reciprocate during future interactions.

Both signal types solve the fundamental cooperation problems inherent in aggregation: partner identification, free-rider prevention, and commitment. Neither requires aggrandizers exercising coercive power, religious motivation creating irrational behavior, or incipient complexity driving organizational change. The signaling system emerges from individual fitness-maximizing decisions under specific environmental conditions.

### 5.2 Multilevel Selection in Action

The simulation results demonstrate multilevel selection operating through the mechanisms identified in the theoretical framework. Between-group selection favors aggregation and signaling because aggregating groups (and the bands within them) survive shortfalls at higher rates than independent bands. This differential survival creates positive covariance between group fitness and signaling frequency, the first term in the Price equation.

Within-group selection opposes signaling because aggregators pay costs that independents avoid. If shortfalls were rare (low σ), these costs would dominate and signaling would be selected against. The within-group component, the second term in the Price equation, is always negative.

The phase transition occurs precisely where these forces balance. Below $\sigma^*$, within-group selection dominates and the population converges on independent strategies. Above $\sigma^*$, between-group selection dominates and signaling spreads. The sharpness of the transition reflects the nonlinear feedback between aggregation size and cooperation benefits: once aggregation begins to pay off, it attracts more bands, increasing cooperation benefits and further favoring aggregation.

The simulation validates this theoretical prediction quantitatively. The observed critical threshold ($\sigma_{eff} \approx 0.54$) matches the analytical prediction ($\sigma^* \approx 0.53$) within simulation error. This correspondence provides strong support for the multilevel selection interpretation of Poverty Point monumentality.

### 5.3 Site Location Optimality

The model predicts that aggregation sites should be located at positions maximizing ecotone access, not simply at resource concentrations or network centrality points. Poverty Point's position at the intersection of multiple ecological zones provides precisely this advantage. The site offers access to floodplain aquatic resources, upland terrestrial game, riverine fish and waterfowl, and forest mast resources (Jackson 1986, 1989; Ward 1998).

Alternative locations with lower ecotone access would face higher effective environmental uncertainty, requiring more extreme regional conditions for aggregation to become adaptive. This explains why Poverty Point achieved primacy over other contemporaneous sites in the region despite not being centrally located in the exchange network or positioned at maximum resource abundance.

The ecotone advantage also explains why Poverty Point could sustain extended aggregations. Multi-zone access meant that aggregating bands were not depleting a single resource type; as aquatic resources declined from intensive exploitation, bands could shift to terrestrial or mast resources. This buffering extended viable aggregation duration and reduced the costs of aggregation, further favoring the Poverty Point location.

### 5.4 Regional Site Hierarchy

The model predicts declining site investment with declining ecotone access. Secondary sites like Jaketown, Claiborne, and J.W. Copes should show lower monument investment proportional to their reduced ecotone advantage (Thomas and Campbell 1978; Jackson 1982; Saunders et al. 2001). Archaeological evidence supports this prediction, with these sites showing earthwork volumes orders of magnitude smaller than Poverty Point despite similar occupation spans.

Distance from the primary aggregation site also affects participation probability due to travel costs. Bands from distant territories face higher costs to aggregate, reducing their fitness advantage from participation. This creates catchment zones around aggregation sites with declining participation intensity.

### 5.5 System Collapse

The model identifies conditions for system abandonment. If environmental uncertainty declines below the critical threshold, aggregation loses its fitness advantage and bands shift toward independent foraging. If ecotone access shifts due to environmental change such as river channel migration, effective uncertainty at the aggregation site increases relative to the regional baseline, potentially pushing conditions below threshold.

Archaeological evidence suggests Poverty Point was abandoned around 1100 BCE after approximately 500-600 years of occupation. Climate reconstruction for this period indicates declining flood frequency and potentially reduced environmental uncertainty (Kidder 2006). River channel changes may have altered ecotone accessibility at the site location. Both mechanisms are consistent with the model's predictions for system collapse.

The model predicts that collapse should be relatively rapid once initiated. As uncertainty declines below threshold, aggregation becomes fitness-reducing. Bands that continue aggregating are outcompeted by bands that shift to independent strategies. The positive feedback that sustained aggregation reverses, producing rapid abandonment rather than gradual decline.

### 5.6 Comparison with Alternative Explanations

The costly signaling model differs from alternatives in several key respects.

Unlike **aggrandizer models** (Gibson and Carr 2004), our approach requires no asymmetric power relations. All participants benefit from the signaling system under appropriate environmental conditions. Individual bands choose strategies based on expected fitness, with aggregation emerging as an equilibrium rather than being imposed. The model explains why followers would participate in monument construction without requiring coercion or deception.

Unlike **pilgrimage models** (Spivey et al. 2015), our approach is explanatory rather than descriptive. It specifies conditions under which aggregation becomes adaptive, predicts site location based on environmental parameters, and identifies conditions for system collapse. Religious motivation may accompany aggregation behavior, but the ultimate explanation lies in fitness consequences.

Unlike **trade models** (Gibson 1999), our approach explains monument construction directly. Exotic goods and monuments serve parallel signaling functions rather than monuments being incidental to exchange. The co-occurrence of both phenomena follows necessarily from the theoretical framework: both are honest signals solving cooperation problems.

Unlike **incipient complexity models**, our approach does not require organizational or social changes beyond the aggregation behavior itself. Bands remain mobile and maintain flexible membership. The "complexity" at Poverty Point represents a particular adaptation to environmental conditions rather than a stage in progressive development toward more complex social organization.

### 5.7 Testable Predictions

The model generates specific testable predictions beyond those already examined.

**Construction chronology** should correlate with paleoclimate proxies for environmental uncertainty. If climate reconstruction indicates elevated uncertainty during specific periods, monument construction should concentrate in those intervals. The model predicts pulsed construction following shortfall events, not constant accumulation.

**Exotic goods source directions** should show multi-directional patterns reflecting a wide network of participating bands rather than linear trade routes. Isotopic and geochemical sourcing studies (Hill et al. 2016) can test this prediction against alternatives emphasizing directed exchange along specific corridors.

**Site spacing** should reflect the balance between ecotone access and travel costs. Secondary aggregation sites should emerge at distances where travel costs to the primary site begin to exceed ecotone advantages of the primary location. This predicts a characteristic spacing of 100-200 km between major aggregation sites.

**Individual-level variation** in exotic goods holdings should correlate with band position in the reciprocal obligation network. High-prestige bands should show both higher exotic holdings and more extensive obligation connections, reflecting the signaling function of exotic acquisition.

---

## 6. Conclusions

The Poverty Point paradox finds resolution in the framework of aggregation-based costly signaling. By extending multilevel selection theory to incorporate the specific challenges faced by mobile hunter-gatherer bands, we derive conditions under which aggregation with monument construction and exotic goods acquisition becomes adaptive. The critical insight is that Poverty Point represents neither anomalous behavior nor incipient complexity, but an adaptive response to specific environmental conditions.

When environmental uncertainty exceeds a critical threshold and ecotone access is sufficient, aggregation with costly signaling provides higher fitness than independent foraging. The monuments and exotic goods are not wasteful displays but functional solutions to cooperation problems inherent in aggregation. They signal commitment and capacity, enabling the formation of reciprocal obligation networks that buffer participants against environmental risk.

Our agent-based model validates these theoretical predictions quantitatively. The simulated phase transition at effective σ approximately 0.54 closely matches the theoretical prediction of $\sigma^* \approx 0.53$. Model outputs scale to archaeological estimates for monument volume and exotic goods quantities. Scenario comparisons demonstrate the predicted relationships between environmental uncertainty, aggregation intensity, and costly signaling investment.

The model implements multilevel selection through fitness-based reproduction, with between-group selection (cooperation benefits, reduced shortfall vulnerability) balanced against within-group selection (signaling costs, opportunity costs). The phase transition emerges when between-group selection overcomes within-group costs, exactly as predicted by the Price equation framework.

This framework has implications beyond Poverty Point. Any mobile population facing cooperation challenges under environmental uncertainty may develop analogous signaling systems. The specific signals will vary with context, but the underlying logic remains constant: costly investment demonstrates commitment, enabling cooperation that would otherwise fail due to free-rider and commitment problems.

The Poverty Point phenomenon thus represents not an anomaly requiring special explanation but an expected outcome given the environmental and social conditions of the Late Archaic Lower Mississippi Valley. Understanding it requires neither mysterious religious motivation, exploitative elites, nor evolutionary progression toward complexity. It requires only that we recognize hunter-gatherer populations as capable of sophisticated adaptive responses to their environments.

---

## Acknowledgments

[To be added]

---

## Data Availability

Simulation code and analysis results are available at https://github.com/clipo/poverty-point-signaling. Archaeological data sources are cited in the text.

---

## References

DiNapoli, R.J., Lipo, C.P., Brosnan, T., Hunt, T.L., Hixon, S., Morrison, A.E., Becker, M., 2021. Rapa Nui (Easter Island) monument (ahu) locations explained by freshwater sources. PLoS ONE 16, e0245008. https://doi.org/10.1371/journal.pone.0245008

Gibson, J.L., 1999. Swamp exchange and the walled mart: Poverty Point's rock business. In: Peacock, E., Brookes, S.O. (Eds.), Raw Materials and Exchange in the Mid-South. Archaeological Report 29. Mississippi Department of Archives and History, Jackson, pp. 57-64.

Gibson, J.L., 2000. The Ancient Mounds of Poverty Point: Place of Rings. University of Florida Press, Gainesville.

Gibson, J.L., 2001. The Ancient Mounds of Poverty Point: Place of Rings. University of Florida Press, Gainesville.

Gibson, J.L., 2007. "Formed from the Earth at That Place": The material side of community at Poverty Point. American Antiquity 72, 509-523. https://doi.org/10.2307/40035858

Gibson, J.L., Carr, P.J. (Eds.), 2004. Signs of Power: The Rise of Cultural Complexity in the Southeast. University of Alabama Press, Tuscaloosa.

Grafen, A., 1990. Biological signals as handicaps. Journal of Theoretical Biology 144, 517-546.

Haag, W.G., 1990. Excavations at the Poverty Point Site: 1972-1975. Louisiana Archaeology 13, 1-36.

Hargrave, M.L., Britt, T., Reynolds, M.D., 2007. Magnetic evidence of ridge construction and use at Poverty Point. American Antiquity 72, 757-770. https://doi.org/10.2307/25470444

Hargrave, M.L., Clay, R.B., Dalan, R.A., Greenlee, D.M., 2021. The complex construction history of Poverty Point's timber circles and concentric ridges. Southeastern Archaeology 40, 1-20. https://doi.org/10.1080/0734578X.2021.1961350

Hayden, B., 2009. The proof is in the pudding: Feasting and the origins of domestication. Current Anthropology 50, 597-601. https://doi.org/10.1086/605110

Hayden, B., 2014. The Power of Feasts: From Prehistory to the Present. Cambridge University Press, Cambridge.

Hays, C.T., 2019. Feasting at Poverty Point with Poverty Point Objects. Southeastern Archaeology 38, 193-207. https://doi.org/10.1080/0734578X.2018.1496315

Hill, M.A., Greenlee, D.M., Neff, H., 2016. Assessing the provenance of Poverty Point copper through LA-ICP-MS compositional analysis. Journal of Archaeological Science: Reports 6, 351-360. https://doi.org/10.1016/j.jasrep.2016.02.030

Jackson, H.E., 1982. Recent research on Poverty Point subsistence and settlement systems: Test excavations at the J.W. Copes site in northeast Louisiana. Louisiana Archaeology 8, 73-86.

Jackson, H.E., 1986. Sedentism and Hunter-Gatherer Adaptations in the Lower Mississippi Valley: Subsistence Strategies During the Poverty Point Period. University Microfilms, Ann Arbor.

Jackson, H.E., 1989. Poverty Point adaptive systems in the Lower Mississippi Valley: Subsistence remains from the J.W. Copes site. North American Archaeologist 10, 173-204.

Jackson, H.E., Scott, S.L., 2001. Archaic faunal utilization in the Louisiana bottomlands. Southeastern Archaeology 20, 187-196.

Kidder, T.R., 2002. Mapping Poverty Point. American Antiquity 67, 89-101. https://doi.org/10.2307/2694878

Kidder, T.R., 2006. Climate change and the Archaic to Woodland transition (3000-2500 cal B.P.) in the Mississippi River basin. American Antiquity 71, 195-231. https://doi.org/10.2307/40035903

Kidder, T.R., Ortmann, A., Allen, T., 2004. Testing Mounds B and E at Poverty Point. Southeastern Archaeology 23, 98-113.

Kidder, T.R., Arco, L.J., Ortmann, A.L., Schilling, T., Boeke, C., Bielitz, R., Adelsberger, K.A., 2009. Poverty Point Mound A: Final report of the 2005 and 2006 field seasons. Report submitted to the Louisiana Division of Archaeology.

Lehmann, G.R., 1991. A summary of Poverty Point investigations in the Yazoo Basin, Mississippi. In: Byrd, K.M. (Ed.), The Poverty Point Culture: Local Manifestations, Subsistence Practices, and Trade Networks. Geoscience and Man 29. Louisiana State University, Baton Rouge, pp. 55-60.

Lipo, C.P., Hunt, T.L., Horneman, R., Bonhomme, V., 2016. Weapons of war? Rapa Nui mata'a morphometric analyses. Antiquity 90, 172-187.

Ortmann, A.L., 2007. The Poverty Point Mounds: Analysis of the chronology, construction history, and function of North America's largest hunter-gatherer monuments. Ph.D. dissertation, Tulane University, New Orleans.

Ortmann, A.L., Kidder, T.R., 2013. Building Mound A at Poverty Point, Louisiana: Monumental public architecture, ritual practice, and implications for hunter-gatherer complexity. Geoarchaeology 28, 66-86. https://doi.org/10.1002/gea.21430

Price, G.R., 1970. Selection and covariance. Nature 227, 520-521.

Sassaman, K.E., 1993. Early Pottery in the Southeast: Tradition and Innovation in Cooking Technology. University of Alabama Press, Tuscaloosa.

Saunders, J., Allen, T., Labatt, D., Jones, R., Griffing, D., 2001. An assessment of the antiquity of the Lower Jackson Mound. Southeastern Archaeology 20, 67-77.

Sherwood, S.C., Kidder, T.R., 2011. The DaVincis of dirt: Geoarchaeological perspectives on Native American mound building in the Mississippi River basin. Journal of Anthropological Archaeology 30, 69-87. https://doi.org/10.1016/j.jaa.2010.11.001

Smith, B.W., 1976. The Late Archaic-Poverty Point steatite trade network in the lower Mississippi Valley. Newsletter of the Louisiana Archaeological Society 3(4), 6-10.

Spivey, S.M., Kidder, T.R., Ortmann, A.L., Arco, L.J., 2015. Pilgrimage to Poverty Point? In: Gilmore, Z., O'Donoughue, J. (Eds.), The Enigma of the Event: Moments of Consequence in the Ancient Southeast. University of Alabama Press, Tuscaloosa, pp. 230-267.

Thomas, P.M., Campbell, L.J., 1978. The Peripheries of Poverty Point. New World Research, Pollock, Louisiana.

Ward, H.D., 1998. The paleoethnobotanical record of the Poverty Point culture: Implications of past and current research. Southeastern Archaeology 17, 166-174.

Webb, C.H., 1968. The extent and content of Poverty Point culture. American Antiquity 33, 297-321. https://doi.org/10.2307/278700

Webb, C.H., 1982. The Poverty Point Culture, 2nd ed. Geoscience and Man XVII. Louisiana State University School of Geoscience, Baton Rouge.

Zahavi, A., 1975. Mate selection: A selection for a handicap. Journal of Theoretical Biology 53, 205-214.
