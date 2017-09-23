from flask import Flask, request, jsonify
import train_planner
import release_schedule
import json
import stringcompression
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/releaseSchedule', methods=['POST'])
def release_schedule_endpoint():
    parsed_json = request.get_json()
    print("RELEASE SCHEDULE")
    print(request.data)
    num_tasks, it_start, it_finish, tasks = release_schedule.parse_input(parsed_json)
    longest_gap = release_schedule.find_longest_gap(num_tasks, it_start, it_finish, tasks)
    return '"{}"'.format(longest_gap)


@app.route('/trainPlanner', methods=['POST'])
def train_planner_endpoint():
    print(request.data)
    json_str = request.get_json()
    print(json_str)
    destination, stations = train_planner.parse_input(json_str)
    line, num_passengers, station = train_planner.plan(destination, stations)
    answer = {'line': line, 'totalNumOfPassengers': num_passengers, 'reachingVia': station}
    return jsonify(answer)

@app.route('/stringcompression/RLE', methods=['POST'])
def str_RLE():
	data = request.get_json()
	inp = data.get('data')
	output = stringcompression.RLE2(inp)
	return jsonify(output)

@app.route('/stringcompression/LZW', methods=['POST'])
def str_LZW():
	data = request.get_json()
	inp = data.get('data')
	output = stringcompression.LZW(inp)
	return jsonify(output)

@app.route('/stringcompression/WDE', methods=['POST'])
def str_WDE():
	data = request.get_json()
	inp = data.get('data')
	output = stringcompression.WDE(inp)
	return jsonify(output)

if __name__ == '__main__':
    app.run()
