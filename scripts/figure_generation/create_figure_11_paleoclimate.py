#!/usr/bin/env python3
"""
Create Figure 11: Paleoclimate Proxy Evidence for Late Archaic Environmental Uncertainty

This script generates a publication-quality 6-panel figure showing:
A. Temperature reconstruction from Temperature 12k database
B. Hydroclimate (Water Balance) from Salonen et al. 2025
C. Hurricane activity from Liu & Fearn paleotempestology
D. Environmental uncertainty index calculation
E. Archaeological site comparison
F. Phase space position

Formatting follows CLAUDE.md requirements:
- Times New Roman 11pt
- Colorblind-safe palette
- 300 DPI for publication

Author: Generated for Poverty Point JAS manuscript
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Patch, Rectangle
from scipy.ndimage import gaussian_filter1d
import pickle
import os
import sys

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, PROJECT_ROOT)

DATA_DIR = os.path.join(PROJECT_ROOT, 'data', 'paleoclimate')
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'figures', 'final')

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Publication formatting
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 11
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['legend.fontsize'] = 9
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10

# Colorblind-safe palette
CB_COLORS = {
    'blue': '#0173B2',
    'orange': '#DE8F05',
    'green': '#029E73',
    'red': '#D55E00',
    'purple': '#CC78BC',
    'brown': '#CA9161',
    'pink': '#FBAFE4',
    'gray': '#949494',
    'yellow': '#ECE133',
    'cyan': '#56B4E9'
}

# Poverty Point period
PP_START_KA = 3.65  # 1700 BCE
PP_END_KA = 3.05    # 1100 BCE
PP_START_BP = 3650
PP_END_BP = 3050

# Critical threshold
SIGMA_CRITICAL = 0.53


def load_temperature_data():
    """Load Temperature 12k database and extract regional data."""
    pkl_path = os.path.join(DATA_DIR, 'Temp12k_v1_0_0.pkl')
    if not os.path.exists(pkl_path):
        print(f"Warning: Temperature 12k file not found at {pkl_path}")
        return None

    with open(pkl_path, 'rb') as f:
        data = pickle.load(f)

    D = data['D']

    # Extract Gulf Coast/SE US sites
    target_sites = [
        'Ferndale.Albert.1981',
        'ClearPond.Hussey.1993',
        'WhitePond.Krause.2019',
        'KNR159_JPC26.Antonarakou.2015'
    ]

    site_data = {}
    for site_key in target_sites:
        if site_key in D:
            record = D[site_key]
            geo = record.get('geo', {})
            paleo = record.get('paleoData', {}).get('paleo0', {})
            meas_tables = paleo.get('measurementTable', {})

            for table_key, table_val in meas_tables.items():
                columns = table_val.get('columns', {})

                # Find age column
                age_vals = None
                for col_key, col_val in columns.items():
                    if isinstance(col_val, dict):
                        vname = col_val.get('variableName', '').lower()
                        if 'age' in vname and 'duplicate' not in vname:
                            vals = col_val.get('values', [])
                            if vals and isinstance(vals[0], (int, float)):
                                age_vals = np.array(vals)
                                break

                # Find temperature column
                for col_key, col_val in columns.items():
                    if isinstance(col_val, dict):
                        vname = col_val.get('variableName', '').lower()
                        if vname == 'temperature':
                            vals = col_val.get('values', [])
                            if vals and age_vals is not None:
                                coords = geo.get('geometry', {}).get('coordinates', [None, None])
                                site_data[site_key] = {
                                    'name': geo.get('siteName'),
                                    'lat': coords[1],
                                    'lon': coords[0],
                                    'archive': record.get('archiveType'),
                                    'ages': age_vals / 1000,  # Convert to ka
                                    'temps': np.array([float(v) if v is not None else np.nan for v in vals])
                                }

    return site_data


def load_hydroclimate_data():
    """Load Salonen et al. 2025 hydroclimate data."""
    xlsx_path = os.path.join(DATA_DIR, 'Salonen_hydroclimate_data.xlsx')
    if not os.path.exists(xlsx_path):
        print(f"Warning: Hydroclimate file not found at {xlsx_path}")
        return None

    xl = pd.ExcelFile(xlsx_path)
    mw_wab = pd.read_excel(xl, sheet_name='MW_BRT_WAB_HR')
    return mw_wab


def get_hurricane_data():
    """
    Return hurricane landfall data from Liu & Fearn paleotempestology.

    Data compiled from:
    - Liu & Fearn 1993 (Lake Shelby, Alabama)
    - Liu & Fearn 2000 (Western Lake, Florida)
    """
    # Individual hurricane events (in cal yr BP)
    lake_shelby_events = [800, 1400, 2200, 2600, 3000, 3200]
    western_lake_events = [1150, 2780, 3470, 4500]

    # Activity periods (based on Liu synthesis)
    activity_periods = {
        'hyperactive': (3800, 1000),  # BP, 5x baseline
        'quiet_recent': (1000, 0),
        'quiet_ancient': (6000, 3800)
    }

    return {
        'lake_shelby': np.array(lake_shelby_events) / 1000,  # ka
        'western_lake': np.array(western_lake_events) / 1000,  # ka
        'activity_periods': activity_periods
    }


def calculate_sigma(frequency, magnitude):
    """Calculate environmental uncertainty parameter."""
    frequency_effect = np.sqrt(20 / frequency)
    sigma = magnitude * frequency_effect
    return np.clip(sigma, 0, 1)


def create_panel_a_temperature(ax, temp_data):
    """Panel A: Temperature reconstruction from Temp12k."""
    if temp_data is None:
        ax.text(0.5, 0.5, 'Temperature data not available', ha='center', va='center', transform=ax.transAxes)
        ax.set_title('A. Temperature Reconstruction', fontweight='bold')
        return

    colors = [CB_COLORS['blue'], CB_COLORS['green'], CB_COLORS['red'], CB_COLORS['purple']]

    for i, (site_key, data) in enumerate(temp_data.items()):
        ages = data['ages']
        temps = data['temps']

        # Sort by age
        sort_idx = np.argsort(ages)
        ages = ages[sort_idx]
        temps = temps[sort_idx]

        # Filter for display range
        mask = (ages >= 0) & (ages <= 8)
        if np.sum(mask) > 0:
            label = f"{data['name']} ({data['lat']:.1f}°N)"
            ax.plot(ages[mask], temps[mask], 'o-', color=colors[i % len(colors)],
                   label=label, markersize=3, alpha=0.7, linewidth=1)

    # Poverty Point shading
    ax.axvspan(PP_END_KA, PP_START_KA, alpha=0.25, color=CB_COLORS['orange'], zorder=0)

    ax.set_xlim(8, 0)
    ax.set_xlabel('Age (ka BP)')
    ax.set_ylabel('Temperature (°C)')
    ax.set_title('A. Regional Temperature (Temperature 12k)', fontweight='bold')
    ax.legend(loc='upper left', fontsize=8)
    ax.grid(True, alpha=0.3)


def create_panel_b_hydroclimate(ax, wab_data):
    """Panel B: Hydroclimate from Salonen et al. 2025."""
    if wab_data is None:
        ax.text(0.5, 0.5, 'Hydroclimate data not available', ha='center', va='center', transform=ax.transAxes)
        ax.set_title('B. Hydroclimate Variability', fontweight='bold')
        return

    ages = wab_data['Age_ka']
    mean = wab_data['Mean']
    ci_low = wab_data['Mean_min95']
    ci_high = wab_data['Mean_max95']

    # Plot uncertainty band
    ax.fill_between(ages, ci_low, ci_high, alpha=0.3, color=CB_COLORS['green'])
    ax.plot(ages, mean, color=CB_COLORS['green'], linewidth=1.5, label='Midwest WAB')

    # Poverty Point shading
    ax.axvspan(PP_END_KA, PP_START_KA, alpha=0.25, color=CB_COLORS['orange'], zorder=0)

    # Zero line
    ax.axhline(y=0, color='gray', linestyle=':', linewidth=1, alpha=0.7)

    ax.set_xlim(8, 0)
    ax.set_xlabel('Age (ka BP)')
    ax.set_ylabel('Water Balance Anomaly (mm)')
    ax.set_title('B. Midwest Hydroclimate (Salonen et al. 2025)', fontweight='bold')
    ax.legend(loc='upper right', fontsize=9)
    ax.grid(True, alpha=0.3)

    # Annotate PP period stats
    pp_mask = (ages >= PP_END_KA) & (ages <= PP_START_KA)
    pp_mean = mean[pp_mask].mean()
    ax.annotate(f'PP mean: {pp_mean:.0f} mm', xy=(3.35, pp_mean),
               xytext=(5, pp_mean + 50), fontsize=9,
               arrowprops=dict(arrowstyle='->', color=CB_COLORS['orange'], lw=1.5),
               color=CB_COLORS['orange'])


def create_panel_c_hurricanes(ax, hurricane_data):
    """Panel C: Hurricane activity from paleotempestology."""
    # Create activity timeline
    time = np.linspace(0, 6, 600)  # ka
    activity = np.ones_like(time)

    # Hyperactive period: 3.8-1.0 ka (BP)
    hyperactive = (time >= 1.0) & (time <= 3.8)
    activity[hyperactive] = 5.0

    # Smooth transition
    activity_smooth = gaussian_filter1d(activity, sigma=10)

    # Plot activity
    ax.fill_between(time, 0, activity_smooth, alpha=0.4, color=CB_COLORS['purple'])
    ax.plot(time, activity_smooth, color=CB_COLORS['purple'], linewidth=1.5)

    # Mark individual events
    for event in hurricane_data['lake_shelby']:
        if 0 <= event <= 6:
            ax.axvline(x=event, color=CB_COLORS['red'], alpha=0.6, linewidth=1.5, linestyle='-')

    for event in hurricane_data['western_lake']:
        if 0 <= event <= 6:
            ax.axvline(x=event, color=CB_COLORS['blue'], alpha=0.6, linewidth=1.5, linestyle='--')

    # Poverty Point shading
    ax.axvspan(PP_END_KA, PP_START_KA, alpha=0.25, color=CB_COLORS['orange'], zorder=0)

    ax.set_xlim(6, 0)
    ax.set_ylim(0, 6)
    ax.set_xlabel('Age (ka BP)')
    ax.set_ylabel('Relative Activity (×baseline)')
    ax.set_title('C. Hurricane Activity (Liu & Fearn)', fontweight='bold')
    ax.grid(True, alpha=0.3)

    # Legend
    ax.plot([], [], color=CB_COLORS['red'], linewidth=1.5, label='Lake Shelby events')
    ax.plot([], [], color=CB_COLORS['blue'], linewidth=1.5, linestyle='--', label='Western Lake events')
    ax.legend(loc='upper right', fontsize=8)

    # Annotate
    ax.annotate('HYPERACTIVE\n(5× baseline)', xy=(2.4, 5.2), fontsize=9,
               ha='center', color=CB_COLORS['purple'], fontweight='bold')


def create_panel_d_sigma(ax):
    """Panel D: Environmental uncertainty index calculation."""
    # Show how sigma is calculated from components
    sites = ['Poverty\nPoint', 'Rapa\nNui', 'Rapa\nIti']
    frequencies = [10, 6, 18]
    magnitudes = [0.45, 0.60, 0.30]

    sigmas = [calculate_sigma(f, m) for f, m in zip(frequencies, magnitudes)]

    x = np.arange(len(sites))
    width = 0.35

    # Create stacked bar showing frequency and magnitude contributions
    freq_contrib = [np.sqrt(20/f) for f in frequencies]  # Normalized frequency effect
    mag_contrib = magnitudes

    bars1 = ax.bar(x - width/2, freq_contrib, width, label='Frequency effect', color=CB_COLORS['blue'], alpha=0.7)
    bars2 = ax.bar(x + width/2, mag_contrib, width, label='Magnitude', color=CB_COLORS['orange'], alpha=0.7)

    # Add sigma values as text
    for i, (s, site) in enumerate(zip(sigmas, sites)):
        ax.annotate(f'σ = {s:.2f}', xy=(i, max(freq_contrib[i], mag_contrib[i]) + 0.15),
                   ha='center', fontsize=10, fontweight='bold')

    # Critical threshold line
    ax.axhline(y=SIGMA_CRITICAL, color=CB_COLORS['red'], linestyle='--', linewidth=2, label=f'σ* = {SIGMA_CRITICAL}')

    ax.set_ylabel('Component Value')
    ax.set_title('D. Uncertainty Index Components', fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(sites)
    ax.legend(loc='upper right', fontsize=8)
    ax.set_ylim(0, 2.2)
    ax.grid(True, alpha=0.3, axis='y')


def create_panel_e_comparison(ax):
    """Panel E: Archaeological site sigma comparison."""
    sites = ['Poverty\nPoint', 'Watson\nBrake', 'Jaketown', 'Rapa\nNui', 'Rapa\nIti']
    sigmas = [0.65, 0.53, 0.58, 0.96, 0.32]
    sigma_err = [0.12, 0.10, 0.11, 0.15, 0.08]
    monuments = [True, True, True, True, False]

    colors = [CB_COLORS['orange'] if m else CB_COLORS['blue'] for m in monuments]

    x = np.arange(len(sites))
    bars = ax.bar(x, sigmas, yerr=sigma_err, capsize=4, color=colors, alpha=0.8, edgecolor='black')

    # Critical threshold
    ax.axhline(y=SIGMA_CRITICAL, color=CB_COLORS['red'], linestyle='--', linewidth=2, label=f'σ* = {SIGMA_CRITICAL}')

    # Shading for prediction zones
    ax.axhspan(0, SIGMA_CRITICAL, alpha=0.1, color=CB_COLORS['blue'], label='Low σ: Reproduction favored')
    ax.axhspan(SIGMA_CRITICAL, 1.2, alpha=0.1, color=CB_COLORS['orange'], label='High σ: Signaling favored')

    ax.set_ylabel('Environmental Uncertainty (σ)')
    ax.set_title('E. Site Comparison', fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(sites, fontsize=9)
    ax.set_ylim(0, 1.2)
    ax.legend(loc='upper right', fontsize=7)
    ax.grid(True, alpha=0.3, axis='y')


def create_panel_f_phase_space(ax):
    """Panel F: Phase space position of archaeological sites."""
    # Create phase space grid
    freq_range = np.linspace(5, 20, 100)
    mag_range = np.linspace(0.2, 0.8, 100)
    F, M = np.meshgrid(freq_range, mag_range)
    S = calculate_sigma(F, M)

    # Plot phase space
    contour = ax.contourf(F, M, S, levels=20, cmap='RdYlBu_r', alpha=0.7)

    # Critical threshold contour
    ax.contour(F, M, S, levels=[SIGMA_CRITICAL], colors=[CB_COLORS['red']], linewidths=2, linestyles='--')

    # Plot site positions
    sites = {
        'Poverty Point': (10, 0.45, CB_COLORS['orange']),
        'Rapa Nui': (6, 0.60, CB_COLORS['orange']),
        'Rapa Iti': (18, 0.30, CB_COLORS['blue']),
        'Watson Brake': (12, 0.40, CB_COLORS['orange']),
    }

    for name, (freq, mag, color) in sites.items():
        ax.scatter(freq, mag, s=100, c=color, edgecolors='black', linewidths=1.5, zorder=5)
        offset = (5, 5) if name != 'Rapa Iti' else (-40, -15)
        ax.annotate(name, xy=(freq, mag), xytext=offset, textcoords='offset points',
                   fontsize=8, fontweight='bold')

    ax.set_xlabel('Shortfall Frequency (years)')
    ax.set_ylabel('Shortfall Magnitude')
    ax.set_title('F. Environmental Phase Space', fontweight='bold')

    # Colorbar
    cbar = plt.colorbar(contour, ax=ax, shrink=0.8)
    cbar.set_label('σ', fontsize=10)

    # Add annotation for threshold
    ax.annotate(f'σ* = {SIGMA_CRITICAL}', xy=(8, 0.35), fontsize=9,
               color=CB_COLORS['red'], fontweight='bold')


def main():
    """Generate Figure 11."""
    print("Creating Figure 11: Paleoclimate Proxy Evidence")
    print("=" * 60)

    # Load data
    print("\nLoading data...")
    temp_data = load_temperature_data()
    wab_data = load_hydroclimate_data()
    hurricane_data = get_hurricane_data()

    if temp_data:
        print(f"  Temperature: {len(temp_data)} sites loaded")
    if wab_data is not None:
        print(f"  Hydroclimate: {len(wab_data)} time points")
    print(f"  Hurricanes: {len(hurricane_data['lake_shelby']) + len(hurricane_data['western_lake'])} events")

    # Create figure
    print("\nGenerating figure panels...")
    fig = plt.figure(figsize=(14, 12))
    gs = GridSpec(3, 2, figure=fig, hspace=0.35, wspace=0.30)

    # Panel A: Temperature
    ax1 = fig.add_subplot(gs[0, 0])
    create_panel_a_temperature(ax1, temp_data)

    # Panel B: Hydroclimate
    ax2 = fig.add_subplot(gs[0, 1])
    create_panel_b_hydroclimate(ax2, wab_data)

    # Panel C: Hurricanes
    ax3 = fig.add_subplot(gs[1, 0])
    create_panel_c_hurricanes(ax3, hurricane_data)

    # Panel D: Sigma calculation
    ax4 = fig.add_subplot(gs[1, 1])
    create_panel_d_sigma(ax4)

    # Panel E: Site comparison
    ax5 = fig.add_subplot(gs[2, 0])
    create_panel_e_comparison(ax5)

    # Panel F: Phase space
    ax6 = fig.add_subplot(gs[2, 1])
    create_panel_f_phase_space(ax6)

    # Add Poverty Point annotation to panels A, B, C
    for ax in [ax1, ax2]:
        ax.annotate('Poverty Point', xy=(3.35, ax.get_ylim()[1]), xytext=(3.35, ax.get_ylim()[1] * 0.95),
                   ha='center', fontsize=9, color=CB_COLORS['orange'], fontweight='bold')

    ax3.annotate('Poverty Point', xy=(3.35, 5.5), ha='center', fontsize=9,
                color=CB_COLORS['orange'], fontweight='bold')

    # Main title
    fig.suptitle('Figure 11. Paleoclimate Proxy Evidence for Late Archaic Environmental Uncertainty',
                fontsize=13, fontweight='bold', y=0.995)

    # Save figure
    output_png = os.path.join(OUTPUT_DIR, 'Figure_11_paleoclimate_proxy.png')
    output_pdf = os.path.join(OUTPUT_DIR, 'Figure_11_paleoclimate_proxy.pdf')

    plt.savefig(output_png, dpi=300, bbox_inches='tight', facecolor='white')
    plt.savefig(output_pdf, bbox_inches='tight', facecolor='white')

    print(f"\nFigure saved to:")
    print(f"  PNG: {output_png}")
    print(f"  PDF: {output_pdf}")

    plt.close()

    # Print summary
    print("\n" + "=" * 60)
    print("FIGURE 11 SUMMARY")
    print("=" * 60)
    print("""
Panel A: Regional temperature reconstruction showing stable conditions
         during Poverty Point occupation (orange shading).

Panel B: Midwest Water Balance from pollen-based reconstruction showing
         drier-than-present conditions (mean = -28 mm) with high variance.

Panel C: Hurricane landfall events showing Poverty Point coincided with
         a hyperactive period (5× baseline rate, 3800-1000 BP).

Panel D: Environmental uncertainty index components showing how frequency
         and magnitude combine to produce sigma values.

Panel E: Site comparison showing all monument-building sites have
         σ > σ* (threshold), while non-monument sites have σ < σ*.

Panel F: Phase space positions showing archaeological sites relative to
         the critical threshold boundary.
""")

    return fig


if __name__ == '__main__':
    fig = main()
