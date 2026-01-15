"""
Theoretical Phase Space Predictions for Aggregation-Based Costly Signaling

This script generates figures showing theoretical predictions BEFORE running the ABM,
derived directly from the multilevel selection framework adapted for hunter-gatherer
aggregation dynamics.

Key theoretical components:
1. Modified Price equation with environmental uncertainty (σ)
2. Ecotone advantage parameter (ε) - multi-zone buffering
3. Cooperation benefits function f(n)
4. Reciprocal obligations benefit (B_recip)
5. Critical threshold σ* for aggregation emergence
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import FancyBboxPatch
import matplotlib.patches as mpatches
from typing import Tuple, Dict
from dataclasses import dataclass


# =============================================================================
# THEORETICAL PARAMETERS
# =============================================================================

@dataclass
class TheoreticalParameters:
    """
    Parameters derived from theory for aggregation-based costly signaling.

    These parameters are calibrated to produce a meaningful phase transition:
    - At low σ (stable environment): independent foraging should dominate
    - At high σ (uncertain) + high ε (ecotone): aggregation should dominate
    - Transition should occur around σ* ≈ 0.35-0.50

    Key insight: The costs of aggregation must be substantial enough that
    aggregation is NOT always beneficial. Only under sufficient environmental
    uncertainty do the cooperation benefits outweigh the costs.
    """

    # Cost parameters - these are substantial to create realistic tradeoffs
    C_travel_base: float = 0.12      # Base travel cost (12% of resources)
    C_signal: float = 0.18           # Signaling cost during aggregation (18%)
    C_opportunity: float = 0.12      # Foregone foraging during aggregation
    # Total cost when aggregating: ~42% of resources

    # Vulnerability parameters (shortfall mortality)
    # Key: the difference (beta - alpha) drives the selection pressure
    alpha_agg: float = 0.40          # Aggregator vulnerability (buffered but still exposed)
    beta_ind: float = 0.75           # Independent vulnerability (exposed, but can sometimes avoid)

    # Cooperation benefit parameters
    # These must be modest enough that aggregation doesn't always win
    # With f(n) ~ 1.3 and costs ~ 0.42, aggregation needs high σ to be favored
    b_coop: float = 0.08             # Cooperation benefit coefficient (modest)
    n_optimal: int = 25              # Optimal aggregation size (bands)
    c_crowd: float = 0.015           # Crowding cost coefficient

    # Reciprocal obligation benefit - modest
    B_recip: float = 0.05            # Benefit from reciprocal obligations

    # Ecotone parameters
    epsilon_max: float = 0.50        # Maximum ecotone buffering


def cooperation_benefit(n: float, params: TheoreticalParameters) -> float:
    """
    Calculate cooperation benefits as function of aggregation size.

    f(n) = 1 + b * log(n) - crowding penalty if n > n*

    Returns multiplier on baseline fitness (1.0 = no benefit).
    """
    if n <= 1:
        return 1.0

    # Increasing returns from cooperation (logarithmic)
    benefit = 1.0 + params.b_coop * np.log(n)

    # Crowding costs kick in above optimal size
    if n > params.n_optimal:
        crowding = params.c_crowd * (n - params.n_optimal) ** 2
        benefit -= crowding

    return max(1.0, benefit)  # Can't be worse than going alone


def effective_sigma(sigma_regional: float, epsilon: float) -> float:
    """
    Calculate effective environmental uncertainty at ecotone.

    σ_effective = σ_regional * (1 - ε)

    Multi-zone access reduces effective uncertainty through buffering.
    """
    return sigma_regional * (1.0 - epsilon)


def W_aggregator(sigma: float, epsilon: float, n: float,
                 params: TheoreticalParameters) -> float:
    """
    Fitness function for aggregator strategy.

    W_agg = (1 - C_total) * (1 - α * σ_eff) * f(n) * (1 + B_recip)

    Where:
    - C_total = travel + signal + opportunity costs
    - σ_eff = effective uncertainty at ecotone
    - f(n) = cooperation benefits
    - B_recip = reciprocal obligation benefits
    """
    # Total costs
    C_total = params.C_travel_base + params.C_signal + params.C_opportunity

    # Effective uncertainty (reduced by ecotone buffering)
    sigma_eff = effective_sigma(sigma, epsilon)

    # Survival component (lower vulnerability due to buffering + pooling)
    survival = 1.0 - params.alpha_agg * sigma_eff

    # Cooperation benefits
    f_n = cooperation_benefit(n, params)

    # Reciprocal obligations
    recip = 1.0 + params.B_recip

    # Combined fitness
    W = (1.0 - C_total) * survival * f_n * recip

    return max(0.0, W)


def W_independent(sigma: float, params: TheoreticalParameters) -> float:
    """
    Fitness function for independent (non-aggregating) strategy.

    W_ind = R_ind * (1 - β * σ)

    Where R_ind represents the reproductive advantage of not paying aggregation costs.
    At low σ, independents have MORE resources for reproduction because they don't
    pay travel, signaling, or opportunity costs.

    Key insight: Independents have a reproductive advantage (no costs) but
    higher vulnerability during shortfalls. The tradeoff only favors aggregation
    when σ is high enough that vulnerability matters more than reproductive advantage.
    """
    # Reproductive advantage: independents keep resources that aggregators spend
    # This represents the demographic advantage of not aggregating
    R_ind = 1.10  # 10% reproductive advantage over aggregators

    # Survival component (higher vulnerability)
    survival = 1.0 - params.beta_ind * sigma

    return max(0.0, R_ind * survival)


def critical_threshold(epsilon: float, n: float,
                       params: TheoreticalParameters) -> float:
    """
    Calculate critical σ* where aggregation becomes adaptive.

    Setting W_agg = W_ind and solving for σ.

    W_agg = (1 - C_total) * (1 - α_eff * σ) * f(n) * (1 + B_recip)
    W_ind = R_ind * (1 - β * σ)

    At σ*, these are equal. Solving:
    (1 - C) * (1 - α_eff * σ) * f * r = R * (1 - β * σ)

    Let A = (1 - C) * f * r  (aggregation factor)
    A * (1 - α_eff * σ) = R * (1 - β * σ)
    A - A * α_eff * σ = R - R * β * σ
    R * β * σ - A * α_eff * σ = R - A
    σ * (R * β - A * α_eff) = R - A
    σ* = (R - A) / (R * β - A * α_eff)
    """
    C_total = params.C_travel_base + params.C_signal + params.C_opportunity
    f_n = cooperation_benefit(n, params)
    recip = 1.0 + params.B_recip

    # Independent reproductive advantage
    R_ind = 1.10

    # Aggregation factor
    A = (1.0 - C_total) * f_n * recip

    # Effective alpha (reduced by ecotone)
    alpha_eff = params.alpha_agg * (1.0 - epsilon)

    # Denominator
    denom = R_ind * params.beta_ind - A * alpha_eff

    if denom <= 0:
        # Aggregation always wins (even at σ=0)
        return 0.0

    # Numerator
    numerator = R_ind - A

    if numerator <= 0:
        # Aggregation always wins at σ=0
        return 0.0

    sigma_star = numerator / denom
    return max(0.0, min(1.0, sigma_star))


def strategy_dominance(sigma: float, epsilon: float, n: float,
                       params: TheoreticalParameters) -> float:
    """
    Calculate which strategy dominates at given parameters.

    Returns value in [-1, 1]:
    - Positive = aggregation dominates
    - Negative = independent dominates
    - Magnitude indicates strength of selection
    """
    W_agg = W_aggregator(sigma, epsilon, n, params)
    W_ind = W_independent(sigma, params)

    # Avoid division by zero
    W_total = W_agg + W_ind
    if W_total < 0.001:
        return 0.0

    # Normalized difference
    dominance = (W_agg - W_ind) / W_total
    return dominance


# =============================================================================
# FIGURE 1: BASIC PHASE SPACE (σ vs ε)
# =============================================================================

def create_phase_space_sigma_epsilon(params: TheoreticalParameters,
                                     n_fixed: float = 25.0) -> plt.Figure:
    """
    Create phase space plot showing strategy dominance as function of
    environmental uncertainty (σ) and ecotone advantage (ε).

    This is the primary theoretical prediction figure.
    """
    fig, ax = plt.subplots(figsize=(10, 8))

    # Parameter ranges
    sigma_range = np.linspace(0.1, 0.9, 100)
    epsilon_range = np.linspace(0.0, 0.5, 100)

    # Calculate dominance across phase space
    dominance = np.zeros((len(epsilon_range), len(sigma_range)))

    for i, eps in enumerate(epsilon_range):
        for j, sig in enumerate(sigma_range):
            dominance[i, j] = strategy_dominance(sig, eps, n_fixed, params)

    # Custom colormap: purple (independent) to white to orange (aggregation)
    colors = ['#7b3294', '#c2a5cf', '#f7f7f7', '#fdae61', '#e66101']
    cmap = LinearSegmentedColormap.from_list('strategy', colors, N=256)

    # Plot phase space
    im = ax.imshow(dominance, extent=[0.1, 0.9, 0.0, 0.5],
                   origin='lower', aspect='auto', cmap=cmap, vmin=-1, vmax=1)

    # Calculate and plot critical threshold line
    sigma_stars = []
    for eps in epsilon_range:
        s_star = critical_threshold(eps, n_fixed, params)
        sigma_stars.append(s_star)

    ax.plot(sigma_stars, epsilon_range, 'k-', linewidth=2.5, label='σ* (critical threshold)')
    ax.plot(sigma_stars, epsilon_range, 'w--', linewidth=1.5)

    # Mark key regions
    ax.annotate('AGGREGATION\nDOMINATES', xy=(0.7, 0.35), fontsize=12,
                ha='center', va='center', fontweight='bold', color='#8c510a')
    ax.annotate('INDEPENDENT\nDOMINATES', xy=(0.25, 0.15), fontsize=12,
                ha='center', va='center', fontweight='bold', color='#542788')

    # Mark hypothesized Poverty Point location
    ax.plot(0.55, 0.40, 'k*', markersize=20, markeredgecolor='white',
            markeredgewidth=2, label='Poverty Point (hypothesized)')

    # Mark hypothesized conditions for secondary sites
    ax.plot(0.50, 0.20, 'ks', markersize=12, markeredgecolor='white',
            markeredgewidth=1.5, label='Secondary sites (Jaketown, etc.)')

    # Labels and formatting
    ax.set_xlabel('Environmental Uncertainty (σ)', fontsize=12)
    ax.set_ylabel('Ecotone Advantage (ε)', fontsize=12)
    ax.set_title('Theoretical Phase Space: Aggregation-Based Costly Signaling\n'
                 f'(n = {n_fixed} bands at aggregation)', fontsize=14)

    # Colorbar
    cbar = plt.colorbar(im, ax=ax, label='Strategy Dominance', shrink=0.8)
    cbar.ax.set_ylabel('← Independent | Aggregation →', fontsize=10)

    ax.legend(loc='upper left', framealpha=0.9)

    plt.tight_layout()
    return fig


# =============================================================================
# FIGURE 2: FITNESS FUNCTIONS vs SIGMA
# =============================================================================

def create_fitness_curves(params: TheoreticalParameters) -> plt.Figure:
    """
    Show how fitness varies with σ for different strategies and ecotone values.
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    sigma_range = np.linspace(0.1, 0.9, 100)
    n_fixed = 25.0

    # Panel A: Fitness curves at different ecotone values
    ax1 = axes[0]

    epsilon_values = [0.0, 0.2, 0.4]
    colors_agg = ['#fdae61', '#e66101', '#b35806']

    # Independent fitness (same regardless of epsilon)
    W_ind = [W_independent(s, params) for s in sigma_range]
    ax1.plot(sigma_range, W_ind, 'b-', linewidth=2.5, label='Independent')

    # Aggregator fitness at different epsilon
    for eps, color in zip(epsilon_values, colors_agg):
        W_agg = [W_aggregator(s, eps, n_fixed, params) for s in sigma_range]
        ax1.plot(sigma_range, W_agg, '-', color=color, linewidth=2,
                 label=f'Aggregator (ε={eps})')

        # Mark crossover point
        sigma_star = critical_threshold(eps, n_fixed, params)
        if 0.1 < sigma_star < 0.9:
            ax1.axvline(sigma_star, color=color, linestyle=':', alpha=0.7)
            ax1.plot(sigma_star, W_independent(sigma_star, params), 'o',
                    color=color, markersize=8)

    ax1.set_xlabel('Environmental Uncertainty (σ)', fontsize=12)
    ax1.set_ylabel('Fitness (W)', fontsize=12)
    ax1.set_title('A. Fitness Functions by Ecotone Advantage', fontsize=12)
    ax1.legend(loc='upper right', fontsize=9)
    ax1.set_xlim(0.1, 0.9)
    ax1.set_ylim(0, 1.2)
    ax1.grid(True, alpha=0.3)

    # Panel B: Critical threshold as function of ecotone advantage
    ax2 = axes[1]

    epsilon_range = np.linspace(0.0, 0.5, 50)
    n_values = [15, 25, 40]
    colors_n = ['#1b7837', '#5aae61', '#a6dba0']

    for n, color in zip(n_values, colors_n):
        sigma_stars = [critical_threshold(eps, n, params) for eps in epsilon_range]
        ax2.plot(epsilon_range, sigma_stars, '-', color=color, linewidth=2,
                 label=f'n = {n} bands')

    ax2.axhline(0.5, color='gray', linestyle='--', alpha=0.5,
                label='Rapa Nui σ* (territorial)')

    ax2.set_xlabel('Ecotone Advantage (ε)', fontsize=12)
    ax2.set_ylabel('Critical Threshold (σ*)', fontsize=12)
    ax2.set_title('B. Critical Threshold vs Ecotone Advantage', fontsize=12)
    ax2.legend(loc='upper right', fontsize=9)
    ax2.set_xlim(0.0, 0.5)
    ax2.set_ylim(0.0, 0.8)
    ax2.grid(True, alpha=0.3)

    # Shade region where aggregation has lower threshold than territorial
    ax2.fill_between(epsilon_range, 0, 0.5, alpha=0.1, color='orange',
                     label='Aggregation favored over territorial')

    plt.tight_layout()
    return fig


