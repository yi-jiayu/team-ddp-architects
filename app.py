from flask import Flask, request, jsonify
import train_planner
import release_schedule
import json

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/releaseSchedule', methods=['POST'])
def release_schedule_endpoint():
    parsed_json = request.get_json()
    num_tasks, it_start, it_finish, tasks = release_schedule.parse_input(parsed_json)
    longest_gap = release_schedule.find_longest_gap(num_tasks, it_start, it_finish, tasks)
    return str(longest_gap)


@app.route('/trainPlanner', methods=['POST'])
def train_planner_endpoint():
    print(request.data)
    json_str = request.get_json()
    print(json_str)
    destination, stations = train_planner.parse_input(json_str)
    line, num_passengers, station = train_planner.plan(destination, stations)
    answer = {'line': line, 'totalNumOfPassengers': num_passengers, 'reachingVia': station}
    return jsonify(json.dumps(answer))


if __name__ == '__main__':
    app.run()
