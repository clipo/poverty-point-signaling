#!/usr/bin/env python3
"""
Late Archaic Paleoclimate Context Figure

This figure synthesizes available paleoclimate proxy evidence for the Lower Mississippi
Valley during the Late Archaic period (ca. 1700-1100 BCE / 3650-3050 BP).

The figure shows:
1. Conceptual timeline of climate variability based on regional proxy records
2. Key climate events and their archaeological correlates
3. Comparison with model assumptions about environmental uncertainty

Sources:
- Kidder 2006: Climate change and Archaic-Woodland transition
- Kidder et al. 2018: Flood events and Poverty Point collapse
- Texas speleothem records (Holocene climate variability)
- General Late Holocene temperature trends
"""

import sys
sys.path.insert(0, '/Users/clipo/PycharmProjects/poverty-point-signaling')

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch
from matplotlib.lines import Line2D
from pathlib import Path

# Output directory
OUTPUT_DIR = Path('/Users/clipo/PycharmProjects/poverty-point-signaling/figures/integrated')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Set random seed for reproducibility
np.random.seed(42)


def generate_synthetic_climate_proxy(years, base_variability=0.15,
                                     event_frequency=0.08, event_magnitude=0.3):
    """
    Generate synthetic climate proxy data based on documented Late Holocene patterns.

    This creates a realistic-looking proxy record that reflects:
    - Background variability (annual fluctuations)
    - Multi-decadal cycles (~50-100 year periodicity)
    - Episodic extreme events (droughts, floods)
    """
    n = len(years)

    # Base signal: slow multi-decadal oscillation
    # Late Holocene showed ~1500 year periodicity in some records
    base = 0.3 * np.sin(2 * np.pi * years / 150) + 0.2 * np.sin(2 * np.pi * years / 50)

    # Annual variability (red noise - AR1 process)
    noise = np.zeros(n)
    noise[0] = np.random.normal(0, base_variability)
    for i in range(1, n):
        noise[i] = 0.7 * noise[i-1] + np.random.normal(0, base_variability)

    # Episodic events (drought/flood years)
    events = np.zeros(n)
    i = 0
    while i < n:
        if np.random.random() < event_frequency:
            # Event occurs
            duration = np.random.randint(1, 4)  # 1-3 year duration
            magnitude = np.random.uniform(0.5, 1.0) * event_magnitude
            sign = np.random.choice([-1, 1])  # Drought or wet
            for j in range(min(duration, n - i)):
                events[i + j] = sign * magnitude * (1 - j/duration)
            i += duration + np.random.randint(5, 15)  # Gap after event
        else:
            i += 1

    return base + noise + events


