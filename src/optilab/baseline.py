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
        next_location = min(unvisited, key=lambda location: distance_matrix[current][location])
        route.append(next_location)
        unvisited.remove(next_location)
        current = next_location

    route.append(start)
    return route

def two_opt_swap(route, i, j):
    """
    Core operation for 2-opt algorithm, reversing segment between location i and j.

    Returns:
        A new candidate route, with two edges removed and reconnected.
    """
    return route[:i] + route[i:j+1][::-1] + route[j+1:]

def two_opt(route, distance_matrix):
    """
    Improve a route through repeated 2-opt swaps.

    Returns:
        The improved route and its total distance.
    """
    best_route = route.copy()
    shortest_distance = calculate_route_distance(best_route, distance_matrix)

    improved = True
    while improved:
        improved = False
        for i in range(1, len(best_route) - 2):
            for j in range(i + 1, len(best_route) - 1):
                if j - i == 1: # avoid adjacent locations
                    continue

                candidate_route = two_opt_swap(best_route, i, j)
                candidate_distance = calculate_route_distance(candidate_route, distance_matrix)
                if candidate_distance < shortest_distance:
                    best_route = candidate_route
                    shortest_distance = candidate_distance
                    improved = True
                    break

            if improved:
                break

    return best_route, shortest_distance


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