"""
Phase space exploration for Poverty Point ABM.

This script runs simulations across the σ × ε parameter space
to validate theoretical predictions and identify emergence conditions.
"""

import numpy as np
import json
import os
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict, Tuple
from concurrent.futures import ProcessPoolExecutor, as_completed
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from poverty_point.core_simulation import run_single_simulation, SimulationResults
from poverty_point.parameters import default_parameters, critical_threshold


@dataclass
class PhaseSpacePoint:
    """Results for a single point in phase space."""
    sigma: float
    epsilon: float
    seed: int

    # Primary outcomes
    strategy_dominance: float
    mean_aggregation_size: float
    final_monument_level: float
    total_exotics: int
    mean_population: float

    # Theoretical comparison
    sigma_star_theoretical: float
    above_threshold: bool  # sigma > sigma*

    # Diagnostics
    run_time_seconds: float


def run_single_point(sigma: float, epsilon: float, seed: int,
                     duration: int = 600) -> PhaseSpacePoint:
    """
    Run a single simulation and extract phase space point.

    Args:
        sigma: Environmental uncertainty
        epsilon: Ecotone advantage
        seed: Random seed
        duration: Simulation duration

    Returns:
        PhaseSpacePoint with results
    """
    import time
    start_time = time.time()

    results = run_single_simulation(
        sigma=sigma,
        epsilon=epsilon,
        seed=seed,
        duration=duration,
        verbose=False
    )

    elapsed = time.time() - start_time

    return PhaseSpacePoint(
        sigma=float(sigma),
        epsilon=float(epsilon),
        seed=int(seed),
        strategy_dominance=float(results.final_strategy_dominance),
        mean_aggregation_size=float(results.mean_aggregation_size),
        final_monument_level=float(results.final_monument_level),
        total_exotics=int(results.total_exotics),
        mean_population=float(results.mean_population),
        sigma_star_theoretical=float(results.sigma_star_theoretical),
        above_threshold=bool(sigma > results.sigma_star_theoretical),
        run_time_seconds=float(elapsed)
    )


def run_phase_space_exploration(
    sigma_range: Tuple[float, float, int] = (0.2, 0.8, 13),
    epsilon_range: Tuple[float, float, int] = (0.0, 0.5, 11),
    n_replicates: int = 10,
    duration: int = 600,
    n_workers: int = 4,
    output_dir: str = "results/phase_space",
    verbose: bool = True
) -> List[PhaseSpacePoint]:
    """
    Run full phase space exploration.

    Args:
        sigma_range: (min, max, n_points) for sigma
        epsilon_range: (min, max, n_points) for epsilon
        n_replicates: Number of replicates per parameter combination
        duration: Simulation duration per run
        n_workers: Number of parallel workers
        output_dir: Directory for output files
        verbose: Print progress

    Returns:
        List of PhaseSpacePoint results
    """
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Generate parameter grid
    sigma_values = np.linspace(*sigma_range)
    epsilon_values = np.linspace(*epsilon_range)

    # Generate all jobs
    jobs = []
    base_seed = 42

    for i, sigma in enumerate(sigma_values):
        for j, epsilon in enumerate(epsilon_values):
            for k in range(n_replicates):
                seed = base_seed + i * 1000 + j * 100 + k
                jobs.append((sigma, epsilon, seed, duration))

    total_jobs = len(jobs)
    if verbose:
        print(f"Phase space exploration")
        print(f"  σ range: {sigma_range[0]:.2f} - {sigma_range[1]:.2f} ({sigma_range[2]} points)")
        print(f"  ε range: {epsilon_range[0]:.2f} - {epsilon_range[1]:.2f} ({epsilon_range[2]} points)")
        print(f"  Replicates: {n_replicates}")
        print(f"  Total runs: {total_jobs}")
        print(f"  Workers: {n_workers}")
        print()

    # Run simulations
    results = []
    completed = 0

    if n_workers == 1:
        # Serial execution
        for sigma, epsilon, seed, dur in jobs:
            result = run_single_point(sigma, epsilon, seed, dur)
            results.append(result)
            completed += 1
            if verbose and completed % 10 == 0:
                print(f"  Completed {completed}/{total_jobs} ({100*completed/total_jobs:.1f}%)")
    else:
        # Parallel execution
        with ProcessPoolExecutor(max_workers=n_workers) as executor:
            futures = {
                executor.submit(run_single_point, sigma, epsilon, seed, dur): (sigma, epsilon, seed)
                for sigma, epsilon, seed, dur in jobs
            }

            for future in as_completed(futures):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    sigma, epsilon, seed = futures[future]
                    print(f"  Error at σ={sigma:.2f}, ε={epsilon:.2f}, seed={seed}: {e}")

                completed += 1
                if verbose and completed % 50 == 0:
                    print(f"  Completed {completed}/{total_jobs} ({100*completed/total_jobs:.1f}%)")

    if verbose:
        print(f"\nCompleted all {len(results)} simulations")

    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(output_dir, f"phase_space_{timestamp}.json")

    with open(output_file, 'w') as f:
        json.dump([asdict(r) for r in results], f, indent=2)

    if verbose:
        print(f"Results saved to: {output_file}")

    return results


