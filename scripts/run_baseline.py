from matplotlib import pyplot as plt
from optilab.data import generate_locations
from optilab.distance import calculate_distance_matrix
from optilab.baseline import nearest_neighbor, calculate_route_distance

def main():
    locations, labels = generate_locations()
    distance_matrix = calculate_distance_matrix(locations)
    route = nearest_neighbor(distance_matrix)
    total_distance = calculate_route_distance(route, distance_matrix)

    print('Route: ', route)
    print('Total distance needed: ', total_distance)

    plt.figure(figsize=(9, 7))

    route_locations = locations[route]
    plt.plot(route_locations[:, 0], route_locations[:, 1], marker='o', linestyle='-')
    plt.scatter(locations[0, 0], locations[0, 1], marker='s', s=180, label='Depot')
    plt.scatter(locations[1:, 0], locations[1:, 1], s=80, label='Customers')

    for i, (x, y) in enumerate(locations):
        plt.annotate(labels[i], (x, y), xytext=(5, 5), textcoords='offset points')

    plt.title('OptiLab - Nearest Neighbor Routing')
    plt.xlabel('X coordinate')
    plt.ylabel('Y coordinate')
    plt.legend()
    plt.grid(alpha=0.3)

    plt.savefig('outputs/nearest_neighbor.png', dpi=150)
    plt.show()

if __name__ == '__main__':
    main()