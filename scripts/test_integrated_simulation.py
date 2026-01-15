#!/usr/bin/env python3
"""
Test script for integrated simulation with environmental scenarios.

This script tests the integrated simulation under different environmental
conditions to verify that:
1. Higher σ environments lead to aggregation dominance
2. Lower σ environments favor independence
3. Poverty Point conditions produce sustained monument building
"""

import sys
sys.path.insert(0, '/Users/clipo/PycharmProjects/poverty-point-signaling')

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from src.poverty_point.integrated_simulation import IntegratedSimulation
from src.poverty_point.environmental_scenarios import (
    get_scenario, list_scenarios, create_critical_threshold_scenario,
    ShortfallParams, EnvironmentalScenario
)
from src.poverty_point.parameters import default_parameters
from src.poverty_point.environment import EnvironmentConfig


def run_scenario_test(scenario_name: str, duration: int = 400, seed: int = 42):
    """Run simulation with a specific scenario."""
    scenario = get_scenario(scenario_name)

    print(f"\n{'='*60}")
    print(f"Testing: {scenario.name}")
    print(f"Description: {scenario.description}")
    print(f"Expected σ: {scenario.expected_sigma_range[0]:.2f} - "
          f"{scenario.expected_sigma_range[1]:.2f}")
    print(f"{'='*60}")

    # Create simulation with scenario config
    params = default_parameters(seed=seed)
    params.duration = duration
    params.burn_in = 50

    sim = IntegratedSimulation(
        params=params,
        env_config=scenario.env_config,
        seed=seed
    )

    # Override shortfall generation with scenario parameters
    sim.shortfall_params = scenario.shortfall_params

    results = sim.run(verbose=True)

    return results, scenario


def run_sigma_sweep(sigma_values: list, duration: int = 300, seed: int = 42):
    """Run simulations across a range of σ values."""
    results_list = []

    for target_sigma in sigma_values:
        scenario = create_critical_threshold_scenario(target_sigma=target_sigma)

        params = default_parameters(seed=seed)
        params.duration = duration
        params.burn_in = 50

        sim = IntegratedSimulation(
            params=params,
            env_config=scenario.env_config,
            seed=seed
        )

        results = sim.run(verbose=False)

        results_list.append({
            'target_sigma': target_sigma,
            'actual_sigma': results.mean_effective_sigma,
            'dominance': results.final_strategy_dominance,
            'monument': results.final_monument_level,
            'aggregation': results.mean_aggregation_size,
            'exotics': results.total_exotics,
        })

        print(f"σ={target_sigma:.2f}: dominance={results.final_strategy_dominance:.2f}, "
              f"monuments={results.final_monument_level:.0f}")

    return results_list


def plot_results(yearly_states, scenario_name: str, output_dir: Path = None):
    """Plot time series from simulation."""
    years = [s.year for s in yearly_states]
    population = [s.total_population for s in yearly_states]
    dominance = [s.strategy_dominance for s in yearly_states]
    monuments = [s.monument_level for s in yearly_states]
    sigma = [s.effective_sigma for s in yearly_states]
    shortfall = [1 if s.in_shortfall else 0 for s in yearly_states]

    fig, axes = plt.subplots(4, 1, figsize=(12, 10), sharex=True)

    # Population
    ax = axes[0]
    ax.plot(years, population, 'b-', linewidth=1)
    ax.set_ylabel('Population')
    ax.set_title(f'{scenario_name} - Simulation Results')

    # Strategy dominance
    ax = axes[1]
    ax.plot(years, dominance, 'g-', linewidth=1)
    ax.axhline(y=0, color='k', linestyle='--', alpha=0.3)
    ax.set_ylabel('Strategy Dominance\n(+ = aggregator)')
    ax.set_ylim(-1.1, 1.1)

    # Add shortfall markers
    shortfall_years = [y for y, s in zip(years, shortfall) if s]
    ax.scatter(shortfall_years, [1.0] * len(shortfall_years),
               c='red', marker='v', s=20, alpha=0.5, label='Shortfall')
    ax.legend(loc='upper right')

    # Monument level
    ax = axes[2]
    ax.plot(years, monuments, 'purple', linewidth=1)
    ax.set_ylabel('Monument Level')

    # Effective sigma
    ax = axes[3]
    ax.plot(years, sigma, 'orange', linewidth=1)
    ax.set_ylabel('Effective σ')
    ax.set_xlabel('Year')

    plt.tight_layout()

    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f'integrated_sim_{scenario_name.lower().replace(" ", "_")}.png'
        plt.savefig(output_path, dpi=150)
        print(f"Saved plot to: {output_path}")

    plt.show()


def main():
    """Main test routine."""
    print("Testing Integrated Simulation")
    print("=" * 60)

    # List available scenarios
    list_scenarios()

    output_dir = Path('/Users/clipo/PycharmProjects/poverty-point-signaling/figures/simulations')

    # Test each scenario
    scenarios_to_test = ['low', 'poverty_point', 'high']

    all_results = {}
    for scenario_name in scenarios_to_test:
        results, scenario = run_scenario_test(scenario_name, duration=400, seed=42)
        all_results[scenario_name] = results

        # Plot results
        plot_results(results.yearly_states, scenario.name, output_dir)

    # Summary comparison
    print("\n" + "=" * 60)
    print("COMPARISON SUMMARY")
    print("=" * 60)
    print(f"{'Scenario':<20} {'Dom':>8} {'Agg Size':>10} {'Monument':>10} {'σ_eff':>8}")
    print("-" * 60)

    for name, results in all_results.items():
        print(f"{name:<20} {results.final_strategy_dominance:>8.2f} "
              f"{results.mean_aggregation_size:>10.1f} "
              f"{results.final_monument_level:>10.0f} "
              f"{results.mean_effective_sigma:>8.3f}")

    # σ sweep test
    print("\n" + "=" * 60)
    print("SIGMA SWEEP TEST")
    print("=" * 60)

    sigma_values = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
    sweep_results = run_sigma_sweep(sigma_values, duration=300, seed=42)

    # Plot σ sweep
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))

    sigmas = [r['target_sigma'] for r in sweep_results]
    dominances = [r['dominance'] for r in sweep_results]
    monuments = [r['monument'] for r in sweep_results]
    aggregations = [r['aggregation'] for r in sweep_results]

    axes[0].plot(sigmas, dominances, 'o-')
    axes[0].axhline(y=0, color='k', linestyle='--', alpha=0.3)
    axes[0].axvline(x=0.53, color='r', linestyle='--', alpha=0.5, label='σ*')
    axes[0].set_xlabel('Target σ')
    axes[0].set_ylabel('Strategy Dominance')
    axes[0].set_title('Strategy vs Environmental Uncertainty')
    axes[0].legend()

    axes[1].plot(sigmas, monuments, 'o-', color='purple')
    axes[1].set_xlabel('Target σ')
    axes[1].set_ylabel('Final Monument Level')
    axes[1].set_title('Monument Building vs σ')

    axes[2].plot(sigmas, aggregations, 'o-', color='green')
    axes[2].set_xlabel('Target σ')
    axes[2].set_ylabel('Mean Aggregation Size')
    axes[2].set_title('Aggregation Size vs σ')

    plt.tight_layout()
    plt.savefig(output_dir / 'sigma_sweep.png', dpi=150)
    plt.show()

    print("\nTests complete!")


if __name__ == "__main__":
    main()
