"""
Calibrate theory-ABM offset based on diagnostic findings.

The offset appears to stem primarily from:
1. Emergent n differs from assumed n=25 (varies with σ)
2. Non-equilibrium dynamics (strategy switching near threshold)
3. Memory effects in band decision-making

This script derives a calibration correction.
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from poverty_point.core_simulation import run_single_simulation
from poverty_point.parameters import (
    default_parameters, critical_threshold, W_aggregator, W_independent,
    cooperation_benefit
)


def measure_emergent_n_at_sigma(sigma: float, epsilon: float,
                                n_runs: int = 10, duration: int = 400) -> dict:
    """Measure what n actually emerges at a given sigma."""
    all_n = []

    for seed in range(n_runs):
        results = run_single_simulation(
            sigma=sigma, epsilon=epsilon, seed=seed,
            duration=duration, verbose=False
        )

        # Post-burn-in aggregation sizes
        for state in results.yearly_states[100:]:
            all_n.append(state.aggregation_size)

    return {
        'sigma': sigma,
        'mean_n': np.mean(all_n),
        'std_n': np.std(all_n)
    }


def fit_emergent_n_model(epsilon: float = 0.35) -> dict:
    """
    Fit a model for how n depends on sigma.

    n(σ) ≈ n_base + k * σ
    """
    sigma_values = [0.30, 0.40, 0.50, 0.60, 0.70, 0.80]
    n_values = []

    print(f"Measuring emergent n at ε={epsilon}...")
    for sigma in sigma_values:
        result = measure_emergent_n_at_sigma(sigma, epsilon, n_runs=5, duration=300)
        n_values.append(result['mean_n'])
        print(f"  σ={sigma:.2f}: n={result['mean_n']:.1f}")

    # Linear fit
    coeffs = np.polyfit(sigma_values, n_values, 1)
    k, n_base = coeffs

    return {
        'k': k,
        'n_base': n_base,
        'sigma_values': sigma_values,
        'n_values': n_values,
        'model': lambda sigma: n_base + k * sigma
    }


def critical_threshold_with_emergent_n(epsilon: float, sigma_guess: float,
                                       params, n_model) -> float:
    """
    Calculate σ* accounting for emergent n.

    This requires iterative solution since:
    - σ* depends on n
    - n depends on σ

    We find σ where W_agg(σ, n(σ)) = W_ind(σ)
    """
    # Iterative solution
    sigma = sigma_guess

    for _ in range(20):  # Iterate to convergence
        n_at_sigma = max(5, n_model(sigma))  # Ensure n >= 5

        # Calculate threshold for this n
        new_sigma = critical_threshold(epsilon, n_at_sigma, params)

        if abs(new_sigma - sigma) < 0.001:
            break

        sigma = 0.5 * sigma + 0.5 * new_sigma  # Damped update

    return sigma


def create_calibration_figure(output_dir: str = "figures/diagnostics"):
    """Create figure showing calibrated vs uncalibrated predictions."""
    os.makedirs(output_dir, exist_ok=True)

    # Fit emergent n model
    n_fit = fit_emergent_n_model(epsilon=0.35)

    print(f"\nEmergent n model: n(σ) = {n_fit['n_base']:.2f} + {n_fit['k']:.2f} * σ")

    # Create figure
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # Panel A: Emergent n model
    ax1 = axes[0]
    sigma_fine = np.linspace(0.2, 0.9, 50)
    n_predicted = [n_fit['model'](s) for s in sigma_fine]

    ax1.scatter(n_fit['sigma_values'], n_fit['n_values'], s=80, c='blue',
                label='ABM measurements')
    ax1.plot(sigma_fine, n_predicted, 'b--', label='Linear fit')
    ax1.axhline(25, color='red', linestyle=':', label='Theory assumption (n=25)')
    ax1.set_xlabel('Environmental Uncertainty (σ)')
    ax1.set_ylabel('Aggregation Size (n)')
    ax1.set_title('A. Emergent n vs σ')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Panel B: Original vs calibrated threshold
    ax2 = axes[1]

    epsilon_values = np.linspace(0.0, 0.5, 20)
    params = default_parameters()

    sigma_star_original = []
    sigma_star_calibrated = []

    for eps in epsilon_values:
        # Original (n=25)
        orig = critical_threshold(eps, 25, params)
        sigma_star_original.append(orig)

        # Calibrated (emergent n)
        calib = critical_threshold_with_emergent_n(eps, 0.5, params, n_fit['model'])
        sigma_star_calibrated.append(calib)

    ax2.plot(epsilon_values, sigma_star_original, 'b-', linewidth=2,
             label='Original (n=25)')
    ax2.plot(epsilon_values, sigma_star_calibrated, 'r-', linewidth=2,
             label='Calibrated (emergent n)')

    # Add empirical data points (from offset analysis)
    eps_empirical = [0.15, 0.25, 0.35, 0.45]
    sigma_empirical = [0.704, 0.679, 0.648, 0.625]
    ax2.scatter(eps_empirical, sigma_empirical, s=100, c='purple', marker='s',
                label='ABM empirical', zorder=5)

    ax2.set_xlabel('Ecotone Advantage (ε)')
    ax2.set_ylabel('Critical Threshold (σ*)')
    ax2.set_title('B. Theory Calibration')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # Panel C: Residuals
    ax3 = axes[2]

    # Calculate residuals for empirical points
    residuals_original = []
    residuals_calibrated = []

    for eps, sigma_emp in zip(eps_empirical, sigma_empirical):
        orig = critical_threshold(eps, 25, params)
        calib = critical_threshold_with_emergent_n(eps, 0.5, params, n_fit['model'])
        residuals_original.append(sigma_emp - orig)
        residuals_calibrated.append(sigma_emp - calib)

    x = np.arange(len(eps_empirical))
    width = 0.35

    bars1 = ax3.bar(x - width/2, residuals_original, width, label='Original', color='blue')
    bars2 = ax3.bar(x + width/2, residuals_calibrated, width, label='Calibrated', color='red')

    ax3.set_xlabel('Ecotone Advantage (ε)')
    ax3.set_ylabel('Residual (ABM - Theory)')
    ax3.set_title('C. Residual Analysis')
    ax3.set_xticks(x)
    ax3.set_xticklabels([f'{e:.2f}' for e in eps_empirical])
    ax3.legend()
    ax3.axhline(0, color='black', linestyle='-', linewidth=0.5)
    ax3.grid(True, alpha=0.3, axis='y')

    # Add text with statistics
    mean_orig = np.mean(residuals_original)
    mean_calib = np.mean(residuals_calibrated)
    ax3.text(0.95, 0.95, f'Mean residual:\nOriginal: {mean_orig:+.3f}\nCalibrated: {mean_calib:+.3f}',
             transform=ax3.transAxes, ha='right', va='top', fontsize=10,
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    plt.tight_layout()

    # Save
    fig.savefig(os.path.join(output_dir, 'calibration_analysis.png'),
                dpi=150, bbox_inches='tight', facecolor='white')
    fig.savefig(os.path.join(output_dir, 'calibration_analysis.pdf'),
                bbox_inches='tight', facecolor='white')
    plt.close(fig)

    print(f"\nCalibration figure saved to {output_dir}/calibration_analysis.png")

    # Print calibration summary
    print("\n" + "="*60)
    print("CALIBRATION SUMMARY")
    print("="*60)
    print(f"\nEmergent n model: n(σ) = {n_fit['n_base']:.2f} + {n_fit['k']:.2f} * σ")
    print(f"  At σ=0.3: n ≈ {n_fit['model'](0.3):.1f}")
    print(f"  At σ=0.5: n ≈ {n_fit['model'](0.5):.1f}")
    print(f"  At σ=0.7: n ≈ {n_fit['model'](0.7):.1f}")
    print(f"\nResidual improvement:")
    print(f"  Original mean residual: {mean_orig:+.3f}")
    print(f"  Calibrated mean residual: {mean_calib:+.3f}")
    print(f"  Improvement: {abs(mean_orig) - abs(mean_calib):.3f}")

    return {
        'n_model': n_fit,
        'residuals_original': residuals_original,
        'residuals_calibrated': residuals_calibrated
    }


if __name__ == "__main__":
    results = create_calibration_figure()
