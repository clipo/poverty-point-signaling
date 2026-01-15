"""
Visualize monument accumulation trajectories at Poverty Point.

Key insight: Monument building is CUMULATIVE and SELF-REINFORCING.
- Each year's investment adds to the total
- Larger monuments attract more participants
- More participants → more investment → larger monuments
- This creates positive feedback that distinguishes PP from other sites

This script visualizes:
1. Monument growth trajectories under different conditions
2. The feedback between attendance and investment
3. How environmental conditions affect accumulation rates
4. The "takeoff" dynamics when aggregation becomes dominant
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from poverty_point.core_simulation import PovertyPointSimulation
from poverty_point.parameters import default_parameters, critical_threshold


def run_trajectory(sigma: float, epsilon: float, seed: int = 42,
                   duration: int = 600) -> dict:
    """
    Run simulation and extract monument trajectory with full detail.
    """
    params = default_parameters(sigma=sigma, epsilon=epsilon, seed=seed)
    params.duration = duration

    sim = PovertyPointSimulation(params)
    sim.run(verbose=False)

    # Extract time series
    years = [s.year for s in sim.results.yearly_states]
    monument = [s.monument_level for s in sim.results.yearly_states]
    construction = [s.annual_construction for s in sim.results.yearly_states]
    attendance = [s.aggregation_size for s in sim.results.yearly_states]
    population = [s.aggregation_population for s in sim.results.yearly_states]
    dominance = [s.strategy_dominance for s in sim.results.yearly_states]
    exotics = [s.total_exotics for s in sim.results.yearly_states]

    return {
        'sigma': sigma,
        'epsilon': epsilon,
        'years': np.array(years),
        'monument': np.array(monument),
        'construction': np.array(construction),
        'attendance': np.array(attendance),
        'population': np.array(population),
        'dominance': np.array(dominance),
        'exotics': np.array(exotics),
        'sigma_star': critical_threshold(epsilon, 25, params)
    }


def analyze_feedback_dynamics(trajectory: dict) -> dict:
    """
    Analyze the feedback between attendance and construction.

    Returns correlation and phase statistics.
    """
    # Skip burn-in
    att = trajectory['attendance'][100:]
    con = trajectory['construction'][100:]
    mon = trajectory['monument'][100:]

    # Correlation between attendance and construction
    corr_att_con = np.corrcoef(att, con)[0, 1]

    # Growth rate of monument
    growth_rates = np.diff(mon) / (mon[:-1] + 1)  # Avoid div by zero

    # Identify "takeoff" point - when growth accelerates
    # Look for sustained positive second derivative
    accel = np.diff(growth_rates)
    takeoff_idx = None
    for i in range(len(accel) - 10):
        if np.mean(accel[i:i+10]) > 0.001:
            takeoff_idx = i + 100  # Add burn-in offset
            break

    return {
        'correlation_attendance_construction': corr_att_con,
        'mean_growth_rate': np.mean(growth_rates),
        'max_growth_rate': np.max(growth_rates),
        'takeoff_year': takeoff_idx,
        'final_monument': mon[-1]
    }


def create_monument_trajectory_figure(output_dir: str = "figures/diagnostics"):
    """
    Create comprehensive figure showing monument accumulation dynamics.
    """
    os.makedirs(output_dir, exist_ok=True)

    fig = plt.figure(figsize=(16, 14))

    # Define grid
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

    # ======== Panel A: Monument trajectories across sigma ========
    ax1 = fig.add_subplot(gs[0, :2])

    sigma_values = [0.35, 0.45, 0.55, 0.65, 0.75]
    epsilon = 0.35
    colors = plt.cm.viridis(np.linspace(0, 1, len(sigma_values)))

    trajectories = {}
    for sig, color in zip(sigma_values, colors):
        traj = run_trajectory(sig, epsilon, seed=42, duration=600)
        trajectories[sig] = traj

        label = f'σ={sig:.2f}'
        if sig > traj['sigma_star']:
            label += ' (above σ*)'

        ax1.plot(traj['years'], traj['monument'], color=color,
                 linewidth=2, label=label)

    ax1.set_xlabel('Year', fontsize=12)
    ax1.set_ylabel('Cumulative Monument Level', fontsize=12)
    ax1.set_title('A. Monument Accumulation Trajectories\n'
                  f'(ε={epsilon}, σ* ≈ {traj["sigma_star"]:.2f})', fontsize=14)
    ax1.legend(loc='upper left')
    ax1.grid(True, alpha=0.3)

    # Add annotation about feedback
    ax1.annotate('Higher σ → more aggregation\n→ faster accumulation',
                 xy=(400, trajectories[0.75]['monument'][400]),
                 xytext=(200, trajectories[0.75]['monument'][400] * 0.7),
                 fontsize=10, ha='center',
                 arrowprops=dict(arrowstyle='->', color='gray'),
                 bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    # ======== Panel B: Annual construction rate ========
    ax2 = fig.add_subplot(gs[0, 2])

    for sig, color in zip([0.45, 0.55, 0.65], colors[1:4]):
        traj = trajectories[sig]
        # Smooth construction rate
        window = 20
        smoothed = np.convolve(traj['construction'],
                               np.ones(window)/window, mode='valid')
        ax2.plot(traj['years'][window-1:], smoothed, color=color,
                 label=f'σ={sig:.2f}')

    ax2.set_xlabel('Year', fontsize=12)
    ax2.set_ylabel('Construction Rate\n(smoothed)', fontsize=12)
    ax2.set_title('B. Annual Construction', fontsize=14)
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # ======== Panel C: Attendance-Construction feedback ========
    ax3 = fig.add_subplot(gs[1, 0])

    # Show for one trajectory above threshold
    traj = trajectories[0.65]
    att = traj['attendance'][100:]
    con = traj['construction'][100:]

    ax3.scatter(att, con, alpha=0.3, s=20, c='purple')

    # Add trend line
    z = np.polyfit(att, con, 1)
    p = np.poly1d(z)
    x_line = np.linspace(min(att), max(att), 100)
    ax3.plot(x_line, p(x_line), 'r-', linewidth=2, label='Trend')

    corr = np.corrcoef(att, con)[0, 1]
    ax3.text(0.05, 0.95, f'r = {corr:.2f}', transform=ax3.transAxes,
             fontsize=12, va='top',
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    ax3.set_xlabel('Bands Attending', fontsize=12)
    ax3.set_ylabel('Annual Construction', fontsize=12)
    ax3.set_title('C. Feedback: Attendance → Construction\n(σ=0.65)', fontsize=14)
    ax3.grid(True, alpha=0.3)

    # ======== Panel D: Monument vs Population at site ========
    ax4 = fig.add_subplot(gs[1, 1])

    for sig, color in zip([0.45, 0.55, 0.65], colors[1:4]):
        traj = trajectories[sig]
        # Show relationship between monument and attending population
        ax4.scatter(traj['monument'][100:], traj['population'][100:],
                   alpha=0.3, s=15, color=color, label=f'σ={sig:.2f}')

    ax4.set_xlabel('Monument Level', fontsize=12)
    ax4.set_ylabel('Population at Aggregation', fontsize=12)
    ax4.set_title('D. Monument Size vs Attendance', fontsize=14)
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    # ======== Panel E: Strategy dominance over time ========
    ax5 = fig.add_subplot(gs[1, 2])

    for sig, color in zip(sigma_values, colors):
        traj = trajectories[sig]
        # Smooth dominance
        window = 20
        smoothed = np.convolve(traj['dominance'],
                               np.ones(window)/window, mode='valid')
        ax5.plot(traj['years'][window-1:], smoothed, color=color,
                 label=f'σ={sig:.2f}', linewidth=1.5)

    ax5.axhline(0, color='black', linestyle='--', alpha=0.5)
    ax5.set_xlabel('Year', fontsize=12)
    ax5.set_ylabel('Strategy Dominance\n(+ = aggregators)', fontsize=12)
    ax5.set_title('E. Strategy Evolution', fontsize=14)
    ax5.legend(loc='lower right', fontsize=9)
    ax5.grid(True, alpha=0.3)
    ax5.set_ylim(-1, 1)

    # ======== Panel F: Multiple realizations (stochastic variation) ========
    ax6 = fig.add_subplot(gs[2, 0])

    # Run multiple seeds at one sigma
    sigma_test = 0.60
    for seed in range(8):
        traj = run_trajectory(sigma_test, epsilon, seed=seed, duration=600)
        ax6.plot(traj['years'], traj['monument'], alpha=0.5, linewidth=1)

    ax6.set_xlabel('Year', fontsize=12)
    ax6.set_ylabel('Monument Level', fontsize=12)
    ax6.set_title(f'F. Stochastic Variation\n(σ={sigma_test}, 8 replicates)', fontsize=14)
    ax6.grid(True, alpha=0.3)

    # ======== Panel G: Growth rate acceleration ========
    ax7 = fig.add_subplot(gs[2, 1])

    traj = trajectories[0.65]
    mon = traj['monument'][50:]  # Skip early years

    # Calculate growth rate
    growth = np.diff(mon) / (mon[:-1] + 1)

    # Smooth
    window = 30
    smoothed_growth = np.convolve(growth, np.ones(window)/window, mode='valid')

    ax7.plot(traj['years'][50+window:], smoothed_growth, 'b-', linewidth=2)
    ax7.axhline(0, color='black', linestyle='--', alpha=0.5)

    ax7.set_xlabel('Year', fontsize=12)
    ax7.set_ylabel('Growth Rate\n(ΔM / M)', fontsize=12)
    ax7.set_title('G. Monument Growth Acceleration\n(σ=0.65)', fontsize=14)
    ax7.grid(True, alpha=0.3)

    # Mark phases
    ax7.axvspan(50, 150, alpha=0.2, color='gray', label='Burn-in')
    ax7.axvspan(150, 300, alpha=0.2, color='yellow', label='Growth phase')
    ax7.axvspan(300, 600, alpha=0.2, color='green', label='Mature phase')

    # ======== Panel H: Exotic goods accumulation ========
    ax8 = fig.add_subplot(gs[2, 2])

    for sig, color in zip([0.45, 0.55, 0.65, 0.75], colors[1:]):
        traj = trajectories[sig]
        ax8.plot(traj['years'], traj['exotics'], color=color,
                 label=f'σ={sig:.2f}', linewidth=1.5)

    ax8.set_xlabel('Year', fontsize=12)
    ax8.set_ylabel('Total Exotic Goods', fontsize=12)
    ax8.set_title('H. Exotic Goods Accumulation', fontsize=14)
    ax8.legend()
    ax8.grid(True, alpha=0.3)

    plt.suptitle('Monument Building as Cumulative Aggregate Signaling at Poverty Point',
                 fontsize=16, fontweight='bold', y=1.02)

    # Save
    fig.savefig(os.path.join(output_dir, 'monument_trajectories.png'),
                dpi=150, bbox_inches='tight', facecolor='white')
    fig.savefig(os.path.join(output_dir, 'monument_trajectories.pdf'),
                bbox_inches='tight', facecolor='white')
    plt.close(fig)

    print(f"\nMonument trajectory figure saved to {output_dir}/monument_trajectories.png")

    # Print summary statistics
    print("\n" + "="*60)
    print("MONUMENT ACCUMULATION SUMMARY")
    print("="*60)

    for sig in [0.45, 0.55, 0.65, 0.75]:
        traj = trajectories[sig]
        stats = analyze_feedback_dynamics(traj)
        print(f"\nσ={sig:.2f} (σ* = {traj['sigma_star']:.2f}):")
        print(f"  Final monument level: {stats['final_monument']:.0f}")
        print(f"  Attendance-construction correlation: {stats['correlation_attendance_construction']:.2f}")
        print(f"  Mean growth rate: {stats['mean_growth_rate']:.4f}")
        if stats['takeoff_year']:
            print(f"  Takeoff year: {stats['takeoff_year']}")

    return trajectories


if __name__ == "__main__":
    trajectories = create_monument_trajectory_figure()
