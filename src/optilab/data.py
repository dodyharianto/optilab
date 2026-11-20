import numpy as np

def generate_locations(n_customers=10, seed=42):
    """
    Generate locations of customers in arbitrary points.
    Assumptions:
    - location 0 is depot.
    - location 1, ..., n are customer locations.
    - there is exactly 1 operating vehicle, same as Traveling Salesman Problem (TSP).

    Returns:
        List of locations and labels (depot or customer i).
    """
    random_generator = np.random.default_rng(seed)

    depot = np.array([[50, 50]])
    customers = random_generator.uniform(low=10, high=100, size=(n_customers, 2))

    locations = np.vstack([depot, customers])
    labels = ['Depot'] + [f'Customer {i}' for i in range(1, n_customers + 1)]

    return locations, labels

def generate_cvrp_data(n_customers=10, n_vehicles=2, seed=42):
    """
    Generate Capacitated VRP locations and customer demands.

    Assumptions:
    - location 0 is depot,
    - location 1, ..., n are customer locations.
    - depot demand is 0.
    - each customer has a positive integer demand

    Returns:
        List of locations, labels (depot or customer i), and demand at each location.
    """
    locations, labels = generate_locations(n_customers=n_customers, seed=seed)

    random_generator = np.random.default_rng(seed)

    # demands for n customers + 1 depot, random for customers
    demands = np.zeros(n_customers + 1, dtype=int)
    demands[1:] = random_generator.integers(low=1, high=6, size=n_customers)

    return locations, labels, demands