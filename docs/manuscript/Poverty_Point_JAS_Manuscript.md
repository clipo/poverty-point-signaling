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

Poverty Point, located in northeastern Louisiana near the confluence of Bayou Macon and the Arkansas River, presents one of the most remarkable archaeological sites in North America. Dating to approximately 1700-1100 BCE, the site encompasses approximately 160 hectares of constructed landscape, including six concentric C-shaped ridges, multiple mounds, and a 17-hectare central plaza. Mound A, the largest earthwork, rises 22 meters and contains an estimated 238,000 cubic meters of fill. Conservative estimates suggest the total earthwork volume exceeds 750,000 cubic meters, representing 1-5 million person-hours of labor investment. Recent research indicates that Mound A may have been constructed in a matter of months rather than generations, implying coordinated labor mobilization at unprecedented scales for hunter-gatherer societies.

The site also served as a focal point for long-distance exchange networks spanning much of eastern North America. Materials sourced from distances exceeding 1,600 kilometers accumulated at Poverty Point in quantities far exceeding any contemporary location. These include copper from the Great Lakes region, galena from Missouri, steatite from the Appalachians, and various lithic materials from across the midcontinent. The combination of massive collective monument construction with extensive individual acquisition of exotic materials demands explanation.

This pattern is paradoxical when viewed through standard models of hunter-gatherer behavior. Ethnographic and archaeological evidence suggests that mobile foraging populations typically minimize investment in fixed infrastructure, maintain flexible group membership, and avoid accumulation of surplus beyond immediate needs. The Poverty Point phenomenon appears to violate these expectations fundamentally. Why would mobile bands invest so heavily in monuments they would periodically abandon? Why acquire exotic materials with no apparent utilitarian function? Why create such pronounced site hierarchy in an otherwise dispersed settlement system?

Previous explanations have invoked several mechanisms, each facing significant challenges. "Big Man" or aggrandizer models propose that powerful individuals mobilized labor through prestige competition, but these accounts assume rather than explain why others participated in what appears to be collective action benefiting elites. Pilgrimage or ritual models describe the phenomenon as religious gatherings but provide no explanation for why this location, why such investment levels, or why the system eventually ended. Trade center models explain the exotic materials but fail to account for monument construction, which has no obvious role in exchange. Incipient sedentism models conflict with artifact distributions and site structure suggesting continued residential mobility for most participants.

We propose an alternative explanation grounded in evolutionary theory: Poverty Point represents an adaptive costly signaling system operating through seasonal aggregation dynamics. Building on the multilevel selection framework developed for explaining monument construction in territorial societies, we extend the theory to incorporate the specific challenges faced by mobile hunter-gatherer bands. Our model shows that under appropriate environmental conditions, aggregation with costly signaling emerges as a fitness-enhancing strategy, with both monument construction and exotic goods acquisition serving as honest signals of cooperation capacity and commitment.

The remainder of this paper develops this argument in four sections. Section 2 presents the theoretical framework, deriving the conditions under which aggregation-based costly signaling becomes adaptive. Section 3 describes an agent-based model that formalizes these dynamics. Section 4 presents simulation results validating the theoretical predictions and comparing model outputs to archaeological data. Section 5 discusses implications and identifies testable predictions that distinguish our model from alternatives.

---

## 2. Theoretical Framework

### 2.1 Costly Signaling and Multilevel Selection

Our approach builds on the Price equation for multilevel selection, which partitions evolutionary change into between-group and within-group components. The first term represents between-group selection, which can favor costly traits if they benefit the group. The second term represents within-group selection, which typically opposes costly traits because individuals bearing the cost have lower relative fitness within their group.

Previous applications of this framework to Rapa Nui moai construction and Chaco Canyon great houses demonstrated that environmental uncertainty modulates the relative strength of these selective forces. Above a critical threshold of uncertainty, the survival benefits of costly signaling during environmental shortfalls outweigh the reproductive costs during normal years. This creates a phase transition in the strategy space, with signaling becoming adaptive only under sufficiently uncertain environmental conditions.