# =============================================================================
# FIGURE 3: COOPERATION BENEFITS FUNCTION
# =============================================================================

def create_cooperation_benefits_figure(params: TheoreticalParameters) -> plt.Figure:
    """
    Show the cooperation benefits function f(n) and how it affects fitness.
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Panel A: f(n) function shape
    ax1 = axes[0]

    n_range = np.linspace(1, 60, 100)
    f_n = [cooperation_benefit(n, params) for n in n_range]

    ax1.plot(n_range, f_n, 'b-', linewidth=2.5)
    ax1.axvline(params.n_optimal, color='red', linestyle='--',
                label=f'Optimal n* = {params.n_optimal}')
    ax1.axhline(1.0, color='gray', linestyle=':', alpha=0.5)

    # Shade regions
    ax1.fill_between(n_range[n_range <= params.n_optimal], 1.0,
                     [cooperation_benefit(n, params) for n in n_range[n_range <= params.n_optimal]],
                     alpha=0.3, color='green', label='Increasing returns')
    ax1.fill_between(n_range[n_range >= params.n_optimal],
                     [cooperation_benefit(n, params) for n in n_range[n_range >= params.n_optimal]],
                     [cooperation_benefit(params.n_optimal, params)] * sum(n_range >= params.n_optimal),
                     alpha=0.3, color='red', label='Crowding costs')

    ax1.set_xlabel('Aggregation Size (n bands)', fontsize=12)
    ax1.set_ylabel('Cooperation Benefit Multiplier f(n)', fontsize=12)
    ax1.set_title('A. Returns to Aggregation Size', fontsize=12)
    ax1.legend(loc='upper right', fontsize=9)
    ax1.set_xlim(1, 60)
    ax1.grid(True, alpha=0.3)

    # Panel B: How n affects critical threshold
    ax2 = axes[1]

    n_range = np.arange(5, 55, 5)
    epsilon_values = [0.1, 0.25, 0.4]
    colors = ['#fee8c8', '#fdbb84', '#e34a33']

    for eps, color in zip(epsilon_values, colors):
        sigma_stars = [critical_threshold(eps, n, params) for n in n_range]
        ax2.plot(n_range, sigma_stars, 'o-', color=color, linewidth=2,
                 markersize=8, label=f'ε = {eps}')

    ax2.axhline(0.5, color='gray', linestyle='--', alpha=0.5,
                label='Territorial σ*')

    ax2.set_xlabel('Aggregation Size (n bands)', fontsize=12)
    ax2.set_ylabel('Critical Threshold (σ*)', fontsize=12)
    ax2.set_title('B. How Aggregation Size Affects Critical Threshold', fontsize=12)
    ax2.legend(loc='upper right', fontsize=9)
    ax2.set_xlim(5, 55)
    ax2.set_ylim(0.0, 0.8)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    return fig


# =============================================================================
# FIGURE 4: THREE-DIMENSIONAL PHASE SPACE (σ, ε, n)
# =============================================================================

def create_3d_phase_space(params: TheoreticalParameters) -> plt.Figure:
    """
    Show how the three key parameters interact to determine strategy dominance.
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))

    # Custom colormap
    colors = ['#7b3294', '#c2a5cf', '#f7f7f7', '#fdae61', '#e66101']
    cmap = LinearSegmentedColormap.from_list('strategy', colors, N=256)

    # Panel A: Low aggregation size (n=10)
    ax1 = axes[0, 0]
    n_low = 10
    sigma_range = np.linspace(0.1, 0.9, 50)
    epsilon_range = np.linspace(0.0, 0.5, 50)
    dominance = np.zeros((len(epsilon_range), len(sigma_range)))
    for i, eps in enumerate(epsilon_range):
        for j, sig in enumerate(sigma_range):
            dominance[i, j] = strategy_dominance(sig, eps, n_low, params)

    im1 = ax1.imshow(dominance, extent=[0.1, 0.9, 0.0, 0.5],
                     origin='lower', aspect='auto', cmap=cmap, vmin=-1, vmax=1)
    sigma_stars = [critical_threshold(eps, n_low, params) for eps in epsilon_range]
    ax1.plot(sigma_stars, epsilon_range, 'k-', linewidth=2)
    ax1.set_title(f'A. Small Aggregation (n={n_low} bands)', fontsize=12)
    ax1.set_xlabel('σ')
    ax1.set_ylabel('ε')

    # Panel B: Medium aggregation size (n=25)
    ax2 = axes[0, 1]
    n_med = 25
    dominance = np.zeros((len(epsilon_range), len(sigma_range)))
    for i, eps in enumerate(epsilon_range):
        for j, sig in enumerate(sigma_range):
            dominance[i, j] = strategy_dominance(sig, eps, n_med, params)

    im2 = ax2.imshow(dominance, extent=[0.1, 0.9, 0.0, 0.5],
                     origin='lower', aspect='auto', cmap=cmap, vmin=-1, vmax=1)
    sigma_stars = [critical_threshold(eps, n_med, params) for eps in epsilon_range]
    ax2.plot(sigma_stars, epsilon_range, 'k-', linewidth=2)
    ax2.set_title(f'B. Optimal Aggregation (n={n_med} bands)', fontsize=12)
    ax2.set_xlabel('σ')
    ax2.set_ylabel('ε')

    # Panel C: Large aggregation size (n=45)
    ax3 = axes[1, 0]
    n_high = 45
    dominance = np.zeros((len(epsilon_range), len(sigma_range)))
    for i, eps in enumerate(epsilon_range):
        for j, sig in enumerate(sigma_range):
            dominance[i, j] = strategy_dominance(sig, eps, n_high, params)

    im3 = ax3.imshow(dominance, extent=[0.1, 0.9, 0.0, 0.5],
                     origin='lower', aspect='auto', cmap=cmap, vmin=-1, vmax=1)
    sigma_stars = [critical_threshold(eps, n_high, params) for eps in epsilon_range]
    ax3.plot(sigma_stars, epsilon_range, 'k-', linewidth=2)
    ax3.set_title(f'C. Large Aggregation (n={n_high} bands, crowding)', fontsize=12)
    ax3.set_xlabel('σ')
    ax3.set_ylabel('ε')

    # Panel D: σ* surface as function of ε and n
    ax4 = axes[1, 1]
    epsilon_range_d = np.linspace(0.05, 0.45, 20)
    n_range_d = np.arange(10, 50, 5)

    for n in n_range_d:
        sigma_stars = [critical_threshold(eps, n, params) for eps in epsilon_range_d]
        color = plt.cm.viridis((n - 10) / 40)
        ax4.plot(epsilon_range_d, sigma_stars, '-', color=color, linewidth=1.5,
                 label=f'n={n}' if n in [10, 25, 45] else None)

    ax4.set_xlabel('Ecotone Advantage (ε)', fontsize=12)
    ax4.set_ylabel('Critical Threshold (σ*)', fontsize=12)
    ax4.set_title('D. Critical Threshold Across Parameters', fontsize=12)
    ax4.legend(loc='upper right', fontsize=9)
    ax4.grid(True, alpha=0.3)

    # Add colorbar
    cbar = fig.colorbar(im2, ax=axes, shrink=0.6, label='Strategy Dominance')
    cbar.ax.set_ylabel('← Independent | Aggregation →', fontsize=10)

    plt.tight_layout()
    return fig


