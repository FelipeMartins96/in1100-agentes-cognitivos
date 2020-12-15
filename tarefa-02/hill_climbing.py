from typing import Dict, List, Tuple
import matplotlib.pyplot as plt
import random
import math
import sys


def parse_tsp(file: str) -> Dict[int, Tuple[float, float]]:
    with open(file, "rt") as f:
        content = f.read()

    _, points = content.split("NODE_COORD_SECTION")

    cities = {}

    for point in points.strip().split("\n"):
        i, x, y = point.split(" ")
        cities[int(i) - 1] = (float(x), float(y))

    return cities


def get_initial_random_route(n_cities: int) -> List[int]:
    route = [i for i in range(n_cities)]
    random.shuffle(route)

    return route


def distance(pointA: Tuple[float, float], pointB: Tuple[float, float]):
    """Euclidean distance between two points"""

    distX = pointA[0] - pointB[0]
    distY = pointA[1] - pointB[1]

    return math.sqrt((distX ** 2 + distY ** 2))


def evaluate(cities: Dict[int, Tuple[float, float]], route: List[int]) -> float:

    cost = distance(cities[route[-1]], cities[route[0]])  # last to first
    for i in range(len(route) - 1):  # each city to the next one
        cost += distance(cities[route[i]], cities[route[i + 1]])

    return cost


def get_neighbors(route: List[int]) -> None:
    """Yields route neighbors from swapping consecutive cities in route"""

    for i in range(len(route) - 1):
        neighbor = route[:]
        neighbor[i], neighbor[i + 1] = route[i + 1], route[i]
        yield neighbor


def plot_result(
    cities: Dict[int, Tuple[float, float]],
    iteration: int,
    n_steps: int,
    initial_route: List[int],
    best_route: List[int],
    cost_history: List[float],
) -> None:
    """Plots a solution of the travelling salesman problem"""

    x_initial = [cities[city_idx][0]
                 for city_idx in initial_route]  # only x_initial
    y_initial = [cities[city_idx][1]
                 for city_idx in initial_route]  # only y_initial

    x_best = [cities[city_idx][0] for city_idx in best_route]  # only x_best
    y_best = [cities[city_idx][1] for city_idx in best_route]  # only y_best

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
    fig.set_figheight(6)
    fig.set_figwidth(13)
    fig.suptitle(
        f"Iteration {iteration} Solution, Reached in {n_steps} steps", fontsize=14, fontweight="bold")

    # ax1 = fig.add_subplot(121)
    # seems like x_initial and y_initial are inverted
    ax1.plot(y_initial + [y_initial[0]], x_initial + [x_initial[0]], linewidth=0.3, marker=".", color="k")

    # ax2 = fig.add_subplot(122)
    ax2.plot(cost_history, linewidth=0.3, marker=".", color="k")

    # ax3 = fig.add_subplot(12)
    # seems like x_best and y_best are inverted
    ax3.plot(y_best + [y_best[0]], x_best + [x_best[0]], linewidth=0.3, marker=".", color="k")

    plt.show()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage python hill_climbing.py filename.tsp")
        raise Exception

    cities: Dict[int, Tuple[float, float]] = parse_tsp(sys.argv[1])

    for i in range(10):
        initial_route: List[int] = get_initial_random_route(len(cities))
        best_route: List[int] = initial_route
        best_cost: float = evaluate(cities, best_route)

        cost_history: List[float] = [best_cost]

        improved: bool = True
        steps: int = 0
        while improved:
            steps += 1
            improved = False
            last_route = best_route

            for neighbor in get_neighbors(last_route):
                neighbor_cost = evaluate(cities, neighbor)
                if neighbor_cost < best_cost:  # if it improves, replace the best
                    best_route, best_cost = neighbor, neighbor_cost
                    improved = True

            if improved:
                cost_history.append(best_cost)
        plot_result(cities, i + 1, steps, initial_route, best_route, cost_history)

