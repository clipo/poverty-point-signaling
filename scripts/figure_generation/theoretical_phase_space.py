#!/usr/bin/env python3
"""
Create Theoretical Phase Space Prediction Figure

This figure shows the analytically predicted phase space for Section 2,
illustrating where aggregation-based costly signaling is expected to be
adaptive based on the theoretical framework BEFORE showing ABM validation.

The figure shows:
1. The critical threshold σ* as a function of ecotone advantage ε
2. Predicted regions where independent vs aggregation strategies dominate
3. How the fitness functions create the phase transition
"""

import sys
sys.path.insert(0, '/Users/clipo/PycharmProjects/poverty-point-signaling')

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from pathlib import Path

# Output directory
OUTPUT_DIR = Path('/Users/clipo/PycharmProjects/poverty-point-signaling/figures/integrated')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def W_aggregator(sigma, epsilon, n, params):
    """Calculate aggregator fitness."""
    C_total = params['C_travel'] + params['C_signal'] + params['C_opportunity']
    alpha = params['alpha_agg']
    b = params['b_coop']
    c = params['c_crowd']
    n_star = params['n_star']
    B_recip = params['B_recip']

    # Effective sigma reduced by ecotone
    sigma_eff = sigma * (1 - epsilon)

    # Cooperation benefits
    f_n = 1 + b * np.log(n)
    if n > n_star:
        f_n -= c * (n - n_star)**2

    # Fitness
    W = (1 - C_total) * (1 - alpha * sigma_eff) * f_n * (1 + B_recip)
    return W


def W_independent(sigma, params):
    """Calculate independent fitness."""
    R_ind = params['R_ind']
    beta = params['beta_ind']

    W = R_ind * (1 - beta * sigma)
    return W


def critical_threshold(epsilon, n, params):
    """Calculate critical σ* where strategies have equal fitness."""
    C_total = params['C_travel'] + params['C_signal'] + params['C_opportunity']
    alpha = params['alpha_agg']
    beta = params['beta_ind']
    R_ind = params['R_ind']
    b = params['b_coop']
    B_recip = params['B_recip']

    # Cooperation benefits at size n
    f_n = 1 + b * np.log(n)

    # Aggregator baseline (without sigma effects)
    agg_base = (1 - C_total) * f_n * (1 + B_recip)

    # Solve for sigma where W_agg = W_ind
    # agg_base * (1 - alpha * sigma * (1-eps)) = R_ind * (1 - beta * sigma)
    # agg_base - agg_base * alpha * sigma * (1-eps) = R_ind - R_ind * beta * sigma
    # R_ind * beta * sigma - agg_base * alpha * (1-eps) * sigma = R_ind - agg_base
    # sigma * (R_ind * beta - agg_base * alpha * (1-eps)) = R_ind - agg_base

    numerator = R_ind - agg_base
    denominator = R_ind * beta - agg_base * alpha * (1 - epsilon)

    if denominator <= 0:
        return 1.0  # No valid threshold

    sigma_star = numerator / denominator
    return max(0, min(1, sigma_star))


def default_parameters():
    """Return default model parameters."""
    return {
        'C_travel': 0.08,
        'C_signal': 0.15,
        'C_opportunity': 0.19,
        'alpha_agg': 0.40,
        'beta_ind': 0.75,
        'R_ind': 1.10,
        'b_coop': 0.08,
        'c_crowd': 0.015,
        'n_star': 25,
        'B_recip': 0.05,
    }