# =============================================================================
# FIGURE 5: PREDICTED SITE HIERARCHY
# =============================================================================

def create_site_hierarchy_prediction(params: TheoreticalParameters) -> plt.Figure:
    """
    Show theoretical prediction for regional site hierarchy based on
    ecotone access at different locations.
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Panel A: Distance decay in participation
    ax1 = axes[0]

    # Model: participation probability declines with distance
    distance_range = np.linspace(0, 300, 100)  # km from ecotone center

    # At different sigma levels
    sigma_values = [0.4, 0.55, 0.7]
    colors = ['#a6dba0', '#5aae61', '#1b7837']

    for sigma, color in zip(sigma_values, colors):
        # Travel cost increases with distance
        C_travel = params.C_travel_base + 0.001 * distance_range

        # Participation probability (simplified logistic)
        W_agg_dist = [(1.0 - c_t - params.C_signal - params.C_opportunity) *
                      (1.0 - params.alpha_agg * sigma * (1 - 0.3)) *
                      cooperation_benefit(25, params) * (1 + params.B_recip)
                      for c_t in C_travel]
        W_ind = W_independent(sigma, params)

        participation = [1 / (1 + np.exp(-10 * (w_a - W_ind))) for w_a in W_agg_dist]

        ax1.plot(distance_range, participation, '-', color=color, linewidth=2,
                 label=f'σ = {sigma}')

    ax1.set_xlabel('Distance from Aggregation Center (km)', fontsize=12)
    ax1.set_ylabel('Probability of Aggregation Participation', fontsize=12)
    ax1.set_title('A. Distance Decay in Aggregation Participation', fontsize=12)
    ax1.legend(loc='upper right', fontsize=10)
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(0, 300)
    ax1.set_ylim(0, 1.05)

    # Panel B: Expected site hierarchy
    ax2 = axes[1]

    # Hypothetical sites with different ecotone access
    sites = {
        'Poverty Point': {'epsilon': 0.40, 'distance': 0, 'sigma': 0.55},
        'Jaketown': {'epsilon': 0.25, 'distance': 150, 'sigma': 0.55},
        'Claiborne': {'epsilon': 0.20, 'distance': 200, 'sigma': 0.50},
        'J.W. Copes': {'epsilon': 0.15, 'distance': 100, 'sigma': 0.55},
        'Small camps': {'epsilon': 0.10, 'distance': 50, 'sigma': 0.55}
    }

    # Calculate predicted relative investment
    investments = {}
    for site, props in sites.items():
        # Aggregation benefit at this site
        n_expected = 25 * (1 - props['distance'] / 500)  # Fewer bands with distance
        n_expected = max(5, n_expected)

        W_agg = W_aggregator(props['sigma'], props['epsilon'], n_expected, params)
        W_ind = W_independent(props['sigma'], params)

        # Investment proportional to fitness advantage
        advantage = max(0, W_agg - W_ind)
        investments[site] = advantage * n_expected * 10  # Scale for visualization

    # Bar plot
    sites_list = list(investments.keys())
    values = list(investments.values())
    colors = ['#e66101', '#fdae61', '#fee8c8', '#f7f7f7', '#d9d9d9']

    bars = ax2.barh(sites_list, values, color=colors, edgecolor='black')
    ax2.set_xlabel('Predicted Relative Monument Investment', fontsize=12)
    ax2.set_title('B. Predicted Site Hierarchy from Theory', fontsize=12)
    ax2.set_xlim(0, max(values) * 1.2)

    # Add ecotone values as annotations
    for i, (site, props) in enumerate(sites.items()):
        ax2.annotate(f'ε={props["epsilon"]}',
                     xy=(values[i] + max(values) * 0.02, i),
                     va='center', fontsize=9)

    plt.tight_layout()
    return fig


# =============================================================================
# FIGURE 6: TEMPORAL PREDICTIONS
# =============================================================================

def create_temporal_predictions(params: TheoreticalParameters) -> plt.Figure:
    """
    Show predicted dynamics over time given environmental variation.
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Simulate 600 years (1700-1100 BCE)
    years = np.arange(0, 600)

    # Panel A: Environmental uncertainty over time (hypothetical)
    ax1 = axes[0, 0]

    # Create plausible sigma trajectory
    np.random.seed(42)
    sigma_base = 0.50
    sigma_trend = sigma_base + 0.15 * np.sin(2 * np.pi * years / 200)  # Long cycle
    sigma_noise = 0.05 * np.random.randn(len(years))
    sigma_time = np.clip(sigma_trend + sigma_noise, 0.2, 0.8)

    ax1.plot(years, sigma_time, 'b-', linewidth=1, alpha=0.7)
    ax1.plot(years, sigma_trend, 'b-', linewidth=2, label='Trend')
    ax1.axhline(0.45, color='red', linestyle='--', label='σ* (critical)', alpha=0.7)
    ax1.fill_between(years, sigma_time, 0.45, where=sigma_time > 0.45,
                     alpha=0.3, color='orange', label='Aggregation favored')
    ax1.fill_between(years, sigma_time, 0.45, where=sigma_time < 0.45,
                     alpha=0.3, color='purple', label='Independence favored')

    ax1.set_xlabel('Years from Start', fontsize=12)
    ax1.set_ylabel('Environmental Uncertainty (σ)', fontsize=12)
    ax1.set_title('A. Hypothetical Environmental Trajectory', fontsize=12)
    ax1.legend(loc='upper right', fontsize=9)
    ax1.set_xlim(0, 600)

    # Panel B: Predicted aggregation intensity
    ax2 = axes[0, 1]

    epsilon_fixed = 0.35
    n_base = 25

    # Aggregation intensity proportional to fitness advantage
    aggregation_intensity = []
    for sig in sigma_time:
        W_agg = W_aggregator(sig, epsilon_fixed, n_base, params)
        W_ind = W_independent(sig, params)
        intensity = max(0, (W_agg - W_ind) / W_ind) if W_ind > 0 else 0
        aggregation_intensity.append(intensity)

    ax2.plot(years, aggregation_intensity, 'orange', linewidth=1.5)
    ax2.fill_between(years, 0, aggregation_intensity, alpha=0.3, color='orange')

    ax2.set_xlabel('Years from Start', fontsize=12)
    ax2.set_ylabel('Aggregation Intensity', fontsize=12)
    ax2.set_title('B. Predicted Aggregation Intensity', fontsize=12)
    ax2.set_xlim(0, 600)

    # Panel C: Predicted cumulative monument investment
    ax3 = axes[1, 0]

    # Monument investment proportional to aggregation intensity
    monument_rate = np.array(aggregation_intensity) * 100  # Scale factor
    monument_cumulative = np.cumsum(monument_rate)

    ax3.plot(years, monument_cumulative, 'brown', linewidth=2)
    ax3.fill_between(years, 0, monument_cumulative, alpha=0.3, color='brown')

    ax3.set_xlabel('Years from Start', fontsize=12)
    ax3.set_ylabel('Cumulative Monument Investment (units)', fontsize=12)
    ax3.set_title('C. Predicted Cumulative Construction', fontsize=12)
    ax3.set_xlim(0, 600)

    # Panel D: Construction rate over time
    ax4 = axes[1, 1]

    # Smooth the rate
    window = 20
    construction_rate_smooth = np.convolve(monument_rate,
                                           np.ones(window)/window, mode='same')

    ax4.plot(years, construction_rate_smooth, 'brown', linewidth=2)
    ax4.fill_between(years, 0, construction_rate_smooth, alpha=0.3, color='brown')

    # Mark periods of high vs low construction
    high_construction = construction_rate_smooth > np.percentile(construction_rate_smooth, 75)
    ax4.fill_between(years, 0, construction_rate_smooth, where=high_construction,
                     alpha=0.5, color='red', label='High construction')

    ax4.set_xlabel('Years from Start', fontsize=12)
    ax4.set_ylabel('Construction Rate (units/year)', fontsize=12)
    ax4.set_title('D. Predicted Construction Rate Over Time', fontsize=12)
    ax4.legend(loc='upper right', fontsize=9)
    ax4.set_xlim(0, 600)

    plt.tight_layout()
    return fig