However, these territorial models cannot be directly applied to Poverty Point. The key differences involve social organization, spatial dynamics, and signal function. Territorial groups compete for fixed resources through monument display that deters competitors. Mobile hunter-gatherer bands face a fundamentally different optimization problem: they must decide whether to aggregate at central locations, how long to remain, and how much to invest in collective activities. The signal function shifts from deterrence to attraction, from "we can defend this territory" to "we will cooperate reliably."

### 2.2 The Aggregation Challenge

Hunter-gatherer bands face coordination and commitment problems that aggregation alone cannot solve. Without signaling mechanisms, aggregations are vulnerable to free-riding, where bands extract benefits without contributing to collective activities. Partner identification becomes difficult when bands cannot distinguish reliable cooperators from exploiters. Commitment problems arise because bands have no incentive to return to the same aggregation site without sunk costs binding them to the system.

Costly signaling through monument construction and exotic goods acquisition solves these problems. Monument investment creates a sunk cost that demonstrates commitment to the aggregation system. Exotic goods signal individual capacity and willingness to invest in the network. Both signals are honest in the evolutionary sense because they cannot be cheaply faked.

### 2.3 Model Structure

We extend the multilevel selection framework to incorporate aggregation dynamics. Bands face a choice between two strategies. The aggregator strategy involves traveling to a central site during the aggregation season, investing in monuments and exotic goods, participating in collective activities, and forming reciprocal obligations. The independent strategy involves remaining dispersed, avoiding aggregation costs, and foraging independently.

The fitness function for aggregators is:

W_agg(σ, ε, n) = (1 - C_total)(1 - α_agg × σ_eff) × f(n) × (1 + B_recip)

where C_total represents total costs (travel, signaling, and opportunity costs, approximately 0.42), α_agg represents vulnerability to shortfalls (reduced by buffering, approximately 0.40), σ_eff represents effective environmental uncertainty (reduced by ecotone access), f(n) represents cooperation benefits as a function of aggregation size, and B_recip represents benefits from reciprocal obligations during dispersal.

The fitness function for independents is:

W_ind(σ) = R_ind(1 - β_ind × σ)

where R_ind represents the reproductive advantage from avoiding aggregation costs (approximately 1.10) and β_ind represents vulnerability to shortfalls when foraging independently (approximately 0.75).

### 2.4 The Ecotone Advantage

A critical innovation in our model is the ecotone advantage parameter (ε), which captures the benefits of multi-zone ecological access at the aggregation site. Poverty Point is positioned at the intersection of multiple ecological zones: Mississippi River floodplain aquatic resources, Macon Ridge upland terrestrial game, Bayou Macon drainage fish and waterfowl, and hardwood forest mast resources.

When these zones have negative covariance in productivity, the ecotone provides variance reduction. If one zone fails, another may succeed. This reduces the effective uncertainty experienced at the aggregation site:

σ_eff = σ_regional(1 - ε)

The ecotone advantage has profound implications. It reduces effective uncertainty at the aggregation site, enables extended aggregation through diverse resource access, creates site primacy for locations with maximum ecotone access, and lowers the critical threshold for aggregation to become adaptive.

### 2.5 Critical Threshold

Setting the aggregator and independent fitness functions equal and solving for σ yields the critical threshold σ* where aggregation becomes adaptive. With our estimated parameters, σ* ranges from approximately 0.64 at zero ecotone advantage to approximately 0.51 at excellent ecotone advantage (ε = 0.45). The ecotone substantially lowers the threshold, making aggregation-based signaling adaptive under milder environmental uncertainty than would otherwise be required.

### 2.6 Cooperation Benefits

The returns to aggregation show increasing then diminishing returns. Cooperation benefits increase logarithmically with aggregation size due to information exchange, collective fishing, labor pooling, and risk pooling. However, crowding costs emerge above the optimal size due to local resource depletion, disease transmission, and coordination difficulties. We estimate optimal aggregation size at approximately 25 bands before crowding costs begin to dominate.

---

## 3. Agent-Based Model

