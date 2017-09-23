from flask import Flask, request, jsonify
import train_planner
import json
import stringcompression
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/trainPlanner', methods=['POST'])
def train_planner_endpoint():
    json_str = request.get_json()
    destination, stations = train_planner.parse_input(json_str)
    line, num_passengers, station = train_planner.plan(destination, stations)
    answer = {'line': line, 'totalNumOfPassengers': num_passengers, 'reachingVia': station}
    return jsonify(json.dumps(answer))

@app.route('/stringcompression/RLE', methods=['POST'])
def str_RLE():
	data = request.get_json()
	inp = data.get('data')
	output = RLE(inp)
	return jsonify(output)

@app.route('/stringcompression/LZW', methods=['POST'])
def str_LZW():
	data = request.get_json()
	inp = data.get('data')
	output = LZW(inp)
	return jsonify(output)

@app.route('/stringcompression/LZW', methods=['POST'])
def str_WDE():
	data = request.get_json()
	inp = data.get('data')
	output = WDE(inp)
	return jsonify(output)

if __name__ == '__main__':
    app.run()
