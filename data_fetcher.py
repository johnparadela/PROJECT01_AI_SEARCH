"""
Author: John Paradela
Class: CS 411 

data_fetcher.py
================
Builds a connected road-network graph for Southern California.
Uses:
  - Nominatim OpenStreetMap API for geocoding (coordinates)
  - OSRM Routing API for road driving distances

Saves the resulting graph to map_data.json.
""" 

import json
import math
import time
import requests



# Region: Southern California locations
REGION_NAME = "Southern California: Los Angeles and Orange counties"

CITIES = [
    "Los Angeles, CA",
    "Santa Monica, CA",
    "Culver City, CA",
    "Beverly Hills, CA",
    "West Hollywood, CA",
    "Burbank, CA",
    "Glendale, CA",
    "Pasadena, CA",
    "Alhambra, CA",
    "Monterey Park, CA",
    "Long Beach, CA",
    "Torrance, CA",
    "Carson, CA",
    "Compton, CA",
    "Inglewood, CA",
    "Anaheim, CA",
    "Fullerton, CA",
    "Santa Ana, CA",
    "Irvine, CA",
    "Huntington Beach, CA",
]

ROAD_CONNECTIONS = [
    ("Los Angeles, CA", "West Hollywood, CA"),
    ("West Hollywood, CA", "Beverly Hills, CA"),
    ("Beverly Hills, CA", "Santa Monica, CA"),
    ("Santa Monica, CA", "Culver City, CA"),
    ("Culver City, CA", "Inglewood, CA"),
    ("Inglewood, CA", "Los Angeles, CA"),
    ("Los Angeles, CA", "Glendale, CA"),
    ("Glendale, CA", "Burbank, CA"),
    ("Glendale, CA", "Pasadena, CA"),
    ("Pasadena, CA", "Alhambra, CA"),
    ("Alhambra, CA", "Monterey Park, CA"),
    ("Monterey Park, CA", "Los Angeles, CA"),
    ("Los Angeles, CA", "Pasadena, CA"),
    ("Los Angeles, CA", "Compton, CA"),
    ("Compton, CA", "Carson, CA"),
    ("Compton, CA", "Long Beach, CA"),
    ("Carson, CA", "Torrance, CA"),
    ("Torrance, CA", "Inglewood, CA"),
    ("Carson, CA", "Long Beach, CA"),
    ("Long Beach, CA", "Huntington Beach, CA"),
    ("Huntington Beach, CA", "Irvine, CA"),
    ("Irvine, CA", "Santa Ana, CA"),
    ("Santa Ana, CA", "Anaheim, CA"),
    ("Anaheim, CA", "Fullerton, CA"),
    ("Fullerton, CA", "Pasadena, CA"),
    ("Fullerton, CA", "Monterey Park, CA"),
    ("Anaheim, CA", "Long Beach, CA"),
]

USER_AGENT = "UIC-CS411-Search-Visualizer/1.0 (jpara3@uic.edu)"


def haversine_distance(coord1, coord2):
    """
    Calculate straight-line distance in miles.
    Coordinates are given as: latitude, longitude.
    """
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    earth_radius_miles = 3958.8

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return round(earth_radius_miles * c, 2)    


def fetch_coordinates(city_name):
    """Fetch a city's latitude and longitude from Nominatim."""
    url = "https://nominatim.openstreetmap.org/search"

    params = {
        "q": city_name, "format": "json", "limit": 1,
    }

    headers = {"User-Agent": USER_AGENT}

    response = requests.get(url, params=params, headers=headers, timeout=10)
    response.raise_for_status()

    results = response.json()
    if not results:
        raise ValueError(f"Nominatim could not find {city_name}")
    
    return {
        "lat": float(results[0]["lat"]),
        "lon": float(results[0]["lon"]),
    }


def fetch_road_distance(coord1, coord2):
    """
    Fetch driving distance in miles from OSRM.
    Coordinates are given as: latitude, longitude.
    """
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    url = ("https://router.project-osrm.org/route/v1/driving/"f"{lon1},{lat1};{lon2},{lat2}")

    response = requests.get(url, params={"overview": "false"}, timeout=10)
    response.raise_for_status()

    data = response.json()
    if data.get("code") != "Ok" or not data.get("routes"):
        raise ValueError(f"OSRM could not find a driving route: {data}")

    distance_meters = data["routes"][0]["distance"]
    distance_miles = distance_meters * 0.000621371
    return round(distance_miles, 2)


def build_graph():
    """Build the road graph and save it to map_data.json."""

    print(f"Building map graph for: {REGION_NAME}")
    print(f"Total cities to geocode: {len(CITIES)}")

    #city coordinates.
    locations = {}

    for index, city in enumerate(CITIES, start=1):
        print(f"[{index}/{len(CITIES)}] Geocoding: {city}")
        locations[city] = fetch_coordinates(city)

        # Limit requests to Nominatim's public service.
        time.sleep(1.1)

    #road distances and create the adjacency list.
    graph = {city: {} for city in CITIES}
    total_edges = 0

    print(f"\nFetching {len(ROAD_CONNECTIONS)} road connections...")

    for city_a, city_b in ROAD_CONNECTIONS:
        if city_a not in locations or city_b not in locations:
            raise ValueError(
                f"Connection references an unknown city: "
                f"{city_a}, {city_b}"
            )

        coord_a = (
            locations[city_a]["lat"],
            locations[city_a]["lon"],
        )
        coord_b = (
            locations[city_b]["lat"],
            locations[city_b]["lon"],
        )

        distance = fetch_road_distance(coord_a, coord_b)

        graph[city_a][city_b] = distance
        graph[city_b][city_a] = distance
        total_edges += 1

        print(f"  {city_a} <--> {city_b}: {distance} miles")
        time.sleep(0.2)

    # Save data in the format used by the deployment starter.
    map_data = {
        "region": REGION_NAME,
        "total_cities": len(locations),
        "total_edges": total_edges,
        "locations": locations,
        "graph": graph,
    }

    with open("map_data.json", "w", encoding="utf-8") as file:
        json.dump(map_data, file, indent=2)

    print("\nGraph construction complete!")
    print(f"Saved {len(locations)} cities and {total_edges} connections.")
    print("Output file: map_data.json")


if __name__ == "__main__":
    build_graph()