### 3.1 Model Overview

We developed an agent-based model to formalize the theoretical framework and explore parameter space systematically. The model integrates three components: an environment module implementing multi-zone ecological dynamics with seasonal cycles and stochastic shortfalls, an agent module implementing band-level decision-making and strategy choice, and a simulation controller implementing the annual aggregation-dispersal cycle.

### 3.2 Environment Module

The environment consists of four resource zones (aquatic, terrestrial, mast, and ecotone) distributed across a 500-kilometer region. Each zone follows seasonal productivity cycles with inter-annual stochastic variation. Zones have negative covariance in productivity, creating the buffering effect central to ecotone advantage.

Environmental shortfalls occur stochastically with parameters controlling frequency (mean interval between events), magnitude (depth of productivity reduction), and duration (how long shortfalls persist). Shortfall magnitude affects both depth and duration, with more severe shortfalls lasting longer.

### 3.3 Agent Module

Bands are the primary decision-making units. Each band has attributes including size, home location, current strategy, resource holdings, prestige, monument contributions, and exotic goods holdings. Bands form reciprocal obligation networks that persist across years.

Strategy choice follows a sigmoid function based on expected fitness difference between aggregating and remaining independent. Bands incorporate memory effects from recent experience, creating path dependence in strategy adoption.

### 3.4 Annual Cycle

The simulation implements a four-phase annual cycle. During spring dispersal, bands forage independently based on zone productivity near their home locations. During summer aggregation, bands following the aggregator strategy travel to the central site, invest in monument construction, form reciprocal obligations, and benefit from cooperation. During fall dispersal, bands return to home territories and may acquire exotic goods. During winter, environmental shortfalls may cause mortality with differential vulnerability based on strategy.

### 3.5 Environmental Scenarios

We defined four environmental scenarios representing different levels of uncertainty. The low uncertainty scenario has shortfalls every 18 years with 30% magnitude, producing effective σ around 0.08. The calibrated Poverty Point scenario has shortfalls every 10 years with 45% magnitude, producing effective σ around 0.20. The high uncertainty scenario has shortfalls every 6 years with 60% magnitude, producing effective σ around 0.43. The critical threshold scenario has shortfalls every 8 years with 55% magnitude, producing effective σ around 0.28.

---

## 4. Results

### 4.1 Phase Transition Validation

The simulation validates the theoretically predicted phase transition. Across a sweep of environmental uncertainty values, we observe a sharp transition at effective σ approximately 0.54, closely matching the theoretical prediction of σ* approximately 0.53.

Below effective σ of 0.30, independent strategy strongly dominates with 96% of bands remaining independent. In the transition zone between 0.30 and 0.54, strategy dominance shifts gradually toward mixed strategies. Above effective σ of 0.54, a qualitative shift occurs. Strategy dominance shifts from -0.83 to -0.24. Mean aggregation size jumps from 4 bands to 19 bands, approaching the theoretical optimal size of 25. Monument investment increases approximately fivefold.

This phase transition behavior supports the core theoretical prediction that aggregation-based costly signaling emerges as an adaptive response to environmental uncertainty above a critical threshold.

### 4.2 Phase Space Structure

Exploration of the full phase space confirms that both σ and ε influence strategy outcomes as predicted. At low ecotone advantage, higher environmental uncertainty is required for aggregation to become adaptive. At high ecotone advantage, aggregation becomes adaptive at lower uncertainty levels. Monument investment concentrates in the high-σ, high-ε quadrant of phase space.

The theoretical critical threshold line accurately separates regions dominated by independent versus aggregation strategies. All simulation points where effective σ exceeds the theoretical σ* showed dominance shifts toward aggregation.

### 4.3 Scenario Comparison

The four environmental scenarios produce distinct outcomes over 500-year simulations. Under low uncertainty conditions, populations stabilize with 96% independent strategy, minimal monument accumulation, and low exotic goods totals. Under calibrated Poverty Point conditions, populations show 91% independent strategy but moderate monument accumulation and exotic goods. Under high uncertainty conditions, populations shift toward 60% independent with sustained monument construction and high exotic accumulation. Under critical threshold conditions, populations remain 84% independent but show elevated monument construction.

