from optilab.exact import mixed_integer_lp
from optilab.data import generate_locations
from optilab.distance import calculate_distance_matrix
from optilab.exact import mixed_integer_lp
from optilab.visualize import visualize_routing

def main():
    locations, labels = generate_locations()
    distance_matrix = calculate_distance_matrix(locations)

    route, total_distance = mixed_integer_lp(distance_matrix)

    print('MILP Result')
    print('Optimal route:', route)
    print('Total distance:', total_distance)

    visualize_routing(locations, route, labels, 'milp.png')

if __name__ == '__main__':
    main()