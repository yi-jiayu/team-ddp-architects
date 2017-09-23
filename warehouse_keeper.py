from queue import PriorityQueue
from copy import deepcopy
from collections import deque
import requests


def clean_map(map_):
    return [list(row.replace('-', 'x').replace('*', ' ')) for row in map_]


def find_keeper(map_):
    for r, row in enumerate(map_):
        for c, col in enumerate(row):
            if col == 'b':
                return r, c


def find_targets(map_):
    for r, row in enumerate(map_):
        for c, col in enumerate(row):
            if col == '*':
                yield (r, c)


def find_boxes(map_):
    for r, row in enumerate(map_):
        for c, col in enumerate(row):
            if col == 'o':
                yield (r, c)


def adjacent(map_, loc):
    r, c = loc
    if r > 0:
        if map_[r - 1][c] != 'x':
            yield (r - 1, c)

    if r < len(map_) - 1:
        if map_[r + 1][c] != 'x':
            yield (r + 1, c)

    if c > 0:
        if map_[r][c - 1] != 'x':
            yield (r, c - 1)

    if c < len(map_[0]) - 1:
        if map_[r][c + 1] != 'x':
            yield (r, c + 1)


def distances_from_target(map_, origin):
    distances = {}
    queue = deque([(origin, 0)])
    visited = set()

    while queue:
        pos, depth = queue.pop()
        distances[pos] = depth

        if pos in visited:
            continue
        visited.add(pos)

        for adj in adjacent(map_, pos):
            if adj not in visited:
                queue.appendleft((adj, depth + 1))

    return distances


def distances_from_nearest_target(map_):
    targets = (target for target in find_targets(map_))
    distances = [distances_from_target(map_, target) for target in targets]
    combined_distances = {loc: min(d[loc] for d in distances) for loc in distances[0].keys()}
    return combined_distances


def heuristic(map_, distances):
    return sum(distances[box] for box in find_boxes(map_))


def get_possible_moves(map_):
    r, c = find_keeper(map_)

    # move up into empty space
    if r > 0 and map_[r - 1][c] == ' ':
        next_state = deepcopy(map_)
        next_state[r][c] = ' '
        next_state[r - 1][c] = 'b'
        yield 'up', next_state

    # push box up into empty space
    if r > 1 and map_[r - 1][c] == 'o' and map_[r - 2][c] == ' ':
        next_state = deepcopy(map_)
        next_state[r][c] = ' '
        next_state[r - 1][c] = 'b'
        next_state[r - 2][c] = 'o'
        yield 'up', next_state

    if r < len(map_) - 1 and map_[r + 1][c] == ' ':
        next_state = deepcopy(map_)
        next_state[r][c] = ' '
        next_state[r + 1][c] = 'b'
        yield 'down', next_state

    if r < len(map_) - 2 and map_[r + 1][c] == 'o' and map_[r + 2][c] == ' ':
        next_state = deepcopy(map_)
        next_state[r][c] = ' '
        next_state[r + 1][c] = 'b'
        next_state[r + 2][c] = 'o'
        yield 'down', next_state

    if c > 0 and map_[r][c - 1] == ' ':
        next_state = deepcopy(map_)
        next_state[r][c] = ' '
        next_state[r][c - 1] = 'b'
        yield 'left', next_state

    if c > 1 and map_[r][c - 1] == 'o' and map_[r][c - 2] == ' ':
        next_state = deepcopy(map_)
        next_state[r][c] = ' '
        next_state[r][c - 1] = 'b'
        next_state[r][c - 2] = 'o'
        yield 'left', next_state

    if c < len(map_[0]) - 1 and map_[r][c + 1] == ' ':
        next_state = deepcopy(map_)
        next_state[r][c] = ' '
        next_state[r][c + 1] = 'b'
        yield 'right', next_state

    if c < len(map_[0]) - 2 and map_[r][c + 1] == 'o' and map_[r][c + 2] == ' ':
        next_state = deepcopy(map_)
        next_state[r][c] = ' '
        next_state[r][c + 1] = 'b'
        next_state[r][c + 2] = 'o'
        yield 'right', next_state


# distances = distances_from_nearest_target(map_)
# for direction, next_state in get_possible_moves(map_):
#     print(direction)
#     for row in next_state:
#         print(row)
#     print(h(next_state, distances))
#     print('\n')


def freeze_map(map_):
    s = ''
    for row in map_:
        s += ''.join(row)
    return s


def solve(map_):
    distances = distances_from_nearest_target(map_)
    stars = list(find_targets(map_))
    map_ = clean_map(map_)

    q = PriorityQueue()
    h_0 = heuristic(map_, distances)
    q.put((h_0, 0, h_0, map_, ()))
    visited = set()

    while not q.empty():
        f, g, h, state, actions = q.get()

        frozen = freeze_map(state)
        visited.add(frozen)

        if h == 0:
            return actions

        for direction, next_state in get_possible_moves(state):
            if freeze_map(next_state) not in visited:
                g_1 = g + 1
                h_1 = heuristic(next_state, distances)
                f_1 = g_1 + h_1
                new_actions = actions + (direction,)
                q.put((f_1, g_1, h_1, next_state, new_actions))

    return None


def solve_one_map(run_id, solution):
    for dir in solution:
        resp = requests.post('https://cis2017-warehouse-keeper.herokuapp.com/move/{}?run_id={}'.format(dir, run_id))
        resp_data = resp.json()
        print(resp_data)
        if resp_data['win']:
            if 'next_map' not in resp_data:
                return True, None
            else:
                map1 = resp_data['next_map']
                return False, map1


def solve_async(run_id, first_map):
    map_ = first_map
    done = False
    while not done:
        soln = solve(map_)
        done, next_map = solve_one_map(run_id, soln)
        map_ = next_map


if __name__ == '__main__':
    map_ = ["xx---xxx",
            "xx-*-xxx",
            "xx- ----",
            "---o o*-",
            "-*ob  --",
            "----o --",
            "xxx-*-xx",
            "xxx---xx"]

    print(solve(map_))

    map2 = ['-----xxxx',
            '-b  -xxxx',
            '- oo- ---',
            '- o - -*-',
            '--- ---*-',
            'x--    *-',
            'x-   -  -',
            'x-   ----',
            'x-----xxx']

    print(solve(map2))
