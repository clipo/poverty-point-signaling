#!/usr/bin/env python3
"""
Create 3-Panel Environmental Variability Figure

This figure illustrates how environmental uncertainty (σ) emerges from:
1. Shortfall frequency (how often shortfalls occur) - shown as bar chart
2. Shortfall magnitude (how severe shortfalls are) - shown as line depth plot
3. Combined effect (frequency × magnitude interaction) - shown as heatmap

Redesigned to make panels A and B visually distinct with clearer differentiation
between the three levels in each.
"""

import sys
sys.path.insert(0, '/Users/clipo/PycharmProjects/poverty-point-signaling')

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Output directory
OUTPUT_DIR = Path('/Users/clipo/PycharmProjects/poverty-point-signaling/figures/integrated')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Set random seed for reproducibility
np.random.seed(42)


def create_environmental_variability_figure():
    """
    Create the 3-panel environmental variability figure with distinct panel styles.
    """
    fig = plt.figure(figsize=(16, 5.5))

    # Create gridspec for flexible layout
    gs = fig.add_gridspec(1, 3, width_ratios=[1, 1, 1.1], wspace=0.3)

    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    ax3 = fig.add_subplot(gs[0, 2])

    # ===============================================
    # Panel A: FREQUENCY - Vertical timeline showing shortfall events
    # ===============================================

    years = 50
    np.random.seed(42)

    # Generate shortfall events for three frequency scenarios
    freq_scenarios = {
        'Rare\n(every 18 yr)': {'interval': 18, 'color': '#2166ac', 'events': []},
        'Moderate\n(every 10 yr)': {'interval': 10, 'color': '#f4a582', 'events': []},
        'Frequent\n(every 6 yr)': {'interval': 6, 'color': '#b2182b', 'events': []},
    }

    # Generate events for each scenario
    for name, params in freq_scenarios.items():
        current = 0
        events = []
        while current < years:
            current += int(np.random.exponential(params['interval']))
            if current < years:
                events.append(current)
        params['events'] = events

    # Plot as horizontal bars with event markers
    y_positions = [2, 1, 0]
    bar_height = 0.6

    for idx, (name, params) in enumerate(freq_scenarios.items()):
        y = y_positions[idx]

        # Draw baseline bar (years without shortfall)
        ax1.barh(y, years, height=bar_height, color='#e0e0e0', edgecolor='none')

        # Draw shortfall events as vertical bars
        for event in params['events']:
            ax1.barh(y, 2, left=event, height=bar_height,
                    color=params['color'], edgecolor='black', linewidth=0.5)

        # Add event count
        n_events = len(params['events'])
        ax1.text(years + 2, y, f'n={n_events}', va='center', ha='left',
                fontsize=10, fontweight='bold', color=params['color'])

    ax1.set_yticks(y_positions)
    ax1.set_yticklabels(list(freq_scenarios.keys()), fontsize=10)
    ax1.set_xlabel('Year', fontsize=11)
    ax1.set_xlim(0, years + 8)
    ax1.set_ylim(-0.5, 2.5)
    ax1.set_title('A. Shortfall Frequency\n(magnitude fixed at 45%)', fontsize=12, fontweight='bold')
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)

    # Add legend
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor='#e0e0e0', label='Normal years'),
                       Patch(facecolor='#b2182b', edgecolor='black', label='Shortfall event')]
    ax1.legend(handles=legend_elements, loc='upper right', fontsize=9)

    # Add arrow showing "more events → higher σ"
    ax1.annotate('', xy=(years-5, -0.3), xytext=(years-5, 2.3),
                arrowprops=dict(arrowstyle='->', color='black', lw=2))
    ax1.text(years-3, 1, 'Higher σ', rotation=90, va='center', fontsize=9, fontweight='bold')

    # ===============================================
    # Panel B: MAGNITUDE - Depth profiles showing shortfall severity
    # ===============================================

    np.random.seed(123)  # Different seed for different pattern

    # Create depth profiles for three magnitude scenarios
    mag_scenarios = [
        ('Mild (30%)', 0.30, '#2166ac'),
        ('Moderate (45%)', 0.45, '#f4a582'),
        ('Severe (60%)', 0.60, '#b2182b'),
    ]

    years_b = 60
    time = np.arange(years_b)

    # Fixed shortfall timing (every ~10 years) but varying magnitude
    shortfall_times = [8, 19, 31, 42, 53]

    for idx, (label, magnitude, color) in enumerate(mag_scenarios):
        # Create productivity profile
        productivity = np.ones(years_b)

        # Add shortfalls at fixed times with this scenario's magnitude
        for t in shortfall_times:
            if t < years_b:
                # Duration scales with magnitude
                duration = max(1, int(1 + magnitude * 2.5))
                for d in range(duration):
                    if t + d < years_b:
                        # Gradual recovery
                        depth = magnitude * (1 - d * 0.25)
                        productivity[t + d] = 1 - depth

        # Offset for visibility
        offset = idx * 0.8

        # Plot productivity line
        ax2.plot(time, productivity + offset, color=color, linewidth=2, label=label)

        # Fill below baseline to show depth
        ax2.fill_between(time, offset + 1, productivity + offset,
                        where=(productivity < 1), color=color, alpha=0.4)

        # Draw baseline
        ax2.axhline(1 + offset, color='gray', linestyle='--', alpha=0.5, linewidth=1)

        # Mark the depth with arrows for first shortfall
        min_idx = np.argmin(productivity[:25])
        min_val = productivity[min_idx]
        if idx == 2:  # Only annotate the severe case
            ax2.annotate('', xy=(min_idx, min_val + offset),
                        xytext=(min_idx, 1 + offset),
                        arrowprops=dict(arrowstyle='<->', color='black', lw=1.5))
            ax2.text(min_idx + 2, (min_val + 1)/2 + offset, f'{magnitude:.0%}\ndepth',
                    fontsize=9, va='center')

    ax2.set_xlabel('Year', fontsize=11)
    ax2.set_ylabel('Productivity (offset for clarity)', fontsize=11)
    ax2.set_xlim(0, years_b)
    ax2.set_ylim(0, 3.2)
    ax2.set_title('B. Shortfall Magnitude\n(frequency fixed at 10 yr)', fontsize=12, fontweight='bold')
    ax2.legend(loc='upper right', fontsize=9)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)

    # Add arrow showing "deeper → higher σ"
    ax2.annotate('', xy=(55, 0.2), xytext=(55, 2.8),
                arrowprops=dict(arrowstyle='->', color='black', lw=2))
    ax2.text(57, 1.5, 'Higher σ', rotation=90, va='center', fontsize=9, fontweight='bold')

    # ===============================================
    # Panel C: COMBINED - Heatmap of frequency × magnitude
    # ===============================================

    # Create grid of frequency × magnitude combinations
    freq_vals = [18, 10, 6]  # years between shortfalls (rare to frequent)
    mag_vals = [0.30, 0.45, 0.60]  # proportion reduction (mild to severe)

    # Run simulations and collect σ values
    np.random.seed(42)
    sigma_grid = np.zeros((len(freq_vals), len(mag_vals)))

    for i, interval in enumerate(freq_vals):
        for j, mag in enumerate(mag_vals):
            # Simulate multiple runs and average
            sigmas = []
            for run in range(10):
                # Generate productivity time series
                years_sim = 200
                productivity = np.ones(years_sim) + np.random.normal(0, 0.05, years_sim)

                current = 0
                while current < years_sim:
                    current += int(np.random.exponential(interval))
                    if current < years_sim:
                        # Apply shortfall
                        actual_mag = np.clip(np.random.normal(mag, 0.1), 0.1, 0.9)
                        duration = max(1, int(1 + actual_mag * 2.5))
                        for d in range(duration):
                            if current + d < years_sim:
                                productivity[current + d] -= actual_mag * (1 - d * 0.2)
                        current += duration

                productivity = np.clip(productivity, 0.1, 1.2)
                sigmas.append(np.std(productivity))

            sigma_grid[i, j] = np.mean(sigmas)

    # Create heatmap with more dramatic color range
    im = ax3.imshow(sigma_grid, cmap='RdYlBu_r', aspect='auto',
                    extent=[-0.5, 2.5, -0.5, 2.5], origin='lower',
                    vmin=0.08, vmax=0.35)

    # Add text annotations with σ values
    for i in range(len(freq_vals)):
        for j in range(len(mag_vals)):
            val = sigma_grid[i, j]
            text_color = 'white' if val > 0.22 else 'black'
            ax3.text(j, i, f'σ={val:.2f}', ha='center', va='center',
                    fontsize=11, fontweight='bold', color=text_color)

    # Labels
    ax3.set_xticks([0, 1, 2])
    ax3.set_xticklabels(['Mild\n(30%)', 'Moderate\n(45%)', 'Severe\n(60%)'], fontsize=10)
    ax3.set_yticks([0, 1, 2])
    ax3.set_yticklabels(['Rare\n(18 yr)', 'Moderate\n(10 yr)', 'Frequent\n(6 yr)'], fontsize=10)
    ax3.set_xlabel('Shortfall Magnitude', fontsize=11)
    ax3.set_ylabel('Shortfall Frequency', fontsize=11)
    ax3.set_title('C. Combined Effect\n(frequency × magnitude → σ)', fontsize=12, fontweight='bold')

    # Colorbar
    cbar = plt.colorbar(im, ax=ax3, label='Effective σ', shrink=0.8, pad=0.02)
    cbar.ax.tick_params(labelsize=9)

    # Mark low and high sigma regions
    ax3.text(-0.3, -0.3, 'Low σ\nregion', fontsize=8, ha='center', va='center',
            color='#2166ac', fontweight='bold')
    ax3.text(2.3, 2.3, 'High σ\nregion', fontsize=8, ha='center', va='center',
            color='#b2182b', fontweight='bold')

    plt.tight_layout()

    # Add main title
    fig.suptitle('Environmental Variability: Two Dimensions of Uncertainty',
                fontsize=14, fontweight='bold', y=1.02)

    return fig


def main():
    """Generate the environmental variability figure."""
    print("=" * 60)
    print("Creating Environmental Variability Figure (Revised)")
    print("=" * 60)

    fig = create_environmental_variability_figure()

    # Save outputs
    output_png = OUTPUT_DIR / 'fig_environmental_variability.png'
    output_pdf = OUTPUT_DIR / 'fig_environmental_variability.pdf'

    fig.savefig(output_png, dpi=300, bbox_inches='tight')
    fig.savefig(output_pdf, bbox_inches='tight')

    print(f"\nFigure saved to:")
    print(f"  PNG: {output_png}")
    print(f"  PDF: {output_pdf}")

    plt.close(fig)

    return fig


if __name__ == "__main__":
    main()
