from matplotlib import pyplot as plt
from optilab.data import generate_locations
from optilab.distance import calculate_distance_matrix
from optilab.baseline import nearest_neighbor, two_opt, calculate_route_distance
from optilab.visualize import visualize_routing

def main():
    locations, labels = generate_locations()
    distance_matrix = calculate_distance_matrix(locations)

    # nearest neighbor
    nn_route = nearest_neighbor(distance_matrix)
    nn_distance = calculate_route_distance(nn_route, distance_matrix)

    # 2-opt
    two_opt_route, two_opt_distance = two_opt(nn_route, distance_matrix)

    print('Nearest neighbor route: ', nn_route)
    print('Nearest neighbor total distance: ', nn_distance)

    print('Nearest neighbor + 2-opt route: ', two_opt_route)
    print('Nearest neighbor + 2-opt total distance: ', two_opt_distance)

    print('Improvement: ', 100 * (nn_distance - two_opt_distance) / nn_distance, '%')

    visualize_routing(locations, nn_route, labels, 'nearest_neighbor.png')
    visualize_routing(locations, two_opt_route, labels, '2-opt.png')

if __name__ == '__main__':
    main()