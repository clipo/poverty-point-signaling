#!/usr/bin/env python3
"""
Phase Space Comparison Figures

Creates three phase space figures:
1. σ vs ε (ecotone advantage) - updated with finer grid
2. σ vs n (aggregation size)
3. σ vs C (signaling cost)

These show how different parameters affect the transition between
independent and aggregation strategies.
"""

import sys
sys.path.insert(0, '/Users/clipo/PycharmProjects/poverty-point-signaling')

import numpy as np
import json
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from pathlib import Path
from scipy.ndimage import gaussian_filter

# Directories
RESULTS_DIR = Path('/Users/clipo/PycharmProjects/poverty-point-signaling/results/analysis')
OUTPUT_DIR = Path('/Users/clipo/PycharmProjects/poverty-point-signaling/figures/integrated')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_fine_phase_space():
    """Load the fine-grained phase space results."""
    files = sorted(RESULTS_DIR.glob('phase_space_fine_*.json'))
    if files:
        latest = files[-1]
        print(f"Loading: {latest}")
        with open(latest) as f:
            return json.load(f)
    return None


def create_fine_phase_space_figure(results):
    """
    Create phase space figure with finer grid showing σ vs ε.
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Extract unique values
    sigma_vals = sorted(set(r['target_sigma'] for r in results))
    epsilon_vals = sorted(set(r['epsilon'] for r in results))

    # Create grids
    dominance_grid = np.zeros((len(epsilon_vals), len(sigma_vals)))
    monument_grid = np.zeros((len(epsilon_vals), len(sigma_vals)))

    for r in results:
        i = epsilon_vals.index(r['epsilon'])
        j = sigma_vals.index(r['target_sigma'])
        dominance_grid[i, j] = r['dominance']
        monument_grid[i, j] = r['monument_level']

    # Smooth the grids slightly for better visualization
    dominance_smooth = gaussian_filter(dominance_grid, sigma=0.5)
    monument_smooth = gaussian_filter(monument_grid, sigma=0.5)

    # Custom colormap
    colors = ['#7b3294', '#c2a5cf', '#f7f7f7', '#fdae61', '#e66101']
    cmap = LinearSegmentedColormap.from_list('strategy', colors, N=256)

    # Panel A: Strategy dominance
    ax1 = axes[0]
    extent = [min(sigma_vals), max(sigma_vals), min(epsilon_vals), max(epsilon_vals)]
    im1 = ax1.imshow(dominance_smooth, extent=extent, origin='lower',
                     aspect='auto', cmap=cmap, vmin=-1, vmax=0.5,
                     interpolation='bilinear')

    # Plot theoretical critical threshold line
    from src.poverty_point.parameters import default_parameters, critical_threshold
    params = default_parameters()
    eps_line = np.linspace(0.05, 0.5, 100)
    sigma_stars = [critical_threshold(eps, 25, params) for eps in eps_line]
    ax1.plot(sigma_stars, eps_line, 'k-', linewidth=2.5, label='Theoretical σ*')
    ax1.plot(sigma_stars, eps_line, 'w--', linewidth=1.5)

    ax1.set_xlabel('Environmental Uncertainty (σ)', fontsize=12)
    ax1.set_ylabel('Ecotone Advantage (ε)', fontsize=12)
    ax1.set_title('A. Strategy Dominance', fontsize=12, fontweight='bold')
    cbar1 = plt.colorbar(im1, ax=ax1, label='Strategy Dominance')
    cbar1.ax.set_ylabel('← Independent | Aggregation →', fontsize=9)
    ax1.legend(loc='upper left', fontsize=10)

    # Panel B: Monument investment
    ax2 = axes[1]
    im2 = ax2.imshow(monument_smooth, extent=extent, origin='lower',
                     aspect='auto', cmap='YlOrBr', interpolation='bilinear')
    ax2.plot(sigma_stars, eps_line, 'k-', linewidth=2.5, label='Theoretical σ*')
    ax2.plot(sigma_stars, eps_line, 'w--', linewidth=1.5)

    ax2.set_xlabel('Environmental Uncertainty (σ)', fontsize=12)
    ax2.set_ylabel('Ecotone Advantage (ε)', fontsize=12)
    ax2.set_title('B. Monument Investment', fontsize=12, fontweight='bold')
    plt.colorbar(im2, ax=ax2, label='Monument Level')
    ax2.legend(loc='upper left', fontsize=10)

    plt.tight_layout()
    return fig


def create_sigma_vs_n_figure():
    """
    Create theoretical figure showing σ vs aggregation size (n).
    """
    from src.poverty_point.parameters import default_parameters, critical_threshold

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    params = default_parameters()

    # Grid for σ and n
    sigma_vals = np.linspace(0.2, 0.9, 100)
    n_vals = np.linspace(5, 40, 100)

    # Calculate fitness difference grid
    epsilon = 0.35  # Fixed ecotone advantage (Poverty Point estimate)
    fitness_diff = np.zeros((len(n_vals), len(sigma_vals)))

    for i, n in enumerate(n_vals):
        for j, sig in enumerate(sigma_vals):
            # Aggregator fitness
            C_total = params.costs.C_total
            sigma_eff = sig * (1 - epsilon)
            f_n = 1 + params.cooperation.b_coop * np.log(n)
            if n > params.cooperation.n_optimal:
                f_n -= params.cooperation.c_crowd * (n - params.cooperation.n_optimal)**2
            W_agg = (1 - C_total) * (1 - params.vulnerability.alpha_agg * sigma_eff) * f_n * (1 + params.cooperation.B_recip)

            # Independent fitness
            W_ind = params.cooperation.R_ind * (1 - params.vulnerability.beta_ind * sig)

            fitness_diff[i, j] = W_agg - W_ind

    # Custom colormap
    colors = ['#7b3294', '#c2a5cf', '#f7f7f7', '#fdae61', '#e66101']
    cmap = LinearSegmentedColormap.from_list('strategy', colors, N=256)

    # Panel A: Fitness difference
    ax1 = axes[0]
    extent = [sigma_vals.min(), sigma_vals.max(), n_vals.min(), n_vals.max()]
    im1 = ax1.imshow(fitness_diff, extent=extent, origin='lower',
                     aspect='auto', cmap=cmap, vmin=-0.3, vmax=0.3,
                     interpolation='bilinear')

    # Plot critical threshold line (where fitness_diff = 0)
    n_line = np.linspace(10, 35, 50)
    sigma_stars = []
    for n in n_line:
        try:
            sig_star = critical_threshold(epsilon, n, params)
            sigma_stars.append(sig_star)
        except:
            sigma_stars.append(np.nan)
    ax1.plot(sigma_stars, n_line, 'k-', linewidth=2.5, label='Critical threshold σ*')
    ax1.plot(sigma_stars, n_line, 'w--', linewidth=1.5)

    # Mark optimal n
    ax1.axhline(params.cooperation.n_optimal, color='gray', linestyle=':', linewidth=1, alpha=0.7)
    ax1.text(0.25, params.cooperation.n_optimal + 1, f'n* = {params.cooperation.n_optimal}', fontsize=9)

    ax1.set_xlabel('Environmental Uncertainty (σ)', fontsize=12)
    ax1.set_ylabel('Aggregation Size (n bands)', fontsize=12)
    ax1.set_title('A. Strategy Dominance (ε = 0.35 fixed)', fontsize=12, fontweight='bold')
    cbar1 = plt.colorbar(im1, ax=ax1, label='Fitness Difference (W_agg - W_ind)')
    cbar1.ax.set_ylabel('← Independent | Aggregation →', fontsize=9)
    ax1.legend(loc='upper left', fontsize=10)

    # Add region labels
    ax1.text(0.3, 30, 'Independent\nFavored', fontsize=11, ha='center', va='center',
             color='#7b3294', fontweight='bold',
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    ax1.text(0.75, 20, 'Aggregation\nFavored', fontsize=11, ha='center', va='center',
             color='#e66101', fontweight='bold',
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    # Panel B: How critical threshold varies with n
    ax2 = axes[1]
    n_range = np.linspace(10, 40, 100)
    for eps, color, label in [(0.15, '#d7191c', 'ε = 0.15 (low)'),
                               (0.35, '#1a9641', 'ε = 0.35 (Poverty Point)'),
                               (0.50, '#2b83ba', 'ε = 0.50 (high)')]:
        sigma_stars_eps = [critical_threshold(eps, n, params) for n in n_range]
        ax2.plot(n_range, sigma_stars_eps, '-', linewidth=2.5, color=color, label=label)

    ax2.axvline(params.cooperation.n_optimal, color='gray', linestyle=':', linewidth=1, alpha=0.7)
    ax2.text(params.cooperation.n_optimal + 0.5, 0.75, f'n* = {params.cooperation.n_optimal}', fontsize=9)

    ax2.set_xlabel('Aggregation Size (n bands)', fontsize=12)
    ax2.set_ylabel('Critical Threshold (σ*)', fontsize=12)
    ax2.set_title('B. Critical Threshold vs. Aggregation Size', fontsize=12, fontweight='bold')
    ax2.legend(loc='upper right', fontsize=10)
    ax2.set_xlim(10, 40)
    ax2.set_ylim(0.4, 0.8)
    ax2.grid(True, alpha=0.3)

    # Add annotation
    ax2.annotate('Larger aggregations\nlower the threshold',
                xy=(30, 0.52), xytext=(35, 0.65),
                fontsize=10, ha='center',
                arrowprops=dict(arrowstyle='->', color='black', lw=1.5))

    plt.tight_layout()
    return fig


def create_sigma_vs_cost_figure():
    """
    Create theoretical figure showing σ vs signaling cost.
    """
    from src.poverty_point.parameters import default_parameters, critical_threshold

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    params = default_parameters()

    # Grid for σ and cost
    sigma_vals = np.linspace(0.2, 0.9, 100)
    cost_vals = np.linspace(0.05, 0.40, 100)  # C_signal ranges from 5% to 40%

    # Calculate fitness difference grid
    epsilon = 0.35  # Fixed ecotone advantage
    n = 25  # Fixed aggregation size
    fitness_diff = np.zeros((len(cost_vals), len(sigma_vals)))

    for i, C_signal in enumerate(cost_vals):
        for j, sig in enumerate(sigma_vals):
            # Aggregator fitness with varying signal cost
            C_total = params.costs.C_travel + C_signal + params.costs.C_opportunity
            sigma_eff = sig * (1 - epsilon)
            f_n = 1 + params.cooperation.b_coop * np.log(n)
            W_agg = (1 - C_total) * (1 - params.vulnerability.alpha_agg * sigma_eff) * f_n * (1 + params.cooperation.B_recip)

            # Independent fitness
            W_ind = params.cooperation.R_ind * (1 - params.vulnerability.beta_ind * sig)

            fitness_diff[i, j] = W_agg - W_ind

    # Custom colormap
    colors = ['#7b3294', '#c2a5cf', '#f7f7f7', '#fdae61', '#e66101']
    cmap = LinearSegmentedColormap.from_list('strategy', colors, N=256)

    # Panel A: Fitness difference
    ax1 = axes[0]
    extent = [sigma_vals.min(), sigma_vals.max(), cost_vals.min(), cost_vals.max()]
    im1 = ax1.imshow(fitness_diff, extent=extent, origin='lower',
                     aspect='auto', cmap=cmap, vmin=-0.3, vmax=0.3,
                     interpolation='bilinear')

    # Calculate and plot critical threshold line
    cost_line = np.linspace(0.05, 0.35, 50)
    sigma_stars = []
    for C_sig in cost_line:
        # Recalculate critical threshold with modified C_signal
        C_total = params.costs.C_travel + C_sig + params.costs.C_opportunity
        agg_base = (1 - C_total) * (1 + params.cooperation.b_coop * np.log(n)) * (1 + params.cooperation.B_recip)
        numerator = params.cooperation.R_ind - agg_base
        denominator = params.cooperation.R_ind * params.vulnerability.beta_ind - agg_base * params.vulnerability.alpha_agg * (1 - epsilon)
        if denominator > 0:
            sigma_stars.append(numerator / denominator)
        else:
            sigma_stars.append(np.nan)

    ax1.plot(sigma_stars, cost_line, 'k-', linewidth=2.5, label='Critical threshold σ*')
    ax1.plot(sigma_stars, cost_line, 'w--', linewidth=1.5)

    # Mark default cost
    ax1.axhline(params.costs.C_signal, color='gray', linestyle=':', linewidth=1, alpha=0.7)
    ax1.text(0.25, params.costs.C_signal + 0.01, f'Default C_signal = {params.costs.C_signal}', fontsize=9)

    ax1.set_xlabel('Environmental Uncertainty (σ)', fontsize=12)
    ax1.set_ylabel('Signaling Cost (C_signal)', fontsize=12)
    ax1.set_title('A. Strategy Dominance (ε = 0.35, n = 25 fixed)', fontsize=12, fontweight='bold')
    cbar1 = plt.colorbar(im1, ax=ax1, label='Fitness Difference (W_agg - W_ind)')
    cbar1.ax.set_ylabel('← Independent | Aggregation →', fontsize=9)
    ax1.legend(loc='upper left', fontsize=10)

    # Add region labels
    ax1.text(0.3, 0.30, 'Independent\nFavored', fontsize=11, ha='center', va='center',
             color='#7b3294', fontweight='bold',
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    ax1.text(0.75, 0.12, 'Aggregation\nFavored', fontsize=11, ha='center', va='center',
             color='#e66101', fontweight='bold',
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    # Panel B: How critical threshold varies with cost
    ax2 = axes[1]
    cost_range = np.linspace(0.05, 0.35, 100)

    for eps, color, label in [(0.15, '#d7191c', 'ε = 0.15 (low)'),
                               (0.35, '#1a9641', 'ε = 0.35 (Poverty Point)'),
                               (0.50, '#2b83ba', 'ε = 0.50 (high)')]:
        sigma_stars_eps = []
        for C_sig in cost_range:
            C_total = params.costs.C_travel + C_sig + params.costs.C_opportunity
            agg_base = (1 - C_total) * (1 + params.cooperation.b_coop * np.log(n)) * (1 + params.cooperation.B_recip)
            numerator = params.cooperation.R_ind - agg_base
            denominator = params.cooperation.R_ind * params.vulnerability.beta_ind - agg_base * params.vulnerability.alpha_agg * (1 - eps)
            if denominator > 0:
                sigma_stars_eps.append(max(0, min(1, numerator / denominator)))
            else:
                sigma_stars_eps.append(1.0)
        ax2.plot(cost_range, sigma_stars_eps, '-', linewidth=2.5, color=color, label=label)

    ax2.axvline(params.costs.C_signal, color='gray', linestyle=':', linewidth=1, alpha=0.7)
    ax2.text(params.costs.C_signal + 0.01, 0.75, f'Default\nC = {params.costs.C_signal}', fontsize=9)

    ax2.set_xlabel('Signaling Cost (C_signal)', fontsize=12)
    ax2.set_ylabel('Critical Threshold (σ*)', fontsize=12)
    ax2.set_title('B. Critical Threshold vs. Signaling Cost', fontsize=12, fontweight='bold')
    ax2.legend(loc='upper left', fontsize=10)
    ax2.set_xlim(0.05, 0.35)
    ax2.set_ylim(0.4, 0.9)
    ax2.grid(True, alpha=0.3)

    # Add annotation
    ax2.annotate('Higher costs\nraise the threshold',
                xy=(0.25, 0.62), xytext=(0.12, 0.75),
                fontsize=10, ha='center',
                arrowprops=dict(arrowstyle='->', color='black', lw=1.5))

    plt.tight_layout()
    return fig


def main():
    """Generate all phase space comparison figures."""
    print("=" * 60)
    print("Creating Phase Space Comparison Figures")
    print("=" * 60)

    # 1. Fine phase space (σ vs ε) from simulation
    results = load_fine_phase_space()
    if results:
        print("\n1. Creating fine σ vs ε figure from simulation...")
        fig1 = create_fine_phase_space_figure(results)
        fig1.savefig(OUTPUT_DIR / 'fig_phase_space.png', dpi=300, bbox_inches='tight')
        fig1.savefig(OUTPUT_DIR / 'fig_phase_space.pdf', bbox_inches='tight')
        plt.close(fig1)
        print("   Saved: fig_phase_space.png/pdf")
    else:
        print("   No fine phase space results found - skipping")

    # 2. σ vs aggregation size (theoretical)
    print("\n2. Creating σ vs aggregation size figure...")
    fig2 = create_sigma_vs_n_figure()
    fig2.savefig(OUTPUT_DIR / 'fig_sigma_vs_aggregation.png', dpi=300, bbox_inches='tight')
    fig2.savefig(OUTPUT_DIR / 'fig_sigma_vs_aggregation.pdf', bbox_inches='tight')
    plt.close(fig2)
    print("   Saved: fig_sigma_vs_aggregation.png/pdf")

    # 3. σ vs signaling cost (theoretical)
    print("\n3. Creating σ vs signaling cost figure...")
    fig3 = create_sigma_vs_cost_figure()
    fig3.savefig(OUTPUT_DIR / 'fig_sigma_vs_cost.png', dpi=300, bbox_inches='tight')
    fig3.savefig(OUTPUT_DIR / 'fig_sigma_vs_cost.pdf', bbox_inches='tight')
    plt.close(fig3)
    print("   Saved: fig_sigma_vs_cost.png/pdf")

    print("\n" + "=" * 60)
    print("All figures saved to:", OUTPUT_DIR)


if __name__ == "__main__":
    main()
