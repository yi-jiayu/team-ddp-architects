import json
from collections import namedtuple, deque

Station = namedtuple('Station', ['name', 'passengers', 'neighbours'])
Connection = namedtuple('Connection', ['name', 'line'])


def parse_input(json_str: str):
    inp = json.loads(json_str)
    destination = inp['destination']

    stations = {}
    for station in inp['stations']:
        name, passengers = station['name'], station['passengers']

        neighbours = []
        for conn in station['connections']:
            nname, line = conn['station'], conn['line']
            neighbours.append(Connection(nname, line))

        stations[name] = Station(name, passengers, neighbours)

    return destination, stations


def train_planner(destination, stations):
    passengers_via = {}
    queue = deque()
    visited = {destination}

    for neighbour in stations[destination].neighbours:
        passengers_via[(neighbour.name, neighbour.line)] = 0
        queue.appendleft(((neighbour.name, neighbour.line), neighbour.name))

    while queue:
        via, curr = queue.pop()

        if curr in visited:
            continue

        passengers_via[via] += stations[curr].passengers

        visited.add(curr)

        for neighbour in stations[curr].neighbours:
            if neighbour.name not in visited:
                queue.appendleft((via, neighbour.name))

    via, num_passengers = sorted(passengers_via.items(), key=lambda x: x[1], reverse=True)[0]
    station, line = via

    return line, num_passengers, station


if __name__ == '__main__':
    test_input = """{
  "destination": "DhobyGhaut",
  "stations": [
    {
      "name": "Punggol",
      "passengers": 80,
      "connections": [
        {
          "station": "Sengkang",
          "line": "purple"
        }
      ]
    },
    {
      "name": "Sengkang",
      "passengers": 40,
      "connections": [
        {
          "station": "Punggol",
          "line": "purple"
        },
        {
          "station": "Serangoon",
          "line": "purple"
        }
      ]
    },
    {
      "name": "Serangoon",
      "passengers": 40,
      "connections": [
        {
          "station": "LittleIndia",
          "line": "purple"
        },
        {
          "station": "Sengkang",
          "line": "purple"
        },
        {
          "station": "PayaLebar",
          "line": "orange"
        },
        {
          "station": "Bishan",
          "line": "orange"
        }
      ]
    },
    {
      "name": "LittleIndia",
      "passengers": 40,
      "connections": [
        {
          "station": "Serangoon",
          "line": "purple"
        },
        {
          "station": "DhobyGhaut",
          "line": "purple"
        }
      ]
    },
    {
      "name": "DhobyGhaut",
      "passengers": 20,
      "connections": [
        {
          "station": "LittleIndia",
          "line": "purple"
        },
        {
          "station": "HarbourFront",
          "line": "purple"
        },
        {
          "station": "Somerset",
          "line": "red"
        },
        {
          "station": "MarinaBay",
          "line": "red"
        },
        {
          "station": "Esplanade",
          "line": "orange"
        }
      ]
    },
    {
      "name": "HarbourFront",
      "passengers": 90,
      "connections": [
        {
          "station": "DhobyGhaut",
          "line": "purple"
        }
      ]
    },
    {
      "name": "Somerset",
      "passengers": 0,
      "connections": [
        {
          "station": "DhobyGhaut",
          "line": "red"
        },
        {
          "station": "Orchard",
          "line": "red"
        }
      ]
    },
    {
      "name": "Orchard",
      "passengers": 30,
      "connections": [
        {
          "station": "Somerset",
          "line": "red"
        },
        {
          "station": "Novena",
          "line": "red"
        }
      ]
    },
    {
      "name": "Novena",
      "passengers": 10,
      "connections": [
        {
          "station": "Orchard",
          "line": "red"
        },
        {
          "station": "Bishan",
          "line": "red"
        }
      ]
    },
    {
      "name": "Bishan",
      "passengers": 20,
      "connections": [
        {
          "station": "Novena",
          "line": "red"
        },
        {
          "station": "Woodlands",
          "line": "red"
        },
        {
          "station": "Serangoon",
          "line": "orange"
        }
      ]
    },
    {
      "name": "Woodlands",
      "passengers": 40,
      "connections": [
        {
          "station": "Bishan",
          "line": "red"
        }
      ]
    },
    {
      "name": "MarinaBay",
      "passengers": 100,
      "connections": [
        {
          "station": "DhobyGhaut",
          "line": "red"
        }
      ]
    },
    {
      "name": "Esplanade",
      "passengers": 0,
      "connections": [
        {
          "station": "DhobyGhaut",
          "line": "orange"
        },
        {
          "station": "PayaLebar",
          "line": "orange"
        }
      ]
    },
    {
      "name": "PayaLebar",
      "passengers": 75,
      "connections": [
        {
          "station": "Esplanade",
          "line": "orange"
        },
        {
          "station": "Serangoon",
          "line": "orange"
        }
      ]
    }
  ]
}"""

    destination, stations = parse_input(test_input)

    print(train_planner(destination, stations))