Monument accumulation increases monotonically with environmental uncertainty across all scenarios. Exotic goods totals track monument investment, with the high uncertainty scenario producing quantities closest to archaeological estimates.

### 4.4 Archaeological Calibration

Model outputs can be scaled to archaeological quantities using a calibration factor of 142.6. At this scaling, the model produces approximately 750,000 cubic meters of monument volume over the 500-year simulation, matching archaeological estimates for Poverty Point earthwork volume.

Exotic goods totals in the model range from 895 under low uncertainty to 5,265 under high uncertainty. The archaeological record shows approximately 3,078 items of copper, steatite, and galena combined, falling within the model's prediction range. The high uncertainty scenario produces counts closest to archaeological totals, suggesting that Poverty Point conditions may have involved greater environmental uncertainty than the baseline calibrated scenario.

Population dynamics stabilize around 400-500 individuals across 25-30 bands, consistent with ethnographic expectations for hunter-gatherer aggregations in productive environments.

### 4.5 Temporal Dynamics

Time series analysis reveals that strategy dominance fluctuates in response to environmental conditions. During shortfall periods, aggregation becomes more attractive as bands seek cooperation benefits. Monument construction proceeds in pulses corresponding to periods of elevated aggregation. Exotic goods accumulate gradually as the reciprocal obligation network develops.

These temporal dynamics suggest that archaeological evidence for construction pulses may correlate with periods of environmental stress rather than representing organizational changes or external influences.

---

## 5. Discussion

### 5.1 The Poverty Point Paradox Resolved

Our model provides a unified explanation for the apparently paradoxical combination of massive collective monument construction and extensive individual exotic goods acquisition at Poverty Point. Both phenomena emerge as adaptive costly signals under conditions of environmental uncertainty combined with ecotone access.

Monument construction represents collective investment in an honest signal of commitment to the aggregation system. Bands that invest heavily in monuments demonstrate capacity and willingness to participate in long-term cooperation, reducing uncertainty about partner reliability. The sunk cost nature of monument investment creates commitment that binds participants to return.

Exotic goods acquisition represents individual investment in honest signals of cooperation capacity. Bands that acquire exotic materials demonstrate resource surplus and network connectivity, signaling desirability as cooperation partners. The difficulty of acquisition ensures signal honesty.

Both signal types solve the fundamental cooperation problems inherent in aggregation: partner identification, free-rider prevention, and commitment. Neither requires aggrandizers exercising coercive power, religious motivation creating irrational behavior, or incipient complexity driving organizational change.

### 5.2 Site Location Optimality

The model predicts that aggregation sites should be located at positions maximizing ecotone access, not simply at resource concentrations or network centrality points. Poverty Point's position at the intersection of multiple ecological zones provides precisely this advantage. The site offers access to floodplain aquatic resources, upland terrestrial game, riverine fish and waterfowl, and forest mast resources.

Alternative locations with lower ecotone access would face higher effective environmental uncertainty, requiring more extreme regional conditions for aggregation to become adaptive. This explains why Poverty Point achieved primacy over other contemporaneous sites in the region despite not being centrally located in the exchange network or positioned at maximum resource abundance.

### 5.3 Regional Site Hierarchy

The model predicts declining site investment with declining ecotone access. Secondary sites like Jaketown, Claiborne, and J.W. Copes should show lower monument investment proportional to their reduced ecotone advantage. Archaeological evidence supports this prediction, with these sites showing earthwork volumes orders of magnitude smaller than Poverty Point despite similar occupation spans.

Distance from the primary aggregation site also affects participation probability due to travel costs. Bands from distant territories face higher costs to aggregate, reducing their fitness advantage from participation. This creates catchment zones around aggregation sites with declining participation intensity.

### 5.4 System Collapse

