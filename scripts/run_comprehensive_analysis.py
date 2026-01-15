#!/usr/bin/env python3
"""
Comprehensive Analysis of Poverty Point Integrated Simulation

This script runs systematic analyses to:
1. Map the phase space (σ vs ε)
2. Validate theoretical predictions
3. Compare scenarios to archaeological data
4. Generate publication-quality figures

Results are saved for manuscript integration.
"""

import sys
sys.path.insert(0, '/Users/clipo/PycharmProjects/poverty-point-signaling')

import numpy as np
import json
from pathlib import Path
from datetime import datetime
from dataclasses import asdict

from src.poverty_point.integrated_simulation import IntegratedSimulation
from src.poverty_point.environmental_scenarios import (
    get_scenario, create_critical_threshold_scenario, ShortfallParams,
    EnvironmentalScenario, SCENARIOS
)
from src.poverty_point.parameters import default_parameters, critical_threshold
from src.poverty_point.environment import EnvironmentConfig

# Output directory
OUTPUT_DIR = Path('/Users/clipo/PycharmProjects/poverty-point-signaling/results/analysis')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def run_sigma_sweep(n_points: int = 10, duration: int = 400, n_replicates: int = 3):
    """
    Run simulations across range of σ values.

    Returns detailed results for phase transition analysis.
    """
    print("=" * 60)
    print("SIGMA SWEEP ANALYSIS")
    print("=" * 60)

    sigma_values = np.linspace(0.2, 0.9, n_points)
    results = []

    for i, target_sigma in enumerate(sigma_values):
        print(f"\nσ = {target_sigma:.2f} ({i+1}/{n_points})")

        replicate_results = []
        for rep in range(n_replicates):
            scenario = create_critical_threshold_scenario(target_sigma=target_sigma)
            params = default_parameters(seed=42 + rep)
            params.duration = duration
            params.burn_in = 100

            sim = IntegratedSimulation(
                params=params,
                env_config=scenario.env_config,
                shortfall_params=scenario.shortfall_params,
                seed=42 + rep
            )
            sim_results = sim.run(verbose=False)

            replicate_results.append({
                'target_sigma': float(target_sigma),
                'actual_sigma': float(sim_results.mean_effective_sigma),
                'dominance': float(sim_results.final_strategy_dominance),
                'aggregation_size': float(sim_results.mean_aggregation_size),
                'monument_level': float(sim_results.final_monument_level),
                'total_exotics': int(sim_results.total_exotics),
                'mean_population': float(sim_results.mean_population),
            })

        # Average across replicates
        avg_result = {
            'target_sigma': float(target_sigma),
            'actual_sigma': float(np.mean([r['actual_sigma'] for r in replicate_results])),
            'actual_sigma_std': float(np.std([r['actual_sigma'] for r in replicate_results])),
            'dominance': float(np.mean([r['dominance'] for r in replicate_results])),
            'dominance_std': float(np.std([r['dominance'] for r in replicate_results])),
            'aggregation_size': float(np.mean([r['aggregation_size'] for r in replicate_results])),
            'aggregation_size_std': float(np.std([r['aggregation_size'] for r in replicate_results])),
            'monument_level': float(np.mean([r['monument_level'] for r in replicate_results])),
            'monument_level_std': float(np.std([r['monument_level'] for r in replicate_results])),
            'total_exotics': float(np.mean([r['total_exotics'] for r in replicate_results])),
            'mean_population': float(np.mean([r['mean_population'] for r in replicate_results])),
            'replicates': replicate_results,
        }
        results.append(avg_result)

        print(f"  σ_eff={avg_result['actual_sigma']:.3f} ± {avg_result['actual_sigma_std']:.3f}")
        print(f"  dominance={avg_result['dominance']:+.2f} ± {avg_result['dominance_std']:.2f}")
        print(f"  aggregation={avg_result['aggregation_size']:.1f} bands")
        print(f"  monument={avg_result['monument_level']:.0f}")

    return results


