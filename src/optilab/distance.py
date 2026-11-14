import numpy as np

def calculate_distance_matrix(locations):
    """
    Calculates all distance between location i and location j.

    Returns:
        An euclidean distance matrix.
    """
    pairwise_euclidean = []
    for i in range(len(locations)):
        row = []
        for j in range(len(locations)):
            x_distance = locations[i][0] - locations[j][0]
            y_distance = locations[i][1] - locations[j][1]
            distance = np.sqrt(x_distance ** 2 + y_distance ** 2)
            row.append(distance)
        pairwise_euclidean.append(row)

    return pairwise_euclidean