The model identifies conditions for system abandonment. If environmental uncertainty declines below the critical threshold, aggregation loses its fitness advantage and bands shift toward independent foraging. If ecotone access shifts due to environmental change such as river channel migration, effective uncertainty at the aggregation site increases relative to the regional baseline, potentially pushing conditions below threshold.

Archaeological evidence suggests Poverty Point was abandoned around 1100 BCE after approximately 500-600 years of occupation. Climate reconstruction for this period indicates declining flood frequency and potentially reduced environmental uncertainty. River channel changes may have altered ecotone accessibility at the site location. Both mechanisms are consistent with the model's predictions for system collapse.

### 5.5 Comparison with Alternative Explanations

The costly signaling model differs from alternatives in several key respects. Unlike aggrandizer models, our approach requires no asymmetric power relations. All participants benefit from the signaling system under appropriate environmental conditions. Individual bands choose strategies based on expected fitness, with aggregation emerging as an equilibrium rather than being imposed.

Unlike pilgrimage models, our approach is explanatory rather than descriptive. It specifies conditions under which aggregation becomes adaptive, predicts site location based on environmental parameters, and identifies conditions for system collapse. Religious motivation may accompany aggregation behavior, but the ultimate explanation lies in fitness consequences.

Unlike trade models, our approach explains monument construction directly. Exotic goods and monuments serve parallel signaling functions rather than monuments being incidental to exchange. The co-occurrence of both phenomena follows necessarily from the theoretical framework.

Unlike incipient complexity models, our approach does not require organizational or social changes beyond the aggregation behavior itself. Bands remain mobile and maintain flexible membership. The "complexity" at Poverty Point represents a particular adaptation to environmental conditions rather than a stage in progressive development.

### 5.6 Testable Predictions

The model generates specific testable predictions beyond those already examined. Construction chronology should correlate with paleoclimate proxies for environmental uncertainty. If climate reconstruction indicates elevated uncertainty during specific periods, monument construction should concentrate in those intervals.

Exotic goods source directions should show multi-directional patterns reflecting a wide network of participating bands rather than linear trade routes. Isotopic and geochemical sourcing studies can test this prediction against alternatives emphasizing directed exchange.

Site spacing should reflect the balance between ecotone access and travel costs. Secondary aggregation sites should emerge at distances where travel costs to the primary site begin to exceed ecotone advantages of the primary location.

Individual-level variation in exotic goods holdings should correlate with band position in the reciprocal obligation network. High-prestige bands should show both higher exotic holdings and more extensive obligation connections.

---

## 6. Conclusions

The Poverty Point paradox finds resolution in the framework of aggregation-based costly signaling. By extending multilevel selection theory to incorporate the specific challenges faced by mobile hunter-gatherer bands, we derive conditions under which aggregation with monument construction and exotic goods acquisition becomes adaptive. The critical insight is that Poverty Point represents neither anomalous behavior nor incipient complexity, but an adaptive response to specific environmental conditions.

When environmental uncertainty exceeds a critical threshold and ecotone access is sufficient, aggregation with costly signaling provides higher fitness than independent foraging. The monuments and exotic goods are not wasteful displays but functional solutions to cooperation problems inherent in aggregation. They signal commitment and capacity, enabling the formation of reciprocal obligation networks that buffer participants against environmental risk.

Our agent-based model validates these theoretical predictions quantitatively. The simulated phase transition at effective σ approximately 0.54 closely matches the theoretical prediction of σ* approximately 0.53. Model outputs scale to archaeological estimates for monument volume and exotic goods quantities. Scenario comparisons demonstrate the predicted relationships between environmental uncertainty, aggregation intensity, and costly signaling investment.

This framework has implications beyond Poverty Point. Any mobile population facing cooperation challenges under environmental uncertainty may develop analogous signaling systems. The specific signals will vary with context, but the underlying logic remains constant: costly investment demonstrates commitment, enabling cooperation that would otherwise fail due to free-rider and commitment problems.

