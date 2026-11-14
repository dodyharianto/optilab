def nearest_neighbor(distance_matrix, start=0):
    """
    Get the route using nearest neighbor heuristic.

    Each iteration, visit the unvisited customer with shortest distance.

    Returns:
        A route starting and ending at the depot.
    """
    n_locations = len(distance_matrix)

    unvisited = set(range(n_locations))
    unvisited.remove(start)

    route = [start]
    current = start

    while unvisited:

        next_location = min(
            unvisited,
            key=lambda location: distance_matrix[current][location]
        )

        route.append(next_location)
        unvisited.remove(next_location)

        current = next_location

    route.append(start)
    return route

def calculate_route_distance(route, distance_matrix):
    """
    Using the route obtained from nearest neighbor, compute total distance for the route.

    Returns:
        The total distance for entire route.
    """
    total_distance = 0
    for i in range(len(route) - 1):
        total_distance += distance_matrix[route[i]][route[i + 1]]
    return total_distance
