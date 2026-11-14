import numpy as np

def generate_locations(n_customers=10, seed=42):
    """
    Assuming location 0 is depot,
    And location 1, ..., n are customer locations.

    Returns:
        List of locations and labels (depot or customer i).
    """
    random_generator = np.random.default_rng(seed)

    depot = np.array([[50, 50]])
    customers = random_generator.uniform(low=10, high=100, size=(n_customers, 2))

    locations = np.vstack([depot, customers])
    labels = ['Depot'] + [f'Customer {i}' for i in range(1, n_customers + 1)]

    return locations, labels