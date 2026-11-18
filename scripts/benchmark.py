import os
from time import perf_counter

import pandas as pd

from optilab.baseline import calculate_route_distance, nearest_neighbor, two_opt
from optilab.data import generate_locations
from optilab.distance import calculate_distance_matrix
from optilab.exact import mixed_integer_lp


def main():
    seeds = [42, 123, 456, 789, 2026]
    n_customers = 10
    results = []

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
    output_path = os.path.join(output_directory, 'benchmark.csv')
    pd.DataFrame(results).to_csv(output_path, index=False)

    print(f'Benchmark results saved to {output_path}')


if __name__ == '__main__':
    main()