def create_theoretical_phase_space_figure():
    """
    Create the theoretical phase space prediction figure.
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    params = default_parameters()
    n = 25  # Optimal aggregation size

    # Create fine grid for smooth visualization
    sigma_vals = np.linspace(0.1, 0.9, 100)
    epsilon_vals = np.linspace(0.0, 0.5, 100)

    # Calculate fitness difference grid (W_agg - W_ind)
    fitness_diff = np.zeros((len(epsilon_vals), len(sigma_vals)))

    for i, eps in enumerate(epsilon_vals):
        for j, sig in enumerate(sigma_vals):
            W_agg = W_aggregator(sig, eps, n, params)
            W_ind = W_independent(sig, params)
            fitness_diff[i, j] = W_agg - W_ind

    # Custom colormap: purple (independent favored) to orange (aggregation favored)
    colors = ['#7b3294', '#c2a5cf', '#f7f7f7', '#fdae61', '#e66101']
    cmap = LinearSegmentedColormap.from_list('strategy', colors, N=256)

    # ==================
    # Panel A: Fitness difference (predicted strategy dominance)
    # ==================
    ax1 = axes[0]

    extent = [sigma_vals.min(), sigma_vals.max(), epsilon_vals.min(), epsilon_vals.max()]
    im1 = ax1.imshow(fitness_diff, extent=extent, origin='lower',
                     aspect='auto', cmap=cmap, vmin=-0.3, vmax=0.3,
                     interpolation='bilinear')

    # Plot critical threshold line
    eps_line = np.linspace(0.0, 0.5, 100)
    sigma_stars = [critical_threshold(eps, n, params) for eps in eps_line]
    ax1.plot(sigma_stars, eps_line, 'k-', linewidth=3, label='Critical threshold σ*')
    ax1.plot(sigma_stars, eps_line, 'w--', linewidth=1.5)

    # Add region labels
    ax1.text(0.25, 0.4, 'Independent\nFavored', fontsize=12, ha='center', va='center',
             color='#7b3294', fontweight='bold',
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    ax1.text(0.75, 0.15, 'Aggregation\nFavored', fontsize=12, ha='center', va='center',
             color='#e66101', fontweight='bold',
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    ax1.set_xlabel('Environmental Uncertainty (σ)', fontsize=12)
    ax1.set_ylabel('Ecotone Advantage (ε)', fontsize=12)
    ax1.set_title('A. Predicted Strategy Dominance', fontsize=12, fontweight='bold')
    ax1.legend(loc='upper left', fontsize=10)

    cbar1 = plt.colorbar(im1, ax=ax1, label='Fitness Difference (W_agg - W_ind)')
    cbar1.ax.set_ylabel('← Independent | Aggregation →', fontsize=9)

    # ==================
    # Panel B: Critical threshold as function of epsilon
    # ==================
    ax2 = axes[1]

    # Calculate critical thresholds for different n values
    n_values = [15, 20, 25, 30]
    colors_n = ['#d7191c', '#fdae61', '#1a9641', '#2b83ba']

    for n_val, color in zip(n_values, colors_n):
        sigma_stars_n = [critical_threshold(eps, n_val, params) for eps in eps_line]
        ax2.plot(eps_line, sigma_stars_n, '-', linewidth=2.5, color=color,
                label=f'n = {n_val} bands')

    # Fill regions
    ax2.fill_between(eps_line, 0, [critical_threshold(eps, 25, params) for eps in eps_line],
                     alpha=0.2, color='#7b3294', label='Independent region')
    ax2.fill_between(eps_line, [critical_threshold(eps, 25, params) for eps in eps_line], 1,
                     alpha=0.2, color='#e66101', label='Aggregation region')

    # Mark key points
    ax2.axhline(0.53, color='gray', linestyle=':', linewidth=1, alpha=0.7)
    ax2.text(0.02, 0.55, 'σ* ≈ 0.53\n(at ε=0.35)', fontsize=9, va='bottom')

    ax2.axvline(0.35, color='gray', linestyle=':', linewidth=1, alpha=0.7)
    ax2.text(0.36, 0.15, 'Poverty Point\nε ≈ 0.35', fontsize=9, ha='left')

    ax2.set_xlabel('Ecotone Advantage (ε)', fontsize=12)
    ax2.set_ylabel('Critical Threshold (σ*)', fontsize=12)
    ax2.set_title('B. Critical Threshold vs. Ecotone Advantage', fontsize=12, fontweight='bold')
    ax2.legend(loc='upper right', fontsize=9)
    ax2.set_xlim(0, 0.5)
    ax2.set_ylim(0.3, 0.8)
    ax2.grid(True, alpha=0.3)

    # Add annotation about the key prediction
    ax2.annotate('Higher ecotone advantage\nlowers the threshold',
                xy=(0.4, 0.52), xytext=(0.25, 0.4),
                fontsize=10, ha='center',
                arrowprops=dict(arrowstyle='->', color='black', lw=1.5))

    plt.tight_layout()

    # Add main title
    fig.suptitle('Theoretical Predictions: When Does Aggregation Become Adaptive?',
                fontsize=14, fontweight='bold', y=1.02)

    return fig


def main():
    """Generate the theoretical phase space figure."""
    print("=" * 60)
    print("Creating Theoretical Phase Space Prediction Figure")
    print("=" * 60)

    fig = create_theoretical_phase_space_figure()

    # Save outputs
    output_png = OUTPUT_DIR / 'fig_theoretical_phase_space.png'
    output_pdf = OUTPUT_DIR / 'fig_theoretical_phase_space.pdf'

    fig.savefig(output_png, dpi=300, bbox_inches='tight')
    fig.savefig(output_pdf, bbox_inches='tight')

    print(f"\nFigure saved to:")
    print(f"  PNG: {output_png}")
    print(f"  PDF: {output_pdf}")

    plt.close(fig)

    return fig


if __name__ == "__main__":
    main()