def run_phase_space_analysis(n_sigma: int = 8, n_epsilon: int = 6,
                              duration: int = 300):
    """
    Map the full phase space of σ vs ε.

    This validates the theoretical prediction that:
    - High σ + high ε → aggregation dominates
    - Low σ or low ε → independence dominates
    """
    print("\n" + "=" * 60)
    print("PHASE SPACE ANALYSIS (σ × ε)")
    print("=" * 60)

    sigma_values = np.linspace(0.3, 0.8, n_sigma)
    epsilon_values = np.linspace(0.1, 0.5, n_epsilon)

    results = []

    for i, target_sigma in enumerate(sigma_values):
        for j, epsilon in enumerate(epsilon_values):
            print(f"σ={target_sigma:.2f}, ε={epsilon:.2f} ({i*n_epsilon + j + 1}/{n_sigma*n_epsilon})")

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
                n=25,  # Expected aggregation size
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

    return results


def run_scenario_comparison(duration: int = 500):
    """
    Compare pre-defined scenarios to understand regime differences.
    """
    print("\n" + "=" * 60)
    print("SCENARIO COMPARISON")
    print("=" * 60)

    results = {}

    for name in ['low', 'poverty_point', 'high', 'critical']:
        print(f"\nRunning {name} scenario...")
        scenario = get_scenario(name)

        params = default_parameters(seed=42)
        params.duration = duration
        params.burn_in = 100

        sim = IntegratedSimulation(
            params=params,
            env_config=scenario.env_config,
            shortfall_params=scenario.shortfall_params,
            seed=42
        )
        sim_results = sim.run(verbose=True)

        # Extract time series for analysis
        yearly_data = []
        for state in sim_results.yearly_states:
            yearly_data.append({
                'year': int(state.year),
                'population': int(state.total_population),
                'dominance': float(state.strategy_dominance),
                'aggregation_size': int(state.aggregation_size),
                'monument_level': float(state.monument_level),
                'effective_sigma': float(state.effective_sigma),
                'in_shortfall': bool(state.in_shortfall),
            })

        results[name] = {
            'scenario_name': scenario.name,
            'description': scenario.description,
            'expected_sigma_range': [float(x) for x in scenario.expected_sigma_range],
            'expected_epsilon': float(scenario.expected_epsilon),
            'shortfall_interval': float(scenario.shortfall_params.mean_interval),
            'shortfall_magnitude': float(scenario.shortfall_params.magnitude_mean),
            'final_dominance': float(sim_results.final_strategy_dominance),
            'mean_aggregation': float(sim_results.mean_aggregation_size),
            'final_monument': float(sim_results.final_monument_level),
            'total_exotics': int(sim_results.total_exotics),
            'mean_sigma': float(sim_results.mean_effective_sigma),
            'mean_population': float(sim_results.mean_population),
            'time_series': yearly_data,
        }

    return results


def run_poverty_point_calibration(duration: int = 500, n_replicates: int = 5):
    """
    Run calibrated Poverty Point scenario and compare to archaeological record.

    Archaeological targets:
    - Total monument volume: ~750,000 m³
    - Duration: ~500 years
    - Construction rate: ~1,500 m³/year
    - Exotic goods: copper (155), steatite (2221), galena (702)
    """
    print("\n" + "=" * 60)
    print("POVERTY POINT CALIBRATION")
    print("=" * 60)

    scenario = get_scenario('poverty_point')

    all_results = []
    for rep in range(n_replicates):
        print(f"\nReplicate {rep+1}/{n_replicates}")

        params = default_parameters(seed=42 + rep)
        params.duration = duration
        params.burn_in = 50

        sim = IntegratedSimulation(
            params=params,
            env_config=scenario.env_config,
            shortfall_params=scenario.shortfall_params,
            seed=42 + rep
        )
        sim_results = sim.run(verbose=False)

        all_results.append({
            'final_monument': float(sim_results.final_monument_level),
            'total_exotics': sim_results.total_exotics,
            'mean_aggregation': float(sim_results.mean_aggregation_size),
            'final_dominance': float(sim_results.final_strategy_dominance),
            'mean_sigma': float(sim_results.mean_effective_sigma),
            'mean_population': float(sim_results.mean_population),
        })

    # Calculate summary statistics
    summary = {
        'n_replicates': n_replicates,
        'duration': duration,
        'monument_mean': float(np.mean([r['final_monument'] for r in all_results])),
        'monument_std': float(np.std([r['final_monument'] for r in all_results])),
        'exotics_mean': float(np.mean([r['total_exotics'] for r in all_results])),
        'aggregation_mean': float(np.mean([r['mean_aggregation'] for r in all_results])),
        'dominance_mean': float(np.mean([r['final_dominance'] for r in all_results])),
        'sigma_mean': float(np.mean([r['mean_sigma'] for r in all_results])),
        'population_mean': float(np.mean([r['mean_population'] for r in all_results])),
        'replicates': all_results,
    }

    # Archaeological comparison
    print("\n--- Archaeological Comparison ---")
    print(f"Monument (model): {summary['monument_mean']:.0f} ± {summary['monument_std']:.0f}")
    print(f"Monument (archaeological): ~750,000 m³")

    # Note: Model monument units are arbitrary, need scaling
    scaling_factor = 750000 / summary['monument_mean'] if summary['monument_mean'] > 0 else 1
    print(f"Scaling factor: {scaling_factor:.1f}")

    summary['scaling_factor'] = scaling_factor
    summary['archaeological_monument'] = 750000
    summary['archaeological_exotics'] = {'copper': 155, 'steatite': 2221, 'galena': 702}

    return summary


