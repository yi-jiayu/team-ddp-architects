from flask import Flask, request, jsonify
import train_planner
import release_schedule
import json
import stringcompression
import jewellery_heist
import sorting
import emptyarea
import sorting
import requests
import warehouse_keeper_2 as warehouse_keeper
import horse_racing

import multiprocessing
import sorting
import emptyarea
import sorting
import requests
import warehouse_keeper
import horse_racing

import multiprocessing

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
    print("RLE: {}".format(request.data))
    data = request.get_json()
    inp = data.get('data')
    output = stringcompression.RLE2(inp)
    return jsonify(output)


@app.route('/stringcompression/LZW', methods=['POST'])
def str_LZW():
    print("LZW: {}".format(request.data))
    data = request.get_json()
    inp = data.get('data')
    output = stringcompression.LZW(inp)
    return jsonify(output)


@app.route('/stringcompression/WDE', methods=['POST'])
def str_WDE():
    print("WDE: {}".format(request.data))
    data = request.get_json()
    inp = data.get('data')
    output = stringcompression.WDE(inp)
    return jsonify(output)


@app.route('/heist', methods=['POST'])
def heist():
    print('heist: {}'.format(request.data))
    data = request.get_json()
    maxweight = data.get('maxWeight')
    vault = data.get('vault')
    output = jewellery_heist.solve(maxweight, vault)
    return jsonify(output)


@app.route('/horse-racing', methods=['POST'])
def racing():
    print('horse_racing:{}'.format(request.data))
    inp3 = request.get_json().get("data")
    output = horse_racing.solve(inp3)
    return jsonify(output)


@app.route('/horse-racing', methods=['POST'])
def racing():
    print('horse_racing:{}'.format(request.data))
    inp3 = request.get_json().get("data")
    output = horse_racing.solve(inp3)
    return jsonify(output)

@app.route('/sort', methods=['POST'])
def sort():
    print(request.data)
    return jsonify(request.get_json())
    # data = request.get_json()
    # # output = sorted(data) #13 passed python sorted uses timsort
    # # output = sorting.quickSort(data) #12 passed
    # # output = sorting.heapsort(data) #13 passed
    # # data.sort() #13 passed, one timed out
    # # output = sorting.qsort(data)
    # output = sorting.numpyy(data).tolist()
    # return jsonify(output)


@app.route('/calculateemptyarea', methods=['POST'])
def calcemptyarea():
    print('calcempty:{}'.format(request.data))
    data = request.get_json()
    output = emptyarea.calcArea(data)
    # output = sorted(data) #13 passed python sorted uses timsort
    # output = sorting.quickSort(data) #12 passed
    # output = sorting.heapsort(data) #13 passed
    # data.sort() #13 passed, one timed out
    # output = sorting.qsort(data)
    output = sorting.numpyy(data).tolist()
    return jsonify(output)


@app.route('/warehouse-keeper/game-start', methods=['POST'])
def warehouse_start():
    start = request.get_json()
    print(start)
    run_id = start['run_id']
    first_map = start['map']

    p = multiprocessing.Process(target=warehouse_keeper.solve_async, args=(run_id, first_map))
    p.start()

    return


@app.route('/calculateemptyarea',methods=['POST'])
def calcemptyarea():
    print('calcempty:{}'.format(request.data))
    data = request.get_json()
    output = emptyarea.calcArea(data)
    return jsonify(output)


@app.route('/warehouse-keeper/game-start', methods=['POST'])
def warehouse_start():
    start = request.get_json()
    print(start)
    run_id = start['run_id']
    first_map = start['map']

    p = multiprocessing.Process(target=warehouse_keeper.solve_async, args=(run_id, first_map))
    p.start()

    return



if __name__ == '__main__':
    app.run(debug=True)
