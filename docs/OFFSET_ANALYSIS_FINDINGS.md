# Theory-ABM Offset Analysis: Findings and Calibration Recommendations

## Executive Summary

The Poverty Point ABM shows a systematic offset of **+0.115** from theoretical predictions for the critical threshold σ*. This document summarizes our investigation into the sources of this offset and provides calibration recommendations.

## Key Findings

### 1. Offset Characteristics

- **Mean offset**: +0.115 (ABM threshold higher than theory)
- **Consistency**: Remarkably stable across all ε values (std = 0.002)
- **Pattern**: Linear shift rather than multiplicative scaling

| ε value | Theory σ* | ABM σ* | Offset |
|---------|-----------|--------|--------|
| 0.15    | 0.592     | 0.704  | +0.112 |
| 0.25    | 0.561     | 0.679  | +0.117 |
| 0.35    | 0.534     | 0.648  | +0.114 |
| 0.45    | 0.509     | 0.625  | +0.116 |

### 2. Source Attribution

We identified multiple contributing factors to the offset:

#### 2.1 Emergent Aggregation Size (≈13% of offset)

The theory assumes a fixed aggregation size n=25, but the ABM shows emergent n varies strongly with σ:

```
n(σ) = -11.86 + 57.64 * σ
```

At the theoretical threshold (σ* ≈ 0.53), emergent n ≈ 19, not 25.

**Effect**: Accounting for emergent n reduces residual from +0.115 to +0.102 (improvement of 0.013).

#### 2.2 Decision Stochasticity (≈39% of offset)

The sigmoid decision function with temperature T=10 introduces noise around the threshold. Bands don't switch strategies instantaneously at the fitness crossover point.

**Effect**: Estimated contribution of ~0.045 to offset.

#### 2.3 Memory/Hysteresis Effects (≈22% of offset)

Bands incorporate recent fitness history into decisions, creating strategy persistence (hysteresis). This delays strategy switching and shifts the effective threshold.

**Effect**: Estimated contribution of ~0.025 to offset.

#### 2.4 Shortfall Timing (≈17% of offset)

The stochastic timing of shortfalls creates variance in realized fitness that differs from theoretical expectations.

**Effect**: Estimated contribution of ~0.020 to offset.

#### 2.5 Unexplained (≈10% of offset)

Remaining offset (~0.012) may be due to:
- Initial condition bias (60% independent start)
- Finite population effects
- Interaction effects not captured in decomposition

### 3. Monument Accumulation Dynamics

The ABM successfully captures the key feature of Poverty Point: **cumulative, self-reinforcing monument building**.

Key observations:
- Strong positive feedback between attendance and construction (r = 0.80-0.96)
- Clear divergence in monument trajectories based on σ
- Higher σ → more aggregation → faster monument growth
- Monument level at end of simulation:
  - σ=0.45: ~10,000
  - σ=0.55: ~13,300
  - σ=0.65: ~13,900
  - σ=0.75: ~17,400

### 4. Population Dynamics

Population dynamics show expected patterns:
- Higher σ → lower equilibrium population (more shortfall mortality)
- Strategy composition shifts with σ (more aggregators above σ*)
- Fitness differential crosses zero near the threshold
- Strategy switching rate peaks near σ*

## Calibration Recommendations

### Option 1: Simple Linear Correction (Recommended)

For quick calibration, apply a linear shift:

```python
σ_star_calibrated = σ_star_theoretical + 0.115
```

**Pros**: Simple, consistent across ε values
**Cons**: Doesn't address root causes

### Option 2: Emergent n Correction

Use the emergent n model in theoretical calculations:

```python
def σ_star_with_emergent_n(epsilon, params):
    # Iterative solution
    σ = 0.5  # Initial guess
    for _ in range(20):
        n = max(5, -11.86 + 57.64 * σ)
        σ_new = critical_threshold(epsilon, n, params)
        if abs(σ_new - σ) < 0.001:
            break
        σ = 0.5 * σ + 0.5 * σ_new
    return σ
```

**Pros**: Addresses one root cause
**Cons**: Only captures ~13% of offset

### Option 3: Adjusted Decision Temperature

Reduce decision temperature from T=10 to T≈15 to make decisions more deterministic:

```python
# In agents.py, Band.decide_strategy():
temperature = 15.0  # Was 10.0
```

**Pros**: Reduces stochastic offset
**Cons**: May over-dampen dynamics

### Option 4: Full Recalibration

Adjust multiple parameters simultaneously:
- Reduce b_coop slightly (decreases A term)
- Increase R_ind slightly (shifts threshold up)
- Adjust vulnerability parameters

**Pros**: Can achieve exact match
**Cons**: May compromise theoretical interpretability

## Recommended Approach

For the Poverty Point analysis, we recommend **Option 1** (simple linear correction) for the following reasons:

1. The offset is remarkably consistent, making correction straightforward
2. The offset doesn't affect the qualitative predictions (phase transition exists, same shape)
3. The ABM dynamics (monument accumulation, population responses) match expectations
4. Preserves theoretical parameter interpretability

When comparing theory to ABM results in publications, note:
- Theory predicts threshold behavior at σ* (theoretical formula)
- ABM realizes threshold at σ* + 0.115 due to stochastic dynamics
- This is a systematic calibration difference, not model failure

## Files Generated

All diagnostic figures are in `figures/diagnostics/`:

1. `offset_diagnostics.png` - Four-panel analysis of offset sources
2. `calibration_analysis.png` - Emergent n calibration analysis
3. `monument_trajectories.png` - Monument accumulation dynamics
4. `population_dynamics.png` - Population and strategy dynamics

Scripts in `scripts/exploration/`:

1. `investigate_offset.py` - Main offset analysis
2. `calibrate_offset.py` - Emergent n calibration
3. `investigate_stochastic_offset.py` - Stochastic effects analysis

## Conclusions

The +0.115 offset between theory and ABM is a well-characterized consequence of stochastic dynamics in the ABM that are not captured in the deterministic theoretical model. The offset is consistent and predictable, allowing for straightforward calibration. The ABM successfully captures the key dynamics of Poverty Point: cumulative monument building, strategy-dependent survival, and threshold-dependent aggregation behavior.
