import pulp

def mixed_integer_lp(distance_matrix):
    """
    Solve TSP exactly using Mixed-Integer Linear Programming (TSP first for now).

    Constraints:
    - exactly one outgoing route from a customer.
    - exactly one incoming route to a customer.
    - no subtours, handled by Miller-Tucker-Zemlin subtour elimination. 

    Returns:
        Optimal route and total distance.
    """

    n = len(distance_matrix)
    model = pulp.LpProblem('TSP', pulp.LpMinimize)

    # decision variables
    x = {
        (i, j): model.add_variable(f'x_{i}_{j}', cat='Binary')
        for i in range(n)
        for j in range(n)
        if i != j
    }

    order = {
        i: model.add_variable(f'order_{i}', lowBound=1, upBound=n - 1)
        for i in range(1, n)
    }

    # calculate total distance
    model += pulp.lpSum(distance_matrix[i][j] * x[i, j] for i, j in x)

    # constraint 1: one outgoing edge
    for i in range(n):
        model += pulp.lpSum(x[i, j] for j in range(n) if i != j) == 1
    
    # constraint 2: one incoming edge
    for j in range(n):
        model += pulp.lpSum(x[i, j] for i in range(n) if i != j) == 1

    # MTZ subtour elimination to exclude subtours that do not include the depot
    for i in range(1, n):
        for j in range(1, n):
            if i != j:
                model += order[i] - order[j] + n * x[i, j] <= n - 1

    stats = model.solve(pulp.COIN_CMD(msg=False))
    if not stats.has_solution:
        raise RuntimeError(f'TSP optimization failed: {stats.status_str}')

    successors = {}
    for (i, j), variable in x.items():
        value = pulp.value(variable)
        if value is None:
            raise RuntimeError(f'No solution value for edge ({i}, {j})')
        if value > 0.5:
            successors[i] = j

    # convert successor map into route (list)
    # {0:1, 1:2, 2:3, 3:0} becomes [0, 1, 2, 3, 0]
    route = [0]
    current = 0
    while len(route) < n:
        current = successors[current]
        route.append(current)

    # back to depot
    route.append(0)

    total_distance = pulp.value(model.objective)
    if total_distance is None:
        raise RuntimeError('No objective value returned for the TSP solution')
    return route, total_distance