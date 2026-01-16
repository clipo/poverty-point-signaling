#!/usr/bin/env python3
"""
Run Fine-Grained Phase Space Analysis

This script runs the phase space simulation with a finer grid to better
show variation across both σ and ε axes.
"""

import sys
sys.path.insert(0, '/Users/clipo/PycharmProjects/poverty-point-signaling')

import numpy as np
import json
from pathlib import Path
from datetime import datetime

from src.poverty_point.integrated_simulation import IntegratedSimulation
from src.poverty_point.environmental_scenarios import create_critical_threshold_scenario
from src.poverty_point.parameters import default_parameters, critical_threshold

# Output directory
OUTPUT_DIR = Path('/Users/clipo/PycharmProjects/poverty-point-signaling/results/analysis')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def run_fine_phase_space(n_sigma: int = 12, n_epsilon: int = 10, duration: int = 300):
    """
    Run phase space analysis with finer grid.
    """
    print("=" * 60)
    print(f"FINE PHASE SPACE ANALYSIS ({n_sigma} × {n_epsilon} grid)")
    print("=" * 60)

    sigma_values = np.linspace(0.25, 0.85, n_sigma)
    epsilon_values = np.linspace(0.05, 0.50, n_epsilon)

    results = []
    total = n_sigma * n_epsilon

    for i, target_sigma in enumerate(sigma_values):
        for j, epsilon in enumerate(epsilon_values):
            idx = i * n_epsilon + j + 1
            print(f"σ={target_sigma:.2f}, ε={epsilon:.2f} ({idx}/{total})")

            scenario = create_critical_threshold_scenario(target_sigma=target_sigma)

            # Modify ecotone parameters
            scenario.env_config.ecotone_base_productivity = 0.5 + epsilon * 0.4
            scenario.expected_epsilon = epsilon

            params = default_parameters(seed=42)
            params.duration = duration
            params.burn_in = 50

            sim = IntegratedSimulation(
                params=params,
                env_config=scenario.env_config,
                shortfall_params=scenario.shortfall_params,
                seed=42
            )

            # Override ecotone advantage
            sim.aggregation_site.ecotone_advantage = epsilon

            sim_results = sim.run(verbose=False)

            # Calculate theoretical prediction
            sigma_star = critical_threshold(
                epsilon=epsilon,
                n=25,
                params=params
            )

            results.append({
                'target_sigma': float(target_sigma),
                'epsilon': float(epsilon),
                'actual_sigma': float(sim_results.mean_effective_sigma),
                'dominance': float(sim_results.final_strategy_dominance),
                'aggregation_size': float(sim_results.mean_aggregation_size),
                'monument_level': float(sim_results.final_monument_level),
                'sigma_star_theoretical': float(sigma_star),
                'above_threshold': bool(float(sim_results.mean_effective_sigma) > float(sigma_star)),
            })

    # Save results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = OUTPUT_DIR / f'phase_space_fine_{timestamp}.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to: {output_file}")

    return results


if __name__ == "__main__":
    results = run_fine_phase_space(n_sigma=12, n_epsilon=10, duration=300)
    print(f"\nCompleted {len(results)} simulation runs")
