from flask import Flask, request, jsonify
import train_planner
import json

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/trainPlanner', methods=['POST'])
def train_planner_endpoint():
    json_str = request.get_json()
    print(json_str)
    destination, stations = train_planner.parse_input(json_str)
    line, num_passengers, station = train_planner.plan(destination, stations)
    answer = {'line': line, 'totalNumOfPassengers': num_passengers, 'reachingVia': station}
    return jsonify(json.dumps(answer))


if __name__ == '__main__':
    app.run()