def save_results(sigma_sweep, phase_space, scenarios, calibration):
    """Save all results to JSON files."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Save sigma sweep
    with open(OUTPUT_DIR / f'sigma_sweep_{timestamp}.json', 'w') as f:
        json.dump(sigma_sweep, f, indent=2)

    # Save phase space
    with open(OUTPUT_DIR / f'phase_space_{timestamp}.json', 'w') as f:
        json.dump(phase_space, f, indent=2)

    # Save scenario comparison
    with open(OUTPUT_DIR / f'scenarios_{timestamp}.json', 'w') as f:
        json.dump(scenarios, f, indent=2)

    # Save calibration
    with open(OUTPUT_DIR / f'calibration_{timestamp}.json', 'w') as f:
        json.dump(calibration, f, indent=2)

    # Save combined summary
    summary = {
        'timestamp': timestamp,
        'sigma_sweep_n': len(sigma_sweep),
        'phase_space_n': len(phase_space),
        'scenarios': list(scenarios.keys()),
        'calibration_replicates': calibration['n_replicates'],
    }
    with open(OUTPUT_DIR / f'analysis_summary_{timestamp}.json', 'w') as f:
        json.dump(summary, f, indent=2)

    print(f"\nResults saved to: {OUTPUT_DIR}")
    return timestamp


def main():
    """Run comprehensive analysis."""
    print("=" * 60)
    print("POVERTY POINT ABM COMPREHENSIVE ANALYSIS")
    print(f"Started: {datetime.now().isoformat()}")
    print("=" * 60)

    # Run analyses
    sigma_sweep = run_sigma_sweep(n_points=10, duration=400, n_replicates=3)
    phase_space = run_phase_space_analysis(n_sigma=6, n_epsilon=5, duration=300)
    scenarios = run_scenario_comparison(duration=500)
    calibration = run_poverty_point_calibration(duration=500, n_replicates=5)

    # Save results
    timestamp = save_results(sigma_sweep, phase_space, scenarios, calibration)

    # Print summary
    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE")
    print("=" * 60)

    print("\nKey Findings:")

    # Find critical threshold crossing
    for i, r in enumerate(sigma_sweep[:-1]):
        if r['dominance'] < 0 and sigma_sweep[i+1]['dominance'] > -0.5:
            print(f"\n1. Phase transition detected:")
            print(f"   σ_eff = {r['actual_sigma']:.3f} → {sigma_sweep[i+1]['actual_sigma']:.3f}")
            print(f"   dominance: {r['dominance']:+.2f} → {sigma_sweep[i+1]['dominance']:+.2f}")
            break

    print(f"\n2. Scenario comparison:")
    for name, data in scenarios.items():
        print(f"   {name}: σ={data['mean_sigma']:.3f}, dom={data['final_dominance']:+.2f}")

    print(f"\n3. Poverty Point calibration:")
    print(f"   Monument: {calibration['monument_mean']:.0f} (×{calibration['scaling_factor']:.0f} = 750,000 m³)")
    print(f"   Exotics: {calibration['exotics_mean']:.0f}")
    print(f"   Population: {calibration['population_mean']:.0f}")

    print(f"\nResults saved with timestamp: {timestamp}")

    return {
        'sigma_sweep': sigma_sweep,
        'phase_space': phase_space,
        'scenarios': scenarios,
        'calibration': calibration,
        'timestamp': timestamp,
    }


if __name__ == "__main__":
    results = main()