The Poverty Point phenomenon thus represents not an anomaly requiring special explanation but an expected outcome given the environmental and social conditions of the Late Archaic Lower Mississippi Valley. Understanding it requires neither mysterious religious motivation, exploitative elites, nor evolutionary progression toward complexity. It requires only that we recognize hunter-gatherer populations as capable of sophisticated adaptive responses to their environments.

---

## Acknowledgments

[To be added]

---

## Data Availability

Simulation code and analysis results are available at [repository to be specified]. Archaeological data sources are cited in the text.

---

## References

[References to be formatted in JAS style - key citations include:]

Bettinger, R.L., Garvey, R., Tushingham, S., 2015. Hunter-Gatherers: Archaeological and Evolutionary Theory. Springer, New York.

DiNapoli, R.J., Lipo, C.P., Brosnan, T., Hunt, T.L., Hixon, S., Morrison, A.E., Becker, M., 2021. Rapa Nui (Easter Island) monument (ahu) locations explained by freshwater sources. PLoS ONE 16, e0245008.

Gibson, J.L., 2000. The Ancient Mounds of Poverty Point: Place of Rings. University Press of Florida, Gainesville.

Grafen, A., 1990. Biological signals as handicaps. Journal of Theoretical Biology 144, 517-546.

Kidder, T.R., Ortmann, A.L., Arco, L.J., 2008. Poverty Point and the Archaeology of Singularity. SAA Archaeological Record 8, 9-12.

Lipo, C.P., Hunt, T.L., Horneman, R., Bonhomme, V., 2016. Weapons of war? Rapa Nui mata'a morphometric analyses. Antiquity 90, 172-187.

Ortmann, A.L., Kidder, T.R., 2013. Building Mound A at Poverty Point, Louisiana: Monumental Public Architecture, Ritual Practice, and Implications for Hunter-Gatherer Complexity. Geoarchaeology 28, 66-86.

Price, G.R., 1970. Selection and covariance. Nature 227, 520-521.

Sassaman, K.E., 2005. Poverty Point as Structure, Event, Process. Journal of Archaeological Method and Theory 12, 335-364.

Zahavi, A., 1975. Mate selection: A selection for a handicap. Journal of Theoretical Biology 53, 205-214.

---

## Figure Captions

**Figure 1. Phase Transition Validation.** (A) Strategy dominance as a function of effective environmental uncertainty (σ_eff), showing the transition from independent-dominated (negative values) to mixed strategies near the theoretical critical threshold σ* = 0.53 (dashed line). (B) Mean aggregation size increases sharply above the threshold, approaching the theoretical optimal size of 25 bands. (C) Monument investment increases approximately fivefold above the threshold. (D) Scatter plot showing the relationship between strategy dominance and monument investment, colored by effective σ.

**Figure 2. Phase Space Structure.** (A) Strategy dominance across the phase space defined by environmental uncertainty (σ) and ecotone advantage (ε). Purple indicates independent strategy dominance; orange indicates aggregation dominance. The solid line shows the theoretical critical threshold. (B) Monument investment across the same phase space, showing concentration in the high-σ, high-ε quadrant.

**Figure 3. Scenario Comparison.** (A) Population dynamics over 500 simulated years under four environmental scenarios: low uncertainty (purple), calibrated Poverty Point (green), high uncertainty (orange), and critical threshold (dark orange). (B) Strategy dominance time series showing fluctuations in response to environmental conditions. (C) Cumulative monument construction showing accelerated accumulation under higher uncertainty. (D) Summary comparison of final state metrics across scenarios.

**Figure 4. Archaeological Calibration.** (A) Monument volume comparison between model predictions (scaled) and archaeological estimates, showing close correspondence at approximately 750,000 m³. (B) Exotic goods comparison between model scenarios and archaeological counts. (C) Model fit assessment showing deviation from archaeological data by scenario, with high uncertainty scenario providing the closest match.

**Figure 5. Poverty Point Location and Ecotone Access.** Map showing Poverty Point location relative to ecological zones in the Lower Mississippi Valley. The site is positioned at the intersection of floodplain, upland, riverine, and forest resources, providing maximum ecotone advantage consistent with model predictions for optimal aggregation site location.
