"""
Visualize population dynamics in the Poverty Point ABM.

This script analyzes:
1. Total population trajectories under different conditions
2. Band size distributions
3. Strategy switching dynamics
4. Demographic responses to shortfalls
5. Fitness differentials and selection pressure
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from poverty_point.core_simulation import PovertyPointSimulation
from poverty_point.parameters import default_parameters, critical_threshold


def run_detailed_trajectory(sigma: float, epsilon: float, seed: int = 42,
                            duration: int = 600) -> dict:
    """
    Run simulation and extract detailed population dynamics.
    """
    params = default_parameters(sigma=sigma, epsilon=epsilon, seed=seed)
    params.duration = duration

    sim = PovertyPointSimulation(params)
    sim.run(verbose=False)

    states = sim.results.yearly_states

    return {
        'sigma': sigma,
        'epsilon': epsilon,
        'years': np.array([s.year for s in states]),
        'total_pop': np.array([s.total_population for s in states]),
        'n_bands': np.array([s.n_bands for s in states]),
        'mean_band_size': np.array([s.mean_band_size for s in states]),
        'n_aggregators': np.array([s.n_aggregators for s in states]),
        'n_independents': np.array([s.n_independents for s in states]),
        'dominance': np.array([s.strategy_dominance for s in states]),
        'in_shortfall': np.array([s.in_shortfall for s in states]),
        'shortfall_mag': np.array([s.shortfall_magnitude for s in states]),
        'fitness_agg': np.array([s.mean_fitness_aggregators for s in states]),
        'fitness_ind': np.array([s.mean_fitness_independents for s in states]),
        'aggregation_size': np.array([s.aggregation_size for s in states]),
        'aggregation_pop': np.array([s.aggregation_population for s in states]),
        'sigma_star': critical_threshold(epsilon, 25, params)
    }


def create_population_dynamics_figure(output_dir: str = "figures/diagnostics"):
    """
    Create comprehensive population dynamics visualization.
    """
    os.makedirs(output_dir, exist_ok=True)

    fig = plt.figure(figsize=(18, 16))
    gs = fig.add_gridspec(4, 3, hspace=0.35, wspace=0.3)

    epsilon = 0.35

    # Run trajectories at different sigma values
    trajectories = {}
    sigma_values = [0.35, 0.45, 0.55, 0.65, 0.75]
    colors = plt.cm.plasma(np.linspace(0.1, 0.9, len(sigma_values)))

    print("Running simulations...")
    for sig in sigma_values:
        print(f"  σ={sig:.2f}")
        trajectories[sig] = run_detailed_trajectory(sig, epsilon, seed=42)

    sigma_star = trajectories[0.55]['sigma_star']

    # ======== Panel A: Total population over time ========
    ax1 = fig.add_subplot(gs[0, 0])

    for sig, color in zip(sigma_values, colors):
        traj = trajectories[sig]
        ax1.plot(traj['years'], traj['total_pop'], color=color,
                 linewidth=1.5, label=f'σ={sig:.2f}', alpha=0.8)

    ax1.set_xlabel('Year')
    ax1.set_ylabel('Total Population')
    ax1.set_title('A. Population Trajectories')
    ax1.legend(loc='upper left', fontsize=9)
    ax1.grid(True, alpha=0.3)

    # ======== Panel B: Strategy composition over time ========
    ax2 = fig.add_subplot(gs[0, 1])

    # Show one trajectory in detail (use 0.65 which is in sigma_values)
    traj = trajectories[0.65]

    ax2.fill_between(traj['years'], 0, traj['n_aggregators'],
                     alpha=0.6, color='orange', label='Aggregators')
    ax2.fill_between(traj['years'], traj['n_aggregators'],
                     traj['n_aggregators'] + traj['n_independents'],
                     alpha=0.6, color='purple', label='Independents')

    ax2.set_xlabel('Year')
    ax2.set_ylabel('Number of Bands')
    ax2.set_title('B. Strategy Composition (σ=0.60)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # ======== Panel C: Fitness differential ========
    ax3 = fig.add_subplot(gs[0, 2])

    for sig, color in zip([0.45, 0.55, 0.65], colors[1:4]):
        traj = trajectories[sig]
        # Calculate fitness differential
        diff = traj['fitness_agg'] - traj['fitness_ind']
        # Handle zeros
        diff = np.where(traj['fitness_agg'] > 0, diff, np.nan)

        # Smooth
        window = 20
        valid = ~np.isnan(diff)
        smoothed = np.full_like(diff, np.nan)
        smoothed[valid] = np.convolve(diff[valid],
                                      np.ones(window)/window, mode='same')

        ax3.plot(traj['years'], smoothed, color=color,
                 label=f'σ={sig:.2f}', linewidth=1.5)

    ax3.axhline(0, color='black', linestyle='--', alpha=0.5)
    ax3.set_xlabel('Year')
    ax3.set_ylabel('W_agg - W_ind')
    ax3.set_title('C. Fitness Differential')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # ======== Panel D: Shortfall events and population response ========
    ax4 = fig.add_subplot(gs[1, :2])

    traj = trajectories[0.65]

    # Show shortfall events as shaded regions
    shortfall_years = traj['years'][traj['in_shortfall']]
    for year in shortfall_years:
        ax4.axvspan(year, year+1, alpha=0.2, color='red')

    # Population trajectory
    ax4.plot(traj['years'], traj['total_pop'], 'b-', linewidth=1.5,
             label='Total population')

    # Mark severe shortfalls
    severe_idx = traj['shortfall_mag'] > 0.5
    ax4.scatter(traj['years'][severe_idx],
                traj['total_pop'][severe_idx],
                c='red', s=20, alpha=0.7, label='Severe shortfall')

    ax4.set_xlabel('Year')
    ax4.set_ylabel('Population')
    ax4.set_title('D. Population Response to Shortfalls (σ=0.65)\nRed shading = shortfall years')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    # ======== Panel E: Aggregation attendance distribution ========
    ax5 = fig.add_subplot(gs[1, 2])

    for sig, color in zip([0.45, 0.55, 0.65], colors[1:4]):
        traj = trajectories[sig]
        agg_sizes = traj['aggregation_size'][100:]  # Post burn-in

        ax5.hist(agg_sizes, bins=20, alpha=0.5, color=color,
                 label=f'σ={sig:.2f}', density=True)

    ax5.axvline(25, color='red', linestyle='--', label='Optimal n=25')
    ax5.set_xlabel('Bands at Aggregation')
    ax5.set_ylabel('Density')
    ax5.set_title('E. Aggregation Size Distribution')
    ax5.legend()
    ax5.grid(True, alpha=0.3)

    # ======== Panel F: Strategy switching frequency ========
    ax6 = fig.add_subplot(gs[2, 0])

    # Calculate switching frequency at each sigma
    switch_rates = []
    for sig in sigma_values:
        traj = trajectories[sig]
        dom = traj['dominance'][100:]  # Post burn-in

        # Switching = changes in dominance direction
        switches = np.sum(np.abs(np.diff(np.sign(dom))) > 0)
        rate = switches / len(dom)
        switch_rates.append(rate)

    ax6.bar(range(len(sigma_values)), switch_rates, color=colors)
    ax6.set_xticks(range(len(sigma_values)))
    ax6.set_xticklabels([f'{s:.2f}' for s in sigma_values])
    ax6.set_xlabel('Environmental Uncertainty (σ)')
    ax6.set_ylabel('Strategy Switching Rate')
    ax6.set_title('F. Strategy Volatility')
    ax6.axvline(sigma_values.index(min(sigma_values,
                                       key=lambda x: abs(x - sigma_star))),
                color='blue', linestyle='--', alpha=0.5, label=f'σ* ≈ {sigma_star:.2f}')
    ax6.legend()
    ax6.grid(True, alpha=0.3, axis='y')

    # ======== Panel G: Mean band size by strategy ========
    ax7 = fig.add_subplot(gs[2, 1])

    # This would require tracking band-level data, approximate with aggregation pop/size
    for sig, color in zip([0.45, 0.55, 0.65], colors[1:4]):
        traj = trajectories[sig]

        # Approximate mean band size at aggregation
        valid = traj['aggregation_size'] > 0
        mean_size_at_agg = traj['aggregation_pop'][valid] / traj['aggregation_size'][valid]

        ax7.plot(traj['years'][valid], mean_size_at_agg, color=color,
                 label=f'σ={sig:.2f}', alpha=0.6)

    ax7.set_xlabel('Year')
    ax7.set_ylabel('Mean Band Size at Aggregation')
    ax7.set_title('G. Band Size at Aggregations')
    ax7.legend()
    ax7.grid(True, alpha=0.3)

    # ======== Panel H: Phase portrait (dominance vs population) ========
    ax8 = fig.add_subplot(gs[2, 2])

    for sig, color in zip([0.45, 0.55, 0.65], colors[1:4]):
        traj = trajectories[sig]

        # Post burn-in only
        dom = traj['dominance'][100:]
        pop = traj['total_pop'][100:]

        ax8.scatter(dom, pop, c=[color], alpha=0.3, s=10, label=f'σ={sig:.2f}')

    ax8.set_xlabel('Strategy Dominance')
    ax8.set_ylabel('Total Population')
    ax8.set_title('H. Phase Portrait')
    ax8.legend()
    ax8.grid(True, alpha=0.3)
    ax8.axvline(0, color='black', linestyle='--', alpha=0.5)

    # ======== Panel I: Selection strength over time ========
    ax9 = fig.add_subplot(gs[3, 0])

    traj = trajectories[0.65]

    # Selection strength = |fitness_agg - fitness_ind| * population variance
    fitness_diff = np.abs(traj['fitness_agg'] - traj['fitness_ind'])
    # Proxy for population variance: strategy dominance magnitude
    selection = fitness_diff * np.abs(traj['dominance'])

    window = 20
    smoothed = np.convolve(selection, np.ones(window)/window, mode='valid')

    ax9.plot(traj['years'][window-1:], smoothed, 'g-', linewidth=1.5)
    ax9.set_xlabel('Year')
    ax9.set_ylabel('Selection Strength')
    ax9.set_title('I. Selection Pressure Over Time (σ=0.60)')
    ax9.grid(True, alpha=0.3)

    # ======== Panel J: Final population vs sigma ========
    ax10 = fig.add_subplot(gs[3, 1])

    final_pops = [trajectories[sig]['total_pop'][-1] for sig in sigma_values]

    ax10.bar(range(len(sigma_values)), final_pops, color=colors)
    ax10.set_xticks(range(len(sigma_values)))
    ax10.set_xticklabels([f'{s:.2f}' for s in sigma_values])
    ax10.set_xlabel('Environmental Uncertainty (σ)')
    ax10.set_ylabel('Final Population')
    ax10.set_title('J. Final Population by σ')
    ax10.axvline(sigma_values.index(min(sigma_values,
                                        key=lambda x: abs(x - sigma_star))),
                 color='blue', linestyle='--', alpha=0.5)
    ax10.grid(True, alpha=0.3, axis='y')

    # ======== Panel K: Aggregation efficiency ========
    ax11 = fig.add_subplot(gs[3, 2])

    # Efficiency = population at aggregation / total bands attending
    for sig, color in zip([0.45, 0.55, 0.65], colors[1:4]):
        traj = trajectories[sig]

        # Post burn-in
        valid = traj['aggregation_size'][100:] > 0
        efficiency = (traj['aggregation_pop'][100:][valid] /
                     traj['aggregation_size'][100:][valid])

        ax11.hist(efficiency, bins=15, alpha=0.5, color=color,
                  label=f'σ={sig:.2f}', density=True)

    ax11.set_xlabel('Mean Band Size at Aggregation')
    ax11.set_ylabel('Density')
    ax11.set_title('K. Aggregation Efficiency')
    ax11.legend()
    ax11.grid(True, alpha=0.3)

    plt.suptitle('Population Dynamics in the Poverty Point Aggregation Model',
                 fontsize=16, fontweight='bold', y=1.01)

    # Save
    fig.savefig(os.path.join(output_dir, 'population_dynamics.png'),
                dpi=150, bbox_inches='tight', facecolor='white')
    fig.savefig(os.path.join(output_dir, 'population_dynamics.pdf'),
                bbox_inches='tight', facecolor='white')
    plt.close(fig)

    print(f"\nPopulation dynamics figure saved to {output_dir}/population_dynamics.png")

    # Print summary
    print("\n" + "="*60)
    print("POPULATION DYNAMICS SUMMARY")
    print("="*60)

    for sig in sigma_values:
        traj = trajectories[sig]
        print(f"\nσ={sig:.2f}:")
        print(f"  Final population: {traj['total_pop'][-1]}")
        print(f"  Mean population (post-burn-in): {np.mean(traj['total_pop'][100:]):.0f}")
        print(f"  Mean aggregation size: {np.mean(traj['aggregation_size'][100:]):.1f} bands")
        print(f"  Mean fitness differential: {np.mean(traj['fitness_agg'][100:] - traj['fitness_ind'][100:]):.4f}")

    return trajectories


if __name__ == "__main__":
    trajectories = create_population_dynamics_figure()
