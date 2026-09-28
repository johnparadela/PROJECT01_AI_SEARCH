import math
import heapq


def haversine(coord1, coord2):
    """Calculate straight-line distance in miles between two coordinates."""
    earth_radius_miles = 3958.8

    lat1 = math.radians(coord1["lat"])
    lon1 = math.radians(coord1["lon"])
    lat2 = math.radians(coord2["lat"])
    lon2 = math.radians(coord2["lon"])

    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1

    a = (
        math.sin(delta_lat / 2) ** 2
        + math.cos(lat1)
        * math.cos(lat2)
        * math.sin(delta_lon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return earth_radius_miles * c


def greedy_best_first(map_data, start, goal):
    """
    Greedy Best-First Search.
    Selects the city with the smallest straight-line distance to the goal.
    """
    locations = map_data["locations"]
    graph = map_data["graph"]

    if start not in graph or goal not in graph:
        return {"path": None, "expanded": [], "distance": 0.0}

    goal_coord = locations[goal]

    # Entry: (heuristic, insertion_order, city, path, path_distance)
    frontier = []
    counter = 0
    start_h = haversine(locations[start], goal_coord)
    heapq.heappush(frontier, (start_h, counter, start, [start], 0.0))

    visited = set()
    expanded = []

    while frontier:
        _, _, city, path, distance = heapq.heappop(frontier)

        if city in visited:
            continue

        visited.add(city)
        expanded.append(city)

        if city == goal:
            return {
                "path": path,
                "expanded": expanded,
                "distance": round(distance, 2),
            }

        for neighbor in sorted(graph[city]):
            if neighbor not in visited:
                counter += 1
                new_distance = distance + graph[city][neighbor]
                heuristic = haversine(locations[neighbor], goal_coord)

                heapq.heappush(
                    frontier,
                    (
                        heuristic,
                        counter,
                        neighbor,
                        path + [neighbor],
                        new_distance,
                    ),
                )

    return {"path": None, "expanded": expanded, "distance": 0.0}


def a_star(map_data, start, goal):
    """
    A* Search.
    Selects the city with the smallest g(n) + h(n):
    road distance so far + straight-line distance to the goal.
    """
    locations = map_data["locations"]
    graph = map_data["graph"]

    if start not in graph or goal not in graph:
        return {"path": None, "expanded": [], "distance": 0.0}

    goal_coord = locations[goal]

    # Entry: (estimated_total, insertion_order, city, path, distance_so_far)
    frontier = []
    counter = 0
    start_h = haversine(locations[start], goal_coord)
    heapq.heappush(frontier, (start_h, counter, start, [start], 0.0))

    best_distance = {start: 0.0}
    expanded = []

    while frontier:
        _, _, city, path, distance_so_far = heapq.heappop(frontier)

        # Skip an older, more expensive route to this city.
        if distance_so_far > best_distance[city]:
            continue

        expanded.append(city)

        if city == goal:
            return {
                "path": path,
                "expanded": expanded,
                "distance": round(distance_so_far, 2),
            }

        for neighbor in sorted(graph[city]):
            new_distance = distance_so_far + graph[city][neighbor]

            if new_distance < best_distance.get(neighbor, float("inf")):
                best_distance[neighbor] = new_distance
                counter += 1

                heuristic = haversine(locations[neighbor], goal_coord)
                estimated_total = new_distance + heuristic

                heapq.heappush(
                    frontier,
                    (
                        estimated_total,
                        counter,
                        neighbor,
                        path + [neighbor],
                        new_distance,
                    ),
                )

    return {"path": None, "expanded": expanded, "distance": 0.0}