from collections import deque
import heapq


def bfs(graph, start, goal):
    """Breadth-First Search: expand cities by number of connections."""
    if start not in graph or goal not in graph:
        raise ValueError("Start or goal is not in the graph.")

    queue = deque([(start, [start], 0.0)])
    visited = {start}
    expanded = []

    while queue:
        city, path, distance = queue.popleft()
        expanded.append(city)

        if city == goal:
            return {
                "path": path,
                "expanded": expanded,
                "distance": round(distance, 2),
            }

        for neighbor in sorted(graph[city]):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((
                    neighbor,
                    path + [neighbor],
                    distance + graph[city][neighbor],
                ))

    return {"path": None, "expanded": expanded, "distance": 0.0}


def dfs(graph, start, goal):
    """Depth-First Search: follow a branch before backtracking."""
    if start not in graph or goal not in graph:
        raise ValueError("Start or goal is not in the graph.")

    stack = [(start, [start], 0.0)]
    visited = set()
    expanded = []

    while stack:
        city, path, distance = stack.pop()

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

        # Stack pops the last item first, so add neighbors in reverse order.
        for neighbor in sorted(graph[city], reverse=True):
            if neighbor not in visited:
                stack.append((
                    neighbor,
                    path + [neighbor],
                    distance + graph[city][neighbor],
                ))

    return {"path": None, "expanded": expanded, "distance": 0.0}


def ucs(graph, start, goal):
    """Uniform-Cost Search: expand the lowest-cost path next."""
    if start not in graph or goal not in graph:
        raise ValueError("Start or goal is not in the graph.")

    # Each entry is (total_distance, insertion_order, city, path).
    frontier = [(0.0, 0, start, [start])]
    counter = 0
    visited = set()
    expanded = []

    while frontier:
        distance, _, city, path = heapq.heappop(frontier)

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
                heapq.heappush(
                    frontier,
                    (
                        distance + graph[city][neighbor],
                        counter,
                        neighbor,
                        path + [neighbor],
                    ),
                )

    return {"path": None, "expanded": expanded, "distance": 0.0}


def ids(graph, start, goal):
    """Iterative Deepening Search: repeat DFS with increasing depth limits."""
    if start not in graph or goal not in graph:
        raise ValueError("Start or goal is not in the graph.")

    expanded = []

    def depth_limited_search(city, path, distance, remaining_depth):
        expanded.append(city)

        if city == goal:
            return path, distance

        if remaining_depth == 0:
            return None

        for neighbor in sorted(graph[city]):
            # Avoid cycles within the current path.
            if neighbor not in path:
                result = depth_limited_search(
                    neighbor,
                    path + [neighbor],
                    distance + graph[city][neighbor],
                    remaining_depth - 1,
                )
                if result is not None:
                    return result

        return None

    # A simple path cannot contain more than len(graph) - 1 edges.
    for depth_limit in range(len(graph)):
        result = depth_limited_search(start, [start], 0.0, depth_limit)

        if result is not None:
            path, distance = result
            return {
                "path": path,
                "expanded": expanded,
                "distance": round(distance, 2),
            }

    return {"path": None, "expanded": expanded, "distance": 0.0}