"""
Investigate the offset between theoretical predictions and ABM results.

The ABM shows σ* approximately +0.10 higher than theory predicts.
This script investigates potential sources of this discrepancy.

Potential sources:
1. Stochastic dynamics not captured in deterministic theory
2. Non-equilibrium effects (burn-in period, strategy switching)
3. Emergent aggregation size differs from assumed n=25
4. Memory effects in band decision-making
5. Interaction between shortfall timing and aggregation decisions
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from poverty_point.core_simulation import PovertyPointSimulation, run_single_simulation
from poverty_point.parameters import (
    default_parameters, critical_threshold, W_aggregator, W_independent,
    cooperation_benefit
)
from poverty_point.agents import Strategy


def analyze_emergent_n(sigma: float, epsilon: float, n_runs: int = 10,
                       duration: int = 400) -> dict:
    """
    Analyze what aggregation size actually emerges in ABM.

    Theory assumes n=25, but emergent n may differ.
    """
    all_n = []
    all_dominance = []

    for seed in range(n_runs):
        results = run_single_simulation(
            sigma=sigma, epsilon=epsilon, seed=seed,
            duration=duration, verbose=False
        )

        # Get aggregation sizes from post-burn-in period
        for state in results.yearly_states[100:]:
            all_n.append(state.aggregation_size)

        all_dominance.append(results.final_strategy_dominance)

    return {
        'sigma': sigma,
        'epsilon': epsilon,
        'mean_n': np.mean(all_n),
        'std_n': np.std(all_n),
        'median_n': np.median(all_n),
        'mean_dominance': np.mean(all_dominance),
        'theoretical_sigma_star': critical_threshold(epsilon, 25, default_parameters()),
        'theoretical_sigma_star_at_emergent_n': critical_threshold(
            epsilon, np.mean(all_n), default_parameters()
        )
    }


def analyze_fitness_realization(sigma: float, epsilon: float, n_runs: int = 10,
                                duration: int = 400) -> dict:
    """
    Compare realized fitness in ABM with theoretical fitness.

    Theory assumes deterministic fitness; ABM has stochastic realization.
    """
    agg_fitness_realized = []
    ind_fitness_realized = []

    params = default_parameters(sigma=sigma, epsilon=epsilon)

    for seed in range(n_runs):
        sim = PovertyPointSimulation(params)
        sim.params.duration = duration
        sim.params.seed = seed
        sim.rng = np.random.default_rng(seed)

        results = sim.run(verbose=False)

        # Collect fitness from post-burn-in period
        for state in results.yearly_states[100:]:
            if state.mean_fitness_aggregators > 0:
                agg_fitness_realized.append(state.mean_fitness_aggregators)
            if state.mean_fitness_independents > 0:
                ind_fitness_realized.append(state.mean_fitness_independents)

    # Calculate theoretical fitness
    n_theory = 25
    W_agg_theory = W_aggregator(sigma, epsilon, n_theory, params)
    W_ind_theory = W_independent(sigma, params)

    return {
        'sigma': sigma,
        'epsilon': epsilon,
        'W_agg_theory': W_agg_theory,
        'W_ind_theory': W_ind_theory,
        'W_agg_realized_mean': np.mean(agg_fitness_realized) if agg_fitness_realized else 0,
        'W_agg_realized_std': np.std(agg_fitness_realized) if agg_fitness_realized else 0,
        'W_ind_realized_mean': np.mean(ind_fitness_realized) if ind_fitness_realized else 0,
        'W_ind_realized_std': np.std(ind_fitness_realized) if ind_fitness_realized else 0,
        'theory_diff': W_agg_theory - W_ind_theory,
        'realized_diff': (np.mean(agg_fitness_realized) - np.mean(ind_fitness_realized)
                         if agg_fitness_realized and ind_fitness_realized else 0)
    }


def analyze_strategy_switching(sigma: float, epsilon: float, n_runs: int = 5,
                               duration: int = 400) -> dict:
    """
    Analyze how frequently bands switch strategies.

    High switching rates indicate non-equilibrium dynamics.
    """
    switch_rates = []

    params = default_parameters(sigma=sigma, epsilon=epsilon)

    for seed in range(n_runs):
        sim = PovertyPointSimulation(params)
        sim.params.duration = duration
        sim.params.seed = seed
        sim.rng = np.random.default_rng(seed)

        sim.run(verbose=False)

        # Count strategy switches per band
        for band in sim.bands:
            if len(band.strategy_history) > 1:
                switches = sum(1 for i in range(1, len(band.strategy_history))
                              if band.strategy_history[i] != band.strategy_history[i-1])
                rate = switches / (len(band.strategy_history) - 1)
                switch_rates.append(rate)

    return {
        'sigma': sigma,
        'epsilon': epsilon,
        'mean_switch_rate': np.mean(switch_rates),
        'std_switch_rate': np.std(switch_rates),
        'max_switch_rate': np.max(switch_rates) if switch_rates else 0
    }


def find_empirical_threshold_precise(epsilon: float, n_runs: int = 20,
                                     duration: int = 400) -> dict:
    """
    Find empirical threshold with higher precision using binary search.
    """
    # Binary search for threshold
    sigma_low = 0.3
    sigma_high = 0.9

    results = []

    for _ in range(8):  # 8 iterations gives ~0.002 precision
        sigma_mid = (sigma_low + sigma_high) / 2

        dominances = []
        for seed in range(n_runs):
            res = run_single_simulation(
                sigma=sigma_mid, epsilon=epsilon, seed=seed,
                duration=duration, verbose=False
            )
            dominances.append(res.final_strategy_dominance)

        mean_dom = np.mean(dominances)
        results.append({
            'sigma': sigma_mid,
            'dominance': mean_dom,
            'std': np.std(dominances)
        })

        if mean_dom < 0:
            sigma_low = sigma_mid
        else:
            sigma_high = sigma_mid

    sigma_star_empirical = (sigma_low + sigma_high) / 2
    sigma_star_theory = critical_threshold(epsilon, 25, default_parameters())

    return {
        'epsilon': epsilon,
        'sigma_star_empirical': sigma_star_empirical,
        'sigma_star_theory': sigma_star_theory,
        'offset': sigma_star_empirical - sigma_star_theory,
        'search_results': results
    }


def create_offset_diagnostic_figure(output_dir: str = "figures/diagnostics"):
    """
    Create comprehensive diagnostic figure for offset analysis.
    """
    os.makedirs(output_dir, exist_ok=True)

    fig, axes = plt.subplots(2, 2, figsize=(14, 12))

    # ============ Panel A: Emergent n vs assumed n ============
    ax1 = axes[0, 0]

    sigma_values = [0.4, 0.5, 0.6, 0.7]
    epsilon_values = [0.2, 0.35]

    for eps in epsilon_values:
        emergent_n = []
        for sig in sigma_values:
            result = analyze_emergent_n(sig, eps, n_runs=5, duration=300)
            emergent_n.append(result['mean_n'])

        ax1.plot(sigma_values, emergent_n, 'o-', label=f'ε={eps}')

    ax1.axhline(25, color='red', linestyle='--', label='Theoretical n=25')
    ax1.set_xlabel('Environmental Uncertainty (σ)')
    ax1.set_ylabel('Emergent Aggregation Size (n)')
    ax1.set_title('A. Emergent vs Assumed Aggregation Size')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # ============ Panel B: Realized vs Theoretical Fitness ============
    ax2 = axes[0, 1]

    sigma_test = 0.55
    epsilon_test = 0.35

    fitness_data = analyze_fitness_realization(sigma_test, epsilon_test, n_runs=10, duration=300)

    categories = ['Aggregator\n(Theory)', 'Aggregator\n(ABM)',
                  'Independent\n(Theory)', 'Independent\n(ABM)']
    values = [
        fitness_data['W_agg_theory'],
        fitness_data['W_agg_realized_mean'],
        fitness_data['W_ind_theory'],
        fitness_data['W_ind_realized_mean']
    ]
    errors = [0, fitness_data['W_agg_realized_std'], 0, fitness_data['W_ind_realized_std']]
    colors = ['orange', 'darkorange', 'purple', 'darkviolet']

    bars = ax2.bar(categories, values, yerr=errors, color=colors, capsize=5)
    ax2.set_ylabel('Fitness')
    ax2.set_title(f'B. Theoretical vs Realized Fitness\n(σ={sigma_test}, ε={epsilon_test})')
    ax2.grid(True, alpha=0.3, axis='y')

    # Add difference annotation
    theory_diff = fitness_data['theory_diff']
    realized_diff = fitness_data['realized_diff']
    ax2.text(0.95, 0.95, f'Theory diff: {theory_diff:+.3f}\nRealized diff: {realized_diff:+.3f}',
             transform=ax2.transAxes, ha='right', va='top', fontsize=10,
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    # ============ Panel C: Strategy Switching Rates ============
    ax3 = axes[1, 0]

    switch_data = []
    sigma_range = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8]

    for sig in sigma_range:
        result = analyze_strategy_switching(sig, 0.35, n_runs=3, duration=300)
        switch_data.append(result)

    switch_rates = [d['mean_switch_rate'] for d in switch_data]
    switch_stds = [d['std_switch_rate'] for d in switch_data]

    ax3.errorbar(sigma_range, switch_rates, yerr=switch_stds, fmt='o-', capsize=5)
    ax3.set_xlabel('Environmental Uncertainty (σ)')
    ax3.set_ylabel('Strategy Switching Rate (per year)')
    ax3.set_title('C. Strategy Switching Frequency')
    ax3.grid(True, alpha=0.3)

    # Mark theoretical threshold
    params = default_parameters()
    sigma_star = critical_threshold(0.35, 25, params)
    ax3.axvline(sigma_star, color='blue', linestyle='--', alpha=0.5,
                label=f'σ* theory = {sigma_star:.2f}')
    ax3.legend()

    # ============ Panel D: Precise Threshold Comparison ============
    ax4 = axes[1, 1]

    print("Finding precise thresholds (this may take a few minutes)...")
    epsilon_test_values = [0.15, 0.25, 0.35, 0.45]
    precise_results = []

    for eps in epsilon_test_values:
        print(f"  ε={eps}...")
        result = find_empirical_threshold_precise(eps, n_runs=10, duration=300)
        precise_results.append(result)

    theory_thresholds = [r['sigma_star_theory'] for r in precise_results]
    empirical_thresholds = [r['sigma_star_empirical'] for r in precise_results]
    offsets = [r['offset'] for r in precise_results]

    ax4.scatter(theory_thresholds, empirical_thresholds, s=100, c='purple')

    # Perfect agreement line
    max_val = max(max(theory_thresholds), max(empirical_thresholds)) + 0.05
    min_val = min(min(theory_thresholds), min(empirical_thresholds)) - 0.05
    ax4.plot([min_val, max_val], [min_val, max_val], 'k--', alpha=0.5,
             label='Perfect agreement')

    # Offset line
    mean_offset = np.mean(offsets)
    ax4.plot([min_val, max_val], [min_val + mean_offset, max_val + mean_offset],
             'r-', alpha=0.5, label=f'Mean offset = {mean_offset:+.3f}')

    for i, eps in enumerate(epsilon_test_values):
        ax4.annotate(f'ε={eps}', (theory_thresholds[i], empirical_thresholds[i]),
                     textcoords='offset points', xytext=(5, 5), fontsize=9)

    ax4.set_xlabel('Theoretical σ*')
    ax4.set_ylabel('Empirical σ* (ABM)')
    ax4.set_title('D. Precise Threshold Comparison')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    ax4.set_aspect('equal')

    plt.tight_layout()

    # Save
    fig.savefig(os.path.join(output_dir, 'offset_diagnostics.png'),
                dpi=150, bbox_inches='tight', facecolor='white')
    fig.savefig(os.path.join(output_dir, 'offset_diagnostics.pdf'),
                bbox_inches='tight', facecolor='white')
    plt.close(fig)

    print(f"\nDiagnostic figure saved to {output_dir}/offset_diagnostics.png")

    # Print summary
    print("\n" + "="*60)
    print("OFFSET ANALYSIS SUMMARY")
    print("="*60)
    print(f"\nMean offset: {mean_offset:+.3f}")
    print(f"Std offset:  {np.std(offsets):.3f}")
    print("\nPer-epsilon results:")
    for r in precise_results:
        print(f"  ε={r['epsilon']:.2f}: theory={r['sigma_star_theory']:.3f}, "
              f"ABM={r['sigma_star_empirical']:.3f}, offset={r['offset']:+.3f}")

    return precise_results


if __name__ == "__main__":
    results = create_offset_diagnostic_figure()
