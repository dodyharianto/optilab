import pulp

def capacitated_vrp(distance_matrix, demands, n_vehicles, vehicle_capacity):
    routes = []

    n = len(distance_matrix)
    model = pulp.LpProblem('CVRP', pulp.LpMinimize)

    # decision variable
    x = {
        (i, j, k): model.add_variable(f'x_{i}_{j}{k}', cat='Binary')
        for i in range(n)
        for j in range(n)
        for k in range(n_vehicles)
        if i != j
    }

    # calculate total distance
    model += pulp.lpSum(distance_matrix[i][j] * x[i, j, k] for i, j, k in x)

    # every customer must be visited exactly once
    for j in range(1, n):
        model += pulp.lpSum(
            x[i, j, k]
            for i in range(n)
            if i != j
            for k in range(n_vehicles)
        ) == 1

    # flow constraint, every vehicle entering a customer must leave it (after i to j, next step must start from j)
    for j in range(1, n):
        for k in range(n_vehicles):
            model += (pulp.lpSum(x[i, j, k] for i in range(n) if i != j) == pulp.lpSum(x[j, l, k] for l in range(n) if l != j))

    return routes
    