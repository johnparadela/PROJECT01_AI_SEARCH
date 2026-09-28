import json
import os

from flask import Flask, jsonify, render_template, request

from uninformed import bfs, dfs, ucs, ids
from informed import greedy_best_first, a_star


app = Flask(__name__)
MAP_DATA_FILE = "map_data.json"

ALGORITHMS = {
    "bfs": bfs,
    "dfs": dfs,
    "ucs": ucs,
    "ids": ids,
    "greedy": greedy_best_first,
    "astar": a_star,
}


def load_map_data():
    """Read the generated Southern California graph."""
    with open(MAP_DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


@app.route("/")
def index():
    """Display the map interface."""
    return render_template("index.html")


@app.route("/api/map", methods=["GET"])
def get_map():
    """Send locations and connections to the map interface."""
    return jsonify(load_map_data())


@app.route("/api/search", methods=["POST"])
def search():
    """Run the algorithm selected in the map interface."""
    payload = request.get_json(silent=True) or {}

    start = payload.get("start")
    goal = payload.get("goal")
    algorithm = payload.get("algorithm")

    if algorithm not in ALGORITHMS:
        return jsonify({"message": "Select a valid search algorithm."}), 400

    map_data = load_map_data()
    graph = map_data["graph"]

    if start not in graph or goal not in graph:
        return jsonify({"message": "Select valid start and goal cities."}), 400

    search_function = ALGORITHMS[algorithm]

    # Greedy and A* need coordinates as well as connections.
    if algorithm in ("greedy", "astar"):
        result = search_function(map_data, start, goal)
    else:
        result = search_function(graph, start, goal)

    path = result["path"] or []

    return jsonify({
        "path": path,
        "cost": result["distance"] if path else None,
        "nodes_expanded": len(result["expanded"]),
        "expanded": result["expanded"],
        "message": "Path found." if path else "No path found.",
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)