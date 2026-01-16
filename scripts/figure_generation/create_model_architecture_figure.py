#!/usr/bin/env python3
"""
Create Model Architecture Figure for Poverty Point ABM Manuscript.

This script generates a 6-panel figure summarizing the agent-based model:
- Panel A: Environment Module (4 resource zones, ecotone advantage)
- Panel B: Agents Module (two strategies, band attributes)
- Panel C: Annual Cycle (4-phase flowchart, spanning both columns)
- Panel D: Fitness Functions (W_agg vs W_ind, critical threshold)
- Panel E: Model Outputs and Predictions

Output: figures/final/Figure_5_model_architecture.png
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Wedge
from matplotlib.gridspec import GridSpec
import numpy as np
import os

# Project paths
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'figures', 'final')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Colorblind-safe palette
CB_COLORS = {
    'blue': '#0173B2',       # Aggregators
    'red': '#D55E00',        # Independents
    'green': '#029E73',      # Resources/positive
    'orange': '#DE8F05',     # Costs/stress
    'purple': '#CC78BC',     # Neutral/balance
    'yellow': '#ECE133',     # Highlights
    'gray': '#949494',       # Arrows/neutral
    'black': '#000000',
    'light_gray': '#E5E5E5',
}

ZONE_COLORS = {
    'aquatic': '#a6cee3',
    'terrestrial': '#b15928',
    'mast': '#33a02c',
    'ecotone': '#ffff99',
}

# Font settings (Times New Roman equivalent)
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif', 'serif']
plt.rcParams['font.size'] = 11
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.labelsize'] = 11


def add_fancy_box(ax, x, y, width, height, text, facecolor='white',
                  edgecolor='black', fontsize=10, text_va='center',
                  boxstyle='round,pad=0.02', alpha=0.9, linewidth=1.5):
    """Add a fancy box with text to an axes."""
    box = FancyBboxPatch((x, y), width, height,
                         boxstyle=boxstyle,
                         facecolor=facecolor,
                         edgecolor=edgecolor,
                         alpha=alpha,
                         linewidth=linewidth,
                         transform=ax.transAxes)
    ax.add_patch(box)

    # Add text
    if text:
        ax.text(x + width/2, y + height/2, text,
                ha='center', va=text_va,
                fontsize=fontsize,
                transform=ax.transAxes,
                wrap=True)


def draw_panel_a_environment(ax):
    """Panel A: Environment Module - 4 resource zones with ecotone advantage."""
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    ax.set_title('A. Environment Module', fontweight='bold', fontsize=12, loc='left')

    # Draw stylized landscape cross-section
    # Aquatic zone (left)
    aquatic = FancyBboxPatch((0.02, 0.55), 0.22, 0.35,
                              boxstyle='round,pad=0.01',
                              facecolor=ZONE_COLORS['aquatic'],
                              edgecolor='black', alpha=0.8, linewidth=1)
    ax.add_patch(aquatic)
    ax.text(0.13, 0.72, 'AQUATIC', ha='center', va='center', fontsize=9, fontweight='bold')
    ax.text(0.13, 0.62, 'Fish, waterfowl\nPeak: Summer', ha='center', va='center', fontsize=7)

    # Mast zone (center-left)
    mast = FancyBboxPatch((0.26, 0.55), 0.22, 0.35,
                           boxstyle='round,pad=0.01',
                           facecolor=ZONE_COLORS['mast'],
                           edgecolor='black', alpha=0.8, linewidth=1)
    ax.add_patch(mast)
    ax.text(0.37, 0.72, 'MAST', ha='center', va='center', fontsize=9, fontweight='bold')
    ax.text(0.37, 0.62, 'Nuts, acorns\nPeak: Fall', ha='center', va='center', fontsize=7)

    # Terrestrial zone (center-right)
    terr = FancyBboxPatch((0.50, 0.55), 0.22, 0.35,
                           boxstyle='round,pad=0.01',
                           facecolor=ZONE_COLORS['terrestrial'],
                           edgecolor='black', alpha=0.8, linewidth=1)
    ax.add_patch(terr)
    ax.text(0.61, 0.72, 'TERRESTRIAL', ha='center', va='center', fontsize=9, fontweight='bold')
    ax.text(0.61, 0.62, 'Deer, game\nPeak: Winter', ha='center', va='center', fontsize=7)

    # Ecotone zone (right, highlighted)
    ecotone = FancyBboxPatch((0.74, 0.55), 0.24, 0.35,
                              boxstyle='round,pad=0.01',
                              facecolor=ZONE_COLORS['ecotone'],
                              edgecolor=CB_COLORS['orange'], alpha=0.9, linewidth=2.5)
    ax.add_patch(ecotone)
    ax.text(0.86, 0.75, 'ECOTONE', ha='center', va='center', fontsize=9, fontweight='bold')
    ax.text(0.86, 0.65, 'Multi-zone\naccess', ha='center', va='center', fontsize=7)
    ax.text(0.86, 0.57, '(Poverty Point)', ha='center', va='center', fontsize=7,
            fontstyle='italic', color=CB_COLORS['orange'])

    # Parameter box
    param_box = FancyBboxPatch((0.02, 0.08), 0.55, 0.38,
                                boxstyle='round,pad=0.02',
                                facecolor=CB_COLORS['light_gray'],
                                edgecolor='black', alpha=0.7, linewidth=1)
    ax.add_patch(param_box)
    ax.text(0.05, 0.40, 'Key Parameters:', fontsize=9, fontweight='bold')
    ax.text(0.05, 0.32, r'$\sigma$ = Environmental uncertainty (0-1)', fontsize=8)
    ax.text(0.05, 0.24, r'$\varepsilon$ = Ecotone advantage (0-0.5)', fontsize=8)
    ax.text(0.05, 0.16, 'Zone covariance: Negative = buffering', fontsize=8)

    # Equation box
    eq_box = FancyBboxPatch((0.60, 0.08), 0.38, 0.38,
                             boxstyle='round,pad=0.02',
                             facecolor='white',
                             edgecolor=CB_COLORS['orange'], alpha=0.9, linewidth=1.5)
    ax.add_patch(eq_box)
    ax.text(0.79, 0.38, 'Ecotone Effect:', fontsize=9, fontweight='bold', ha='center')
    ax.text(0.79, 0.26, r'$\sigma_{eff} = \sigma(1-\varepsilon)$', fontsize=11, ha='center')
    ax.text(0.79, 0.14, 'Reduces effective\nuncertainty', fontsize=8, ha='center')


def draw_panel_b_agents(ax):
    """Panel B: Agents Module - Two strategies and band attributes."""
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    ax.set_title('B. Agent Module', fontweight='bold', fontsize=12, loc='left')

    # AGGREGATOR box (left)
    agg_box = FancyBboxPatch((0.02, 0.45), 0.45, 0.50,
                              boxstyle='round,pad=0.02',
                              facecolor=CB_COLORS['blue'],
                              edgecolor='black', alpha=0.3, linewidth=1.5)
    ax.add_patch(agg_box)
    ax.text(0.245, 0.90, 'AGGREGATOR', ha='center', va='center',
            fontsize=10, fontweight='bold', color=CB_COLORS['blue'])

    # Aggregator attributes
    agg_text = [
        'Travels to central site',
        'Invests in monuments',
        'Acquires exotic goods',
        'Forms obligations',
    ]
    for i, txt in enumerate(agg_text):
        ax.text(0.05, 0.80 - i*0.09, f'• {txt}', fontsize=8, va='center')

    ax.text(0.245, 0.48, r'Cost: $C_{total} = 0.42$', ha='center', fontsize=8,
            color=CB_COLORS['blue'], fontstyle='italic')

    # INDEPENDENT box (right)
    ind_box = FancyBboxPatch((0.53, 0.45), 0.45, 0.50,
                              boxstyle='round,pad=0.02',
                              facecolor=CB_COLORS['red'],
                              edgecolor='black', alpha=0.3, linewidth=1.5)
    ax.add_patch(ind_box)
    ax.text(0.755, 0.90, 'INDEPENDENT', ha='center', va='center',
            fontsize=10, fontweight='bold', color=CB_COLORS['red'])

    # Independent attributes
    ind_text = [
        'Remains in home territory',
        'Full foraging time',
        'No aggregation costs',
        'Higher shortfall vulnerability',
    ]
    for i, txt in enumerate(ind_text):
        ax.text(0.56, 0.80 - i*0.09, f'• {txt}', fontsize=8, va='center')

    ax.text(0.755, 0.48, r'Advantage: $R_{ind} = 1.10$', ha='center', fontsize=8,
            color=CB_COLORS['red'], fontstyle='italic')

    # Band attributes box (bottom)
    attr_box = FancyBboxPatch((0.02, 0.02), 0.96, 0.38,
                               boxstyle='round,pad=0.02',
                               facecolor=CB_COLORS['light_gray'],
                               edgecolor='black', alpha=0.7, linewidth=1)
    ax.add_patch(attr_box)
    ax.text(0.50, 0.35, 'Band Attributes', ha='center', fontsize=9, fontweight='bold')

    # Two columns of attributes
    left_attrs = ['size: Population (10-50)', 'resources: Holdings [0,1]']
    right_attrs = ['prestige: Status level', 'obligations: Social network']

    for i, txt in enumerate(left_attrs):
        ax.text(0.08, 0.25 - i*0.10, f'• {txt}', fontsize=8)
    for i, txt in enumerate(right_attrs):
        ax.text(0.52, 0.25 - i*0.10, f'• {txt}', fontsize=8)


def draw_panel_c_annual_cycle(ax):
    """Panel C: Annual Cycle - 4-phase circular flowchart."""
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    ax.set_title('C. Annual Cycle', fontweight='bold', fontsize=12, loc='left')

    # Center point
    cx, cy = 0.5, 0.50
    radius = 0.32

    # Season positions (top, right, bottom, left)
    positions = {
        'spring': (cx, cy + radius),
        'summer': (cx + radius * 1.1, cy),
        'fall': (cx, cy - radius),
        'winter': (cx - radius * 1.1, cy),
    }

    # Season colors
    colors = {
        'spring': CB_COLORS['green'],
        'summer': CB_COLORS['orange'],
        'fall': ZONE_COLORS['terrestrial'],
        'winter': CB_COLORS['blue'],
    }

    # Season content
    content = {
        'spring': ('SPRING', ['Dispersal season', 'Independent foraging', 'Shortfall check']),
        'summer': ('SUMMER', ['Strategy decision', 'Travel to site', 'Monument invest', 'Exotic acquisition']),
        'fall': ('FALL', ['Harvest season', 'Shortfall impacts', 'Obligation calls']),
        'winter': ('WINTER', ['Reproduction', 'Mortality', 'Band dynamics']),
    }

    box_width = 0.22
    box_height = 0.28

    # Draw season boxes
    for season, (x, y) in positions.items():
        box = FancyBboxPatch((x - box_width/2, y - box_height/2),
                              box_width, box_height,
                              boxstyle='round,pad=0.02',
                              facecolor=colors[season],
                              edgecolor='black', alpha=0.4, linewidth=1.5)
        ax.add_patch(box)

        title, items = content[season]
        ax.text(x, y + box_height/2 - 0.04, title, ha='center', va='center',
                fontsize=9, fontweight='bold')

        for i, item in enumerate(items):
            ax.text(x, y + box_height/2 - 0.08 - i*0.055, f'• {item}',
                    ha='center', va='center', fontsize=7)

    # Draw curved arrows between seasons
    arrow_props = dict(arrowstyle='->', color=CB_COLORS['gray'],
                       lw=2, connectionstyle='arc3,rad=0.3')

    # Spring -> Summer
    ax.annotate('', xy=(positions['summer'][0] - 0.12, positions['summer'][1] + 0.10),
                xytext=(positions['spring'][0] + 0.10, positions['spring'][1] - 0.10),
                arrowprops=arrow_props)

    # Summer -> Fall
    ax.annotate('', xy=(positions['fall'][0] + 0.10, positions['fall'][1] + 0.10),
                xytext=(positions['summer'][0] - 0.08, positions['summer'][1] - 0.12),
                arrowprops=arrow_props)

    # Fall -> Winter
    ax.annotate('', xy=(positions['winter'][0] + 0.12, positions['winter'][1] - 0.10),
                xytext=(positions['fall'][0] - 0.10, positions['fall'][1] + 0.10),
                arrowprops=arrow_props)

    # Winter -> Spring
    ax.annotate('', xy=(positions['spring'][0] - 0.10, positions['spring'][1] - 0.10),
                xytext=(positions['winter'][0] + 0.08, positions['winter'][1] + 0.12),
                arrowprops=arrow_props)

    # Center label
    center_box = FancyBboxPatch((cx - 0.10, cy - 0.06), 0.20, 0.12,
                                 boxstyle='round,pad=0.01',
                                 facecolor='white',
                                 edgecolor=CB_COLORS['gray'], alpha=0.9, linewidth=1)
    ax.add_patch(center_box)
    ax.text(cx, cy + 0.02, '500 years', ha='center', va='center', fontsize=9, fontweight='bold')
    ax.text(cx, cy - 0.04, '(1700-1100 BCE)', ha='center', va='center', fontsize=7)


def draw_panel_d_fitness(ax):
    """Panel D: Fitness Functions - W_agg vs W_ind with critical threshold."""
    ax.set_title('D. Fitness Functions', fontweight='bold', fontsize=12, loc='left')

    # Generate fitness curves
    sigma = np.linspace(0, 0.8, 100)

    # Parameters
    C_total = 0.42
    alpha = 0.40
    beta = 0.75
    epsilon = 0.35
    R_ind = 1.10
    f_n = 1.26  # cooperation benefits at n=25
    B_recip = 0.05

    # Fitness functions
    sigma_eff = sigma * (1 - epsilon)
    W_agg = (1 - C_total) * (1 - alpha * sigma_eff) * f_n * (1 + B_recip)
    W_ind = R_ind * (1 - beta * sigma)

    # Find critical threshold
    diff = W_agg - W_ind
    idx = np.argmin(np.abs(diff))
    sigma_star = sigma[idx]

    # Plot
    ax.plot(sigma, W_agg, color=CB_COLORS['blue'], linewidth=2.5, label='Aggregator')
    ax.plot(sigma, W_ind, color=CB_COLORS['red'], linewidth=2.5, label='Independent')

    # Critical threshold
    ax.axvline(x=sigma_star, color=CB_COLORS['gray'], linestyle='--', linewidth=1.5)
    ax.text(sigma_star + 0.02, 0.95, r'$\sigma^* \approx 0.53$', fontsize=9,
            transform=ax.get_xaxis_transform())

    # Shaded regions
    ax.fill_between(sigma[:idx], 0.4, 1.1, alpha=0.1, color=CB_COLORS['red'])
    ax.fill_between(sigma[idx:], 0.4, 1.1, alpha=0.1, color=CB_COLORS['blue'])

    # Region labels
    ax.text(0.15, 0.50, 'Independent\nfavored', ha='center', fontsize=8,
            color=CB_COLORS['red'])
    ax.text(0.70, 0.50, 'Aggregation\nfavored', ha='center', fontsize=8,
            color=CB_COLORS['blue'])

    ax.set_xlabel(r'Environmental Uncertainty ($\sigma$)', fontsize=10)
    ax.set_ylabel('Expected Fitness (W)', fontsize=10)
    ax.set_xlim(0, 0.8)
    ax.set_ylim(0.4, 1.1)
    ax.legend(loc='upper right', fontsize=8)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)


def draw_panel_e_outputs(ax):
    """Panel E: Model Outputs and Predictions."""
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    ax.set_title('E. Model Outputs & Predictions', fontweight='bold', fontsize=12, loc='left')

    # Outputs box (top)
    out_box = FancyBboxPatch((0.02, 0.55), 0.96, 0.42,
                              boxstyle='round,pad=0.02',
                              facecolor=CB_COLORS['light_gray'],
                              edgecolor='black', alpha=0.7, linewidth=1)
    ax.add_patch(out_box)
    ax.text(0.50, 0.92, 'Model Outputs', ha='center', fontsize=10, fontweight='bold')

    outputs = [
        'Strategy dominance: (n_agg - n_ind) / n_total',
        'Monument accumulation: Cumulative investment',
        'Exotic goods: Total across bands',
        'Population dynamics: Size over time',
    ]
    for i, txt in enumerate(outputs):
        ax.text(0.06, 0.82 - i*0.08, f'• {txt}', fontsize=8)

    # Predictions box (bottom)
    pred_box = FancyBboxPatch((0.02, 0.02), 0.96, 0.48,
                               boxstyle='round,pad=0.02',
                               facecolor=ZONE_COLORS['ecotone'],
                               edgecolor=CB_COLORS['orange'], alpha=0.5, linewidth=1.5)
    ax.add_patch(pred_box)
    ax.text(0.50, 0.46, 'Key Predictions', ha='center', fontsize=10, fontweight='bold')

    predictions = [
        r'P1: Aggregation emerges when $\sigma > \sigma^*$',
        r'P2: Monument investment $\propto$ to $\sigma$',
        r'P3: Site primacy at maximum ecotone ($\varepsilon$)',
        r'P4: System collapse when $\sigma$ drops below $\sigma^*$',
    ]
    for i, txt in enumerate(predictions):
        ax.text(0.06, 0.38 - i*0.09, txt, fontsize=8)


def create_figure():
    """Create the complete 5-panel model architecture figure."""
    # Create figure with GridSpec layout
    fig = plt.figure(figsize=(14, 12))
    gs = GridSpec(3, 2, figure=fig, height_ratios=[1, 0.9, 1],
                  hspace=0.35, wspace=0.25,
                  left=0.05, right=0.95, top=0.95, bottom=0.05)

    # Panel A: Environment (top left)
    ax_a = fig.add_subplot(gs[0, 0])
    draw_panel_a_environment(ax_a)

    # Panel B: Agents (top right)
    ax_b = fig.add_subplot(gs[0, 1])
    draw_panel_b_agents(ax_b)

    # Panel C: Annual Cycle (middle, spanning both columns)
    ax_c = fig.add_subplot(gs[1, :])
    draw_panel_c_annual_cycle(ax_c)

    # Panel D: Fitness Functions (bottom left)
    ax_d = fig.add_subplot(gs[2, 0])
    draw_panel_d_fitness(ax_d)

    # Panel E: Outputs (bottom right)
    ax_e = fig.add_subplot(gs[2, 1])
    draw_panel_e_outputs(ax_e)

    return fig


def main():
    """Generate and save the model architecture figure."""
    print("Creating model architecture figure...")

    fig = create_figure()

    # Save outputs
    png_path = os.path.join(OUTPUT_DIR, 'Figure_5_model_architecture.png')
    pdf_path = os.path.join(OUTPUT_DIR, 'Figure_5_model_architecture.pdf')

    fig.savefig(png_path, dpi=300, bbox_inches='tight', facecolor='white')
    fig.savefig(pdf_path, bbox_inches='tight', facecolor='white')

    print(f"Saved: {png_path}")
    print(f"Saved: {pdf_path}")

    plt.close(fig)
    print("Done!")


if __name__ == '__main__':
    main()
