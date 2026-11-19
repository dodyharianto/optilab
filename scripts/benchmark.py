import os
from time import perf_counter

import matplotlib.pyplot as plt
import pandas as pd

from optilab.baseline import calculate_route_distance, nearest_neighbor, two_opt
from optilab.data import generate_locations
from optilab.distance import calculate_distance_matrix
from optilab.exact import mixed_integer_lp


def main():
    seeds = range(10)
    customer_counts = [10, 15, 25, 50, 100]
    results = []

    for n_customers in customer_counts:
        for seed in seeds:
            locations, _ = generate_locations(n_customers=n_customers, seed=seed)
            distance_matrix = calculate_distance_matrix(locations)

            start = perf_counter()
            nn_route = nearest_neighbor(distance_matrix)
            nn_distance = calculate_route_distance(nn_route, distance_matrix)
            results.append({
                'seed': seed,
                'n_customers': n_customers,
                'method': 'nearest_neighbor',
                'distance': nn_distance,
                'runtime_seconds': perf_counter() - start,
            })

            start = perf_counter()
            nn_route = nearest_neighbor(distance_matrix)
            _, two_opt_distance = two_opt(nn_route, distance_matrix)
            results.append({
                'seed': seed,
                'n_customers': n_customers,
                'method': 'nearest_neighbor_2opt',
                'distance': two_opt_distance,
                'runtime_seconds': perf_counter() - start,
            })

            if n_customers in (10, 15):
                start = perf_counter()
                _, milp_distance = mixed_integer_lp(distance_matrix)
                results.append({
                    'seed': seed,
                    'n_customers': n_customers,
                    'method': 'milp',
                    'distance': milp_distance,
                    'runtime_seconds': perf_counter() - start,
                })

    output_directory = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'outputs',
        'benchmark_results',
    )
    os.makedirs(output_directory, exist_ok=True)
    results_frame = pd.DataFrame(results)
    csv_path = os.path.join(output_directory, 'benchmark.csv')
    results_frame.to_csv(csv_path, index=False)

    method_labels = {
        'nearest_neighbor': 'Nearest Neighbor',
        'nearest_neighbor_2opt': 'Nearest Neighbor + 2-opt',
        'milp': 'MILP',
    }
    mean_distances = results_frame.groupby(
        ['n_customers', 'method']
    )['distance'].mean().unstack().rename(columns=method_labels)
    methods = list(method_labels.values())
    colors = ['#4C78A8', '#F2A541', '#54A24B']
    ax = mean_distances[methods].plot(
        kind='bar',
        figsize=(10, 6),
        color=colors,
        width=0.8,
    )
    ax.set_title('Average Route Distance by Instance Size (10 seeds)')
    ax.set_xlabel('Number of customers')
    ax.set_ylabel('Average distance')
    ax.set_xticklabels(customer_counts, rotation=0)
    ax.set_axisbelow(True)
    ax.grid(axis='y', linestyle='--', alpha=0.35)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.legend(
        title='Method',
        frameon=False,
        loc='upper left',
        bbox_to_anchor=(1.02, 1),
    )
    for bar in ax.patches:
        height = bar.get_height()
        if height > 0:
            plt.text(
                bar.get_x() + bar.get_width() / 2,
                height,
                f'{height:.1f}',
                ha='center',
                va='bottom',
                fontsize=8,
                rotation=90,
            )
    plt.tight_layout()
    chart_path = os.path.join(output_directory, 'benchmark.png')
    plt.savefig(chart_path, dpi=160, bbox_inches='tight')
    plt.close()

    print(f'Benchmark results saved to {csv_path}')
    print(f'Benchmark chart saved to {chart_path}')


if __name__ == '__main__':
    main()
