"""
Generate figures comparing ABM results with theoretical predictions.

This script creates validation figures showing:
1. ABM phase space vs theoretical phase space
2. Empirical vs theoretical critical thresholds
3. Emergent dynamics (monument building, aggregation size, etc.)
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import json
import os
import sys
from typing import Dict, List, Optional

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from poverty_point.parameters import (
    default_parameters, critical_threshold, W_aggregator, W_independent,
    cooperation_benefit
)


def load_analysis_results(analysis_file: str) -> Dict:
    """Load analysis results from JSON file."""
    with open(analysis_file, 'r') as f:
        return json.load(f)


def create_phase_space_comparison(analysis: Dict,
                                  output_dir: str = "figures/validation"
                                  ) -> plt.Figure:
    """
    Create side-by-side comparison of theoretical and ABM phase spaces.

    Args:
        analysis: Analysis results dictionary
        output_dir: Output directory

    Returns:
        Figure object
    """
    os.makedirs(output_dir, exist_ok=True)

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Get data ranges
    sigma_values = sorted(analysis['sigma_values'])
    epsilon_values = sorted(analysis['epsilon_values'])

    # Create meshgrid
    sigma_grid = np.array(sigma_values)
    epsilon_grid = np.array(epsilon_values)

    # ============ Panel A: Theoretical Phase Space ============
    ax1 = axes[0]

    # Calculate theoretical dominance
    params = default_parameters()
    n_fixed = 25

    theory_dominance = np.zeros((len(epsilon_grid), len(sigma_grid)))
    for i, eps in enumerate(epsilon_grid):
        for j, sig in enumerate(sigma_grid):
            W_agg = W_aggregator(sig, eps, n_fixed, params)
            W_ind = W_independent(sig, params)
            W_total = W_agg + W_ind
            if W_total > 0.001:
                theory_dominance[i, j] = (W_agg - W_ind) / W_total
            else:
                theory_dominance[i, j] = 0.0

    # Plot theoretical
    colors = ['#7b3294', '#c2a5cf', '#f7f7f7', '#fdae61', '#e66101']
    cmap = LinearSegmentedColormap.from_list('strategy', colors, N=256)

    im1 = ax1.imshow(theory_dominance,
                     extent=[sigma_grid.min(), sigma_grid.max(),
                             epsilon_grid.min(), epsilon_grid.max()],
                     origin='lower', aspect='auto', cmap=cmap, vmin=-1, vmax=1)

    # Add theoretical threshold line
    theory_thresholds = []
    for eps in epsilon_grid:
        s_star = critical_threshold(eps, n_fixed, params)
        theory_thresholds.append(s_star)

    ax1.plot(theory_thresholds, epsilon_grid, 'k-', linewidth=2.5,
             label='σ* (theory)')

    ax1.set_xlabel('Environmental Uncertainty (σ)', fontsize=12)
    ax1.set_ylabel('Ecotone Advantage (ε)', fontsize=12)
    ax1.set_title('A. Theoretical Prediction', fontsize=14)
    ax1.legend(loc='upper left')

    # ============ Panel B: ABM Phase Space ============
    ax2 = axes[1]

    # Extract ABM dominance values
    abm_dominance = np.zeros((len(epsilon_grid), len(sigma_grid)))
    for i, eps in enumerate(epsilon_grid):
        for j, sig in enumerate(sigma_grid):
            key = f"{sig:.3f}_{eps:.3f}"
            if key in analysis['points']:
                abm_dominance[i, j] = analysis['points'][key]['dominance_mean']

    im2 = ax2.imshow(abm_dominance,
                     extent=[sigma_grid.min(), sigma_grid.max(),
                             epsilon_grid.min(), epsilon_grid.max()],
                     origin='lower', aspect='auto', cmap=cmap, vmin=-1, vmax=1)

    # Add empirical threshold line
    emp_thresholds = []
    emp_epsilons = []
    for eps_key, data in analysis['empirical_thresholds'].items():
        if data['sigma_star_empirical'] is not None:
            emp_thresholds.append(data['sigma_star_empirical'])
            emp_epsilons.append(data['epsilon'])

    if emp_thresholds:
        ax2.plot(emp_thresholds, emp_epsilons, 'ko-', linewidth=2.5,
                 markersize=8, label='σ* (ABM)')

    # Also show theoretical for comparison
    ax2.plot(theory_thresholds, epsilon_grid, 'k--', linewidth=1.5,
             alpha=0.5, label='σ* (theory)')

    ax2.set_xlabel('Environmental Uncertainty (σ)', fontsize=12)
    ax2.set_ylabel('Ecotone Advantage (ε)', fontsize=12)
    ax2.set_title('B. ABM Results', fontsize=14)
    ax2.legend(loc='upper left')

    # Shared colorbar
    cbar = fig.colorbar(im2, ax=axes, shrink=0.8)
    cbar.ax.set_ylabel('Strategy Dominance\n← Independent | Aggregation →',
                       fontsize=10)

    plt.tight_layout()

    # Save
    fig.savefig(os.path.join(output_dir, 'phase_space_comparison.png'),
                dpi=150, bbox_inches='tight', facecolor='white')
    fig.savefig(os.path.join(output_dir, 'phase_space_comparison.pdf'),
                bbox_inches='tight', facecolor='white')

    return fig


def create_threshold_comparison(analysis: Dict,
                                output_dir: str = "figures/validation"
                                ) -> plt.Figure:
    """
    Compare theoretical and empirical critical thresholds.

    Args:
        analysis: Analysis results dictionary
        output_dir: Output directory

    Returns:
        Figure object
    """
    os.makedirs(output_dir, exist_ok=True)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # ============ Panel A: Threshold vs Epsilon ============
    ax1 = axes[0]

    # Theoretical thresholds
    params = default_parameters()
    eps_range = np.linspace(0.0, 0.5, 50)
    theory_thresholds = [critical_threshold(eps, 25, params) for eps in eps_range]

    ax1.plot(eps_range, theory_thresholds, 'b-', linewidth=2, label='Theory')

    # Empirical thresholds
    emp_eps = []
    emp_sigma = []
    for eps_key, data in analysis['empirical_thresholds'].items():
        if data['sigma_star_empirical'] is not None:
            emp_eps.append(data['epsilon'])
            emp_sigma.append(data['sigma_star_empirical'])

    if emp_eps:
        ax1.scatter(emp_eps, emp_sigma, s=100, c='red', marker='o',
                    label='ABM (empirical)', zorder=5)

    ax1.set_xlabel('Ecotone Advantage (ε)', fontsize=12)
    ax1.set_ylabel('Critical Threshold (σ*)', fontsize=12)
    ax1.set_title('A. Critical Threshold vs Ecotone Advantage', fontsize=12)
    ax1.legend(loc='upper right')
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(0.0, 0.5)
    ax1.set_ylim(0.0, 1.0)

    # ============ Panel B: Theory vs Empirical Scatter ============
    ax2 = axes[1]

    # Scatter plot of theory vs empirical
    theory_at_emp = []
    for eps_key, data in analysis['empirical_thresholds'].items():
        if data['sigma_star_empirical'] is not None:
            theory_at_emp.append(data['sigma_star_theoretical'])

    if emp_sigma and theory_at_emp:
        ax2.scatter(theory_at_emp, emp_sigma, s=100, c='purple', marker='o')

        # Perfect agreement line
        max_val = max(max(emp_sigma), max(theory_at_emp)) + 0.1
        ax2.plot([0, max_val], [0, max_val], 'k--', alpha=0.5,
                 label='Perfect agreement')

        # Calculate correlation
        correlation = np.corrcoef(theory_at_emp, emp_sigma)[0, 1]
        ax2.text(0.05, 0.95, f'r = {correlation:.3f}',
                 transform=ax2.transAxes, fontsize=12,
                 verticalalignment='top')

        # Calculate mean offset
        offset = np.mean(np.array(emp_sigma) - np.array(theory_at_emp))
        ax2.text(0.05, 0.88, f'Mean offset = {offset:+.3f}',
                 transform=ax2.transAxes, fontsize=12,
                 verticalalignment='top')

    ax2.set_xlabel('Theoretical σ*', fontsize=12)
    ax2.set_ylabel('Empirical σ* (ABM)', fontsize=12)
    ax2.set_title('B. Theory vs ABM Threshold Comparison', fontsize=12)
    ax2.legend(loc='lower right')
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(0.4, 0.8)
    ax2.set_ylim(0.4, 0.8)
    ax2.set_aspect('equal')

    plt.tight_layout()

    # Save
    fig.savefig(os.path.join(output_dir, 'threshold_comparison.png'),
                dpi=150, bbox_inches='tight', facecolor='white')
    fig.savefig(os.path.join(output_dir, 'threshold_comparison.pdf'),
                bbox_inches='tight', facecolor='white')

    return fig


def create_dominance_heatmap(analysis: Dict,
                             output_dir: str = "figures/validation"
                             ) -> plt.Figure:
    """
    Create detailed heatmap of strategy dominance from ABM.

    Args:
        analysis: Analysis results dictionary
        output_dir: Output directory

    Returns:
        Figure object
    """
    os.makedirs(output_dir, exist_ok=True)

    fig, ax = plt.subplots(figsize=(10, 8))

    # Get data
    sigma_values = sorted(analysis['sigma_values'])
    epsilon_values = sorted(analysis['epsilon_values'])

    # Create matrix
    dominance_matrix = np.zeros((len(epsilon_values), len(sigma_values)))

    for i, eps in enumerate(epsilon_values):
        for j, sig in enumerate(sigma_values):
            key = f"{sig:.3f}_{eps:.3f}"
            if key in analysis['points']:
                dominance_matrix[i, j] = analysis['points'][key]['dominance_mean']

    # Plot heatmap
    colors = ['#7b3294', '#c2a5cf', '#f7f7f7', '#fdae61', '#e66101']
    cmap = LinearSegmentedColormap.from_list('strategy', colors, N=256)

    im = ax.imshow(dominance_matrix,
                   extent=[min(sigma_values), max(sigma_values),
                           min(epsilon_values), max(epsilon_values)],
                   origin='lower', aspect='auto', cmap=cmap,
                   vmin=-1, vmax=1)

    # Add contour at dominance = 0
    X, Y = np.meshgrid(sigma_values, epsilon_values)
    contour = ax.contour(X, Y, dominance_matrix, levels=[0],
                         colors='black', linewidths=2)
    ax.clabel(contour, fmt='σ*=%.2f', fontsize=10)

    # Add theoretical threshold line
    params = default_parameters()
    theory_thresholds = [critical_threshold(eps, 25, params)
                         for eps in epsilon_values]
    ax.plot(theory_thresholds, epsilon_values, 'w--', linewidth=2,
            label='Theoretical σ*')

    # Labels
    ax.set_xlabel('Environmental Uncertainty (σ)', fontsize=12)
    ax.set_ylabel('Ecotone Advantage (ε)', fontsize=12)
    ax.set_title('ABM Strategy Dominance Across Phase Space\n'
                 '(Black contour = empirical σ*, white dashed = theoretical σ*)',
                 fontsize=12)

    ax.legend(loc='upper left')

    # Colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.ax.set_ylabel('Strategy Dominance\n← Independent | Aggregation →',
                       fontsize=10)

    plt.tight_layout()

    # Save
    fig.savefig(os.path.join(output_dir, 'dominance_heatmap.png'),
                dpi=150, bbox_inches='tight', facecolor='white')
    fig.savefig(os.path.join(output_dir, 'dominance_heatmap.pdf'),
                bbox_inches='tight', facecolor='white')

    return fig


def generate_all_validation_figures(analysis_file: str,
                                    output_dir: str = "figures/validation"):
    """
    Generate all validation figures from analysis results.

    Args:
        analysis_file: Path to analysis JSON file
        output_dir: Output directory for figures
    """
    print(f"Loading analysis from: {analysis_file}")
    analysis = load_analysis_results(analysis_file)

    print("Generating phase space comparison...")
    create_phase_space_comparison(analysis, output_dir)

    print("Generating threshold comparison...")
    create_threshold_comparison(analysis, output_dir)

    print("Generating dominance heatmap...")
    create_dominance_heatmap(analysis, output_dir)

    print(f"\nAll figures saved to: {output_dir}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate ABM validation figures")
    parser.add_argument("--analysis", type=str,
                        default="results/test/analysis_20260115_082055.json",
                        help="Path to analysis JSON file")
    parser.add_argument("--output", type=str, default="figures/validation",
                        help="Output directory")

    args = parser.parse_args()

    if os.path.exists(args.analysis):
        generate_all_validation_figures(args.analysis, args.output)
    else:
        print(f"Analysis file not found: {args.analysis}")
        print("Run phase space exploration first with:")
        print("  python scripts/exploration/run_phase_space.py --quick")