def analyze_phase_space(results: List[PhaseSpacePoint],
                        output_dir: str = "results/analysis") -> Dict:
    """
    Analyze phase space exploration results.

    Args:
        results: List of PhaseSpacePoint results
        output_dir: Directory for output files

    Returns:
        Analysis dictionary
    """
    os.makedirs(output_dir, exist_ok=True)

    # Group by (sigma, epsilon)
    grouped = {}
    for r in results:
        key = (r.sigma, r.epsilon)
        if key not in grouped:
            grouped[key] = []
        grouped[key].append(r)

    # Calculate statistics at each point
    analysis = {
        'sigma_values': sorted(set(r.sigma for r in results)),
        'epsilon_values': sorted(set(r.epsilon for r in results)),
        'points': {}
    }

    for (sigma, epsilon), points in grouped.items():
        dominances = [p.strategy_dominance for p in points]
        agg_sizes = [p.mean_aggregation_size for p in points]
        monuments = [p.final_monument_level for p in points]

        analysis['points'][f"{sigma:.3f}_{epsilon:.3f}"] = {
            'sigma': sigma,
            'epsilon': epsilon,
            'n_replicates': len(points),
            'dominance_mean': float(np.mean(dominances)),
            'dominance_std': float(np.std(dominances)),
            'dominance_ci95': (
                float(np.percentile(dominances, 2.5)),
                float(np.percentile(dominances, 97.5))
            ),
            'aggregation_mean': float(np.mean(agg_sizes)),
            'aggregation_std': float(np.std(agg_sizes)),
            'monument_mean': float(np.mean(monuments)),
            'monument_std': float(np.std(monuments)),
            'sigma_star_theoretical': points[0].sigma_star_theoretical,
            'predicted_above_threshold': sigma > points[0].sigma_star_theoretical
        }

    # Find empirical critical threshold at each epsilon
    analysis['empirical_thresholds'] = {}

    for epsilon in analysis['epsilon_values']:
        # Get dominance at each sigma for this epsilon
        sigma_dominance = []
        for sigma in analysis['sigma_values']:
            key = f"{sigma:.3f}_{epsilon:.3f}"
            if key in analysis['points']:
                sigma_dominance.append((sigma, analysis['points'][key]['dominance_mean']))

        if sigma_dominance:
            # Find sigma where dominance crosses 0
            sigma_dominance.sort()
            sigma_star_empirical = None

            for i in range(len(sigma_dominance) - 1):
                s1, d1 = sigma_dominance[i]
                s2, d2 = sigma_dominance[i + 1]

                if d1 < 0 and d2 >= 0:
                    # Linear interpolation
                    sigma_star_empirical = s1 + (0 - d1) * (s2 - s1) / (d2 - d1)
                    break

            # Get theoretical threshold
            params = default_parameters(epsilon=epsilon)
            sigma_star_theoretical = critical_threshold(
                epsilon, n=25, params=params
            )

            analysis['empirical_thresholds'][f"{epsilon:.3f}"] = {
                'epsilon': epsilon,
                'sigma_star_empirical': sigma_star_empirical,
                'sigma_star_theoretical': sigma_star_theoretical,
                'difference': (sigma_star_empirical - sigma_star_theoretical
                              if sigma_star_empirical else None)
            }

    # Save analysis
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(output_dir, f"analysis_{timestamp}.json")

    with open(output_file, 'w') as f:
        json.dump(analysis, f, indent=2)

    print(f"Analysis saved to: {output_file}")

    return analysis


def quick_test():
    """Run a quick test with reduced parameters."""
    print("Running quick test...")

    results = run_phase_space_exploration(
        sigma_range=(0.3, 0.7, 5),
        epsilon_range=(0.1, 0.4, 4),
        n_replicates=3,
        duration=200,
        n_workers=1,
        output_dir="results/test",
        verbose=True
    )

    analysis = analyze_phase_space(results, output_dir="results/test")

    print("\nEmpirical thresholds:")
    for eps_key, data in analysis['empirical_thresholds'].items():
        emp = data['sigma_star_empirical']
        emp_str = f"{emp:.3f}" if emp is not None else "N/A"
        print(f"  ε={data['epsilon']:.2f}: "
              f"σ*_emp={emp_str}, "
              f"σ*_theory={data['sigma_star_theoretical']:.3f}")

    return results, analysis


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run phase space exploration")
    parser.add_argument("--quick", action="store_true",
                        help="Run quick test with reduced parameters")
    parser.add_argument("--workers", type=int, default=4,
                        help="Number of parallel workers")
    parser.add_argument("--replicates", type=int, default=10,
                        help="Number of replicates per point")
    parser.add_argument("--duration", type=int, default=600,
                        help="Simulation duration in years")

    args = parser.parse_args()

    if args.quick:
        quick_test()
    else:
        results = run_phase_space_exploration(
            n_replicates=args.replicates,
            duration=args.duration,
            n_workers=args.workers,
            verbose=True
        )
        analyze_phase_space(results)
