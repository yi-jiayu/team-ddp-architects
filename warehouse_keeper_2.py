import requests

solver_endpoint = 'http://localhost:5001'


def preprocess(map_):
    map_ = [row.replace('x', '#').replace('-', '#').replace('o', '$').replace('*', '.').replace('b', '@') for row in
            map_]
    return map_


def solve(map_):
    map_ = preprocess(map_)
    r = requests.post(solver_endpoint, '\n'.join(map_))
    return r.text.strip()


def solve_one_map(run_id, solution: str):
    solution = solution.lower()
    print(solution)
    for c in solution:
        if c == 'u':
            direction = 'up'
        elif c == 'd':
            direction = 'down'
        elif c == 'l':
            direction = 'left'
        elif c == 'r':
            direction = 'right'

        print(direction)

        resp = requests.post(
            'https://cis2017-warehouse-keeper.herokuapp.com/move/{}?run_id={}'.format(direction, run_id))
        resp_data = resp.json()
        print(resp_data)
        if resp_data['win']:
            if 'next_map' not in resp_data:
                return True, None
            else:
                next_map = resp_data['next_map']
                return False, next_map


def solve_async(run_id, first_map):
    map_ = first_map
    done = False
    while not done:
        soln = solve(map_)
        done, next_map = solve_one_map(run_id, soln)
        map_ = next_map


if __name__ == '__main__':
    # map1 = ["xx---xxx",
    #         "xx-*-xxx",
    #         "xx- ----",
    #         "---o o*-",
    #         "-*ob  --",
    #         "----o --",
    #         "xxx-*-xx",
    #         "xxx---xx"]
    #
    # print(solve(map1))

    solve_async('ba1696f4-07ce-41a7-80aa-46b20578d7ea',
                ['xx---xxx', 'xx-*-xxx', 'xx- ----', '---o o*-', '-*ob  --', '----o --', 'xxx-*-xx', 'xxx---xx'])