# =============================================================================
# FIGURE 7: SUMMARY PREDICTIONS DIAGRAM
# =============================================================================

def create_summary_predictions(params: TheoreticalParameters) -> plt.Figure:
    """
    Create a summary diagram showing the key theoretical predictions.
    """
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Title
    ax.text(7, 9.5, 'Theoretical Predictions: Aggregation-Based Costly Signaling',
            fontsize=16, ha='center', fontweight='bold')
    ax.text(7, 9.0, 'Derived from Multilevel Selection Framework',
            fontsize=12, ha='center', style='italic')

    # Core prediction box
    core_box = FancyBboxPatch((0.5, 6.5), 6, 2, boxstyle="round,pad=0.1",
                               facecolor='#fff7bc', edgecolor='black', linewidth=2)
    ax.add_patch(core_box)
    ax.text(3.5, 8.0, 'CORE PREDICTION', fontsize=12, ha='center', fontweight='bold')
    ax.text(3.5, 7.3, 'Aggregation + costly signaling emerges when:', fontsize=10, ha='center')
    ax.text(3.5, 6.9, 'σ > σ* AND ε > ε_min', fontsize=11, ha='center',
            fontfamily='monospace', fontweight='bold')

    # Parameter box
    param_box = FancyBboxPatch((7.5, 6.5), 6, 2, boxstyle="round,pad=0.1",
                                facecolor='#d9f0d3', edgecolor='black', linewidth=2)
    ax.add_patch(param_box)
    ax.text(10.5, 8.0, 'KEY PARAMETERS', fontsize=12, ha='center', fontweight='bold')
    ax.text(8.0, 7.5, f'σ* ≈ 0.53 (at ε=0.35, n=25)', fontsize=9, ha='left')
    ax.text(8.0, 7.1, f'ε_min ≈ 0.20 (minimum ecotone)', fontsize=9, ha='left')
    ax.text(8.0, 6.7, f'n* ≈ 25 bands (optimal size)', fontsize=9, ha='left')

    # Spatial predictions
    spatial_box = FancyBboxPatch((0.5, 3.5), 4, 2.5, boxstyle="round,pad=0.1",
                                  facecolor='#c2e0ff', edgecolor='black', linewidth=1.5)
    ax.add_patch(spatial_box)
    ax.text(2.5, 5.7, 'SPATIAL', fontsize=11, ha='center', fontweight='bold')
    ax.text(0.7, 5.2, '• Site primacy at max ecotone', fontsize=9, ha='left')
    ax.text(0.7, 4.8, '• Distance decay in participation', fontsize=9, ha='left')
    ax.text(0.7, 4.4, '• Hierarchy: PP >> secondary sites', fontsize=9, ha='left')
    ax.text(0.7, 4.0, '• Multi-directional exotic sources', fontsize=9, ha='left')

    # Temporal predictions
    temporal_box = FancyBboxPatch((5, 3.5), 4, 2.5, boxstyle="round,pad=0.1",
                                   facecolor='#ffe0cc', edgecolor='black', linewidth=1.5)
    ax.add_patch(temporal_box)
    ax.text(7, 5.7, 'TEMPORAL', fontsize=11, ha='center', fontweight='bold')
    ax.text(5.2, 5.2, '• Construction ∝ uncertainty', fontsize=9, ha='left')
    ax.text(5.2, 4.8, '• Pulses during high σ periods', fontsize=9, ha='left')
    ax.text(5.2, 4.4, '• Gradual exotic accumulation', fontsize=9, ha='left')
    ax.text(5.2, 4.0, '• Collapse when σ < σ* persists', fontsize=9, ha='left')

    # Individual predictions
    indiv_box = FancyBboxPatch((9.5, 3.5), 4, 2.5, boxstyle="round,pad=0.1",
                                facecolor='#e0ccff', edgecolor='black', linewidth=1.5)
    ax.add_patch(indiv_box)
    ax.text(11.5, 5.7, 'INDIVIDUAL', fontsize=11, ha='center', fontweight='bold')
    ax.text(9.7, 5.2, '• Exotic variation among bands', fontsize=9, ha='left')
    ax.text(9.7, 4.8, '• Contribution ∝ surplus', fontsize=9, ha='left')
    ax.text(9.7, 4.4, '• Reciprocal obligation network', fontsize=9, ha='left')
    ax.text(9.7, 4.0, '• Prestige affects partnerships', fontsize=9, ha='left')

    # Testable hypotheses
    test_box = FancyBboxPatch((0.5, 0.5), 13, 2.5, boxstyle="round,pad=0.1",
                               facecolor='#f0f0f0', edgecolor='black', linewidth=2)
    ax.add_patch(test_box)
    ax.text(7, 2.7, 'TESTABLE HYPOTHESES', fontsize=12, ha='center', fontweight='bold')

    ax.text(0.7, 2.2, 'H1: PP location optimal for ecotone access', fontsize=9, ha='left')
    ax.text(0.7, 1.8, 'H2: Construction correlates with σ proxies', fontsize=9, ha='left')
    ax.text(0.7, 1.4, 'H3: Exotics concentrated at aggregation sites', fontsize=9, ha='left')
    ax.text(7.2, 2.2, 'H4: Site size declines with distance from PP', fontsize=9, ha='left')
    ax.text(7.2, 1.8, 'H5: Collapse correlates with σ decline or ε shift', fontsize=9, ha='left')
    ax.text(7.2, 1.4, 'H6: Individual exotic holdings show variation', fontsize=9, ha='left')

    # Arrows connecting boxes
    ax.annotate('', xy=(3.5, 6.5), xytext=(3.5, 6.0),
                arrowprops=dict(arrowstyle='->', color='black', lw=1.5))
    ax.annotate('', xy=(7, 6.5), xytext=(7, 6.0),
                arrowprops=dict(arrowstyle='->', color='black', lw=1.5))
    ax.annotate('', xy=(11.5, 6.5), xytext=(11.5, 6.0),
                arrowprops=dict(arrowstyle='->', color='black', lw=1.5))

    plt.tight_layout()
    return fig


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def generate_all_figures(output_dir: str = 'figures/theoretical/'):
    """Generate all theoretical prediction figures."""
    import os

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Initialize parameters
    params = TheoreticalParameters()

    print("Generating theoretical prediction figures...")
    print(f"Parameters: C_signal={params.C_signal}, α={params.alpha_agg}, "
          f"β={params.beta_ind}, b_coop={params.b_coop}")

    # Calculate and report critical threshold at reference conditions
    sigma_star_ref = critical_threshold(epsilon=0.35, n=25, params=params)
    print(f"Critical threshold σ* at ε=0.35, n=25: {sigma_star_ref:.3f}")

    # Figure 1: Main phase space
    print("  Figure 1: Phase space (σ vs ε)...")
    fig1 = create_phase_space_sigma_epsilon(params)
    fig1.savefig(f'{output_dir}fig1_phase_space_sigma_epsilon.png', dpi=150,
                 bbox_inches='tight', facecolor='white')
    fig1.savefig(f'{output_dir}fig1_phase_space_sigma_epsilon.pdf',
                 bbox_inches='tight', facecolor='white')
    plt.close(fig1)

    # Figure 2: Fitness curves
    print("  Figure 2: Fitness curves...")
    fig2 = create_fitness_curves(params)
    fig2.savefig(f'{output_dir}fig2_fitness_curves.png', dpi=150,
                 bbox_inches='tight', facecolor='white')
    fig2.savefig(f'{output_dir}fig2_fitness_curves.pdf',
                 bbox_inches='tight', facecolor='white')
    plt.close(fig2)

    # Figure 3: Cooperation benefits
    print("  Figure 3: Cooperation benefits function...")
    fig3 = create_cooperation_benefits_figure(params)
    fig3.savefig(f'{output_dir}fig3_cooperation_benefits.png', dpi=150,
                 bbox_inches='tight', facecolor='white')
    fig3.savefig(f'{output_dir}fig3_cooperation_benefits.pdf',
                 bbox_inches='tight', facecolor='white')
    plt.close(fig3)

    # Figure 4: 3D phase space
    print("  Figure 4: 3D phase space (σ, ε, n)...")
    fig4 = create_3d_phase_space(params)
    fig4.savefig(f'{output_dir}fig4_3d_phase_space.png', dpi=150,
                 bbox_inches='tight', facecolor='white')
    fig4.savefig(f'{output_dir}fig4_3d_phase_space.pdf',
                 bbox_inches='tight', facecolor='white')
    plt.close(fig4)

    # Figure 5: Site hierarchy prediction
    print("  Figure 5: Site hierarchy prediction...")
    fig5 = create_site_hierarchy_prediction(params)
    fig5.savefig(f'{output_dir}fig5_site_hierarchy.png', dpi=150,
                 bbox_inches='tight', facecolor='white')
    fig5.savefig(f'{output_dir}fig5_site_hierarchy.pdf',
                 bbox_inches='tight', facecolor='white')
    plt.close(fig5)

    # Figure 6: Temporal predictions
    print("  Figure 6: Temporal predictions...")
    fig6 = create_temporal_predictions(params)
    fig6.savefig(f'{output_dir}fig6_temporal_predictions.png', dpi=150,
                 bbox_inches='tight', facecolor='white')
    fig6.savefig(f'{output_dir}fig6_temporal_predictions.pdf',
                 bbox_inches='tight', facecolor='white')
    plt.close(fig6)

    # Figure 7: Summary predictions
    print("  Figure 7: Summary predictions diagram...")
    fig7 = create_summary_predictions(params)
    fig7.savefig(f'{output_dir}fig7_summary_predictions.png', dpi=150,
                 bbox_inches='tight', facecolor='white')
    fig7.savefig(f'{output_dir}fig7_summary_predictions.pdf',
                 bbox_inches='tight', facecolor='white')
    plt.close(fig7)

    print(f"\nAll figures saved to {output_dir}")
    print("PNG and PDF versions created for each figure.")

    return params


if __name__ == "__main__":
    params = generate_all_figures()