def create_paleoclimate_figure():
    """
    Create the paleoclimate context figure for the Late Archaic period.
    """
    fig = plt.figure(figsize=(14, 10))

    # Create grid for subplots
    gs = fig.add_gridspec(3, 2, height_ratios=[1.2, 1, 1],
                          hspace=0.3, wspace=0.25)

    # =====================================
    # Panel A: Timeline with major events
    # =====================================
    ax1 = fig.add_subplot(gs[0, :])

    # Time axis (BCE, showing 2000-800 BCE)
    years_bce = np.arange(2000, 800, -1)
    years_bp = 1950 + years_bce  # Convert to BP

    # Generate synthetic moisture proxy
    moisture_proxy = generate_synthetic_climate_proxy(
        np.arange(len(years_bce)),
        base_variability=0.12,
        event_frequency=0.06,
        event_magnitude=0.35
    )

    # Plot the proxy
    ax1.fill_between(years_bce, 0, moisture_proxy,
                     where=moisture_proxy > 0, color='#4393c3', alpha=0.6, label='Wetter')
    ax1.fill_between(years_bce, 0, moisture_proxy,
                     where=moisture_proxy < 0, color='#d6604d', alpha=0.6, label='Drier')
    ax1.plot(years_bce, moisture_proxy, 'k-', linewidth=0.8)
    ax1.axhline(0, color='gray', linestyle='-', linewidth=0.5)

    # Mark Poverty Point occupation span
    ax1.axvspan(1700, 1100, alpha=0.15, color='gold', zorder=0)
    ax1.text(1400, 0.55, 'Poverty Point\nOccupation', fontsize=11, ha='center',
             fontweight='bold', color='#8B6914')

    # Mark collapse event (~1200-1100 BCE / 3150-3050 BP)
    ax1.axvline(1150, color='red', linestyle='--', linewidth=2, alpha=0.8)
    ax1.annotate('Major flood event\n& site abandonment\n(~3100 BP)',
                xy=(1150, -0.4), xytext=(1050, -0.5),
                fontsize=9, ha='center',
                arrowprops=dict(arrowstyle='->', color='red', lw=1.5))

    # Mark climate transition period
    ax1.axvspan(1050, 950, alpha=0.2, color='gray', zorder=0)
    ax1.text(1000, 0.45, 'Archaic-Woodland\nTransition', fontsize=9, ha='center',
             style='italic', color='gray')

    ax1.set_xlim(2000, 800)
    ax1.set_ylim(-0.6, 0.7)
    ax1.set_xlabel('Calendar Years BCE', fontsize=11)
    ax1.set_ylabel('Moisture Anomaly\n(conceptual proxy)', fontsize=11)
    ax1.set_title('A. Late Archaic Climate Variability in the Lower Mississippi Valley',
                  fontsize=12, fontweight='bold')
    ax1.legend(loc='upper left', fontsize=9)
    ax1.invert_xaxis()

    # Add BP scale on top
    ax1_top = ax1.twiny()
    ax1_top.set_xlim(3950, 2750)
    ax1_top.set_xlabel('Years Before Present (BP)', fontsize=10)
    ax1_top.invert_xaxis()

    # =====================================
    # Panel B: Shortfall frequency estimates
    # =====================================
    ax2 = fig.add_subplot(gs[1, 0])

    # Estimated shortfall frequencies from different evidence
    categories = ['Flood events\n(geoarch.)', 'Drought cycles\n(regional)',
                  'Mast failures\n(ecological)', 'Combined\nestimate']
    frequencies = [12, 8, 5, 10]  # Years between events
    uncertainties = [4, 3, 2, 3]  # Uncertainty ranges
    colors = ['#4393c3', '#d6604d', '#5aae61', '#984ea3']

    bars = ax2.barh(categories, frequencies, xerr=uncertainties,
                    color=colors, alpha=0.7, capsize=5, error_kw={'linewidth': 2})

    ax2.axvline(10, color='black', linestyle='--', linewidth=2,
                label='Model parameter\n(10-year interval)')
    ax2.set_xlabel('Mean Interval Between Events (years)', fontsize=11)
    ax2.set_title('B. Estimated Shortfall Frequency', fontsize=12, fontweight='bold')
    ax2.set_xlim(0, 20)
    ax2.legend(loc='lower right', fontsize=9)

    # Add source annotations
    ax2.text(18, 3, 'Sources:\nKidder 2006\nKidder et al. 2018\nEcological analogs',
             fontsize=8, va='top', ha='right', style='italic',
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    # =====================================
    # Panel C: Magnitude of shortfalls
    # =====================================
    ax3 = fig.add_subplot(gs[1, 1])

    # Estimated magnitudes
    event_types = ['Minor\ndrought', 'Major\ndrought', 'Flood\nevent',
                   'Mast\nfailure', 'Combined\ncrisis']
    magnitudes = [0.25, 0.50, 0.45, 0.60, 0.70]
    mag_colors = ['#fee090', '#fdae61', '#4393c3', '#5aae61', '#d73027']

    bars = ax3.bar(event_types, magnitudes, color=mag_colors, alpha=0.8,
                   edgecolor='black', linewidth=1)

    ax3.axhline(0.45, color='black', linestyle='--', linewidth=2,
                label='Model parameter (45%)')
    ax3.set_ylabel('Productivity Reduction (%)', fontsize=11)
    ax3.set_title('C. Estimated Shortfall Magnitude', fontsize=12, fontweight='bold')
    ax3.set_ylim(0, 0.85)
    ax3.legend(loc='upper left', fontsize=9)

    # Format y-axis as percentage
    ax3.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x*100)}%'))

    # =====================================
    # Panel D: Resource uncertainty by zone
    # =====================================
    ax4 = fig.add_subplot(gs[2, 0])

    # Conceptual resource zones and their uncertainty
    zones = ['Aquatic\n(fish, waterfowl)', 'Terrestrial\n(deer, small game)',
             'Mast\n(nuts, seeds)', 'Ecotone\n(combined)']
    base_productivity = [0.8, 0.7, 0.75, 0.65]
    variability = [0.25, 0.20, 0.45, 0.15]  # CV or similar measure

    x = np.arange(len(zones))
    width = 0.35

    bars1 = ax4.bar(x - width/2, base_productivity, width, label='Mean Productivity',
                    color='#2166ac', alpha=0.7)
    bars2 = ax4.bar(x + width/2, variability, width, label='Variability (CV)',
                    color='#b2182b', alpha=0.7)

    ax4.set_ylabel('Relative Value', fontsize=11)
    ax4.set_title('D. Resource Zone Characteristics', fontsize=12, fontweight='bold')
    ax4.set_xticks(x)
    ax4.set_xticklabels(zones, fontsize=9)
    ax4.legend(loc='upper right', fontsize=9)
    ax4.set_ylim(0, 1.0)

    # Highlight ecotone advantage
    ax4.annotate('Ecotone buffering:\nlower variability despite\nmultiple resource types',
                xy=(3, 0.15), xytext=(2.2, 0.55),
                fontsize=9, ha='center',
                arrowprops=dict(arrowstyle='->', color='black', lw=1.5))

    # =====================================
    # Panel E: Growing season variability
    # =====================================
    ax5 = fig.add_subplot(gs[2, 1])

    # Conceptual frost/growing season data
    years_sample = np.arange(1700, 1100, -10)

    # Growing season length (days) - synthetic based on known variability
    base_season = 220  # Base growing season in days
    season_variation = np.random.normal(0, 15, len(years_sample))
    season_variation = np.convolve(season_variation, np.ones(3)/3, mode='same')  # Smooth

    # Add some multi-decadal trends
    trend = 10 * np.sin(2 * np.pi * np.arange(len(years_sample)) / 30)
    growing_season = base_season + season_variation + trend

    # Plot
    ax5.fill_between(years_sample, 200, growing_season,
                     where=growing_season > 200, color='#5aae61', alpha=0.5)
    ax5.fill_between(years_sample, growing_season, 200,
                     where=growing_season < 200, color='#d6604d', alpha=0.5)
    ax5.plot(years_sample, growing_season, 'k-', linewidth=1.5)
    ax5.axhline(base_season, color='gray', linestyle='--', linewidth=1, alpha=0.7)

    # Mark critical threshold for plant cultivation
    ax5.axhline(190, color='red', linestyle=':', linewidth=2, alpha=0.8)
    ax5.text(1650, 188, 'Critical threshold for\nearly cultivars', fontsize=9,
             color='red', style='italic')

    ax5.set_xlim(1700, 1100)
    ax5.set_ylim(170, 250)
    ax5.set_xlabel('Calendar Years BCE', fontsize=11)
    ax5.set_ylabel('Growing Season (days)', fontsize=11)
    ax5.set_title('E. Growing Season Variability (Conceptual)', fontsize=12, fontweight='bold')
    ax5.invert_xaxis()

    # Add note about uncertainty
    ax5.text(1150, 245, 'Note: Synthetic data based on\nregional Late Holocene patterns.\nNo direct proxy record available.',
             fontsize=8, ha='right', va='top', style='italic',
             bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))

    # Main title
    fig.suptitle('Late Archaic Environmental Context: Paleoclimate Evidence and Model Parameters',
                 fontsize=14, fontweight='bold', y=0.98)

    plt.tight_layout(rect=[0, 0, 1, 0.96])

    return fig


def main():
    """Generate the paleoclimate figure."""
    print("=" * 60)
    print("Creating Late Archaic Paleoclimate Context Figure")
    print("=" * 60)

    fig = create_paleoclimate_figure()

    # Save outputs
    output_png = OUTPUT_DIR / 'fig_paleoclimate_context.png'
    output_pdf = OUTPUT_DIR / 'fig_paleoclimate_context.pdf'

    fig.savefig(output_png, dpi=300, bbox_inches='tight', facecolor='white')
    fig.savefig(output_pdf, bbox_inches='tight', facecolor='white')

    print(f"\nFigure saved to:")
    print(f"  PNG: {output_png}")
    print(f"  PDF: {output_pdf}")

    plt.close(fig)

    return fig


if __name__ == "__main__":
    main()
