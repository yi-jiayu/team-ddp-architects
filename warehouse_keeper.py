from queue import PriorityQueue
from copy import deepcopy
from collections import deque
import requests
from munkres import Munkres


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


def adjacent(map_, loc, walls=('x',)):
    r, c = loc

    # up open
    if r > 0:
        if map_[r - 1][c] not in walls:
            yield (r - 1, c)

    # left open
    if c > 0:
        if map_[r][c - 1] not in walls:
            yield (r, c - 1)

    # down open
    if r < len(map_) - 1:
        if map_[r + 1][c] not in walls:
            yield (r + 1, c)

    # right open
    if c < len(map_[0]) - 1:
        if map_[r][c + 1] not in walls:
            yield (r, c + 1)


def accessible_player_positions(state):
    pos = find_keeper(state)
    q = deque((pos,))
    visited = set()

    while q:
        curr = q.pop()
        visited.add(curr)

        for adj in adjacent(state, curr, ('x', 'o')):
            if adj not in visited:
                q.appendleft(adj)

    return visited


def opposite(origin, beside):
    r1, c1 = origin
    r2, c2 = beside

    if r1 == r2:
        if c1 > c2:
            return r1, c1 - 1
        else:
            return r1, c1 + 1
    else:
        if r1 > r2:
            return r1 + 1, c1
        else:
            return r1 - 1, c1


def possible_pushes(state, accessible_locations):
    for r, c in find_boxes(state):
        # push down
        if r > 0 and state[r-1][c] in accessible_locations and state[r+1][c] != 'x':
            next_state = deepcopy(state)
            next_state[r][c] = 'b'
            next_state[r+1][c] = 'o'
            yield 'down', next_state

        # push up
        if r < len(state) - 1 and state[r+1][c] in accessible_locations and state[r-1][c] != 'x':
            next_state = deepcopy(state)
            next_state[r][c] = 'b'
            next_state[r - 1][c] = 'o'
            yield 'up', next_state

        # push right
        if c > 0 and state[r][c-1] in accessible_locations and state[r][c+1] != 'x':
            next_state = deepcopy(state)
            next_state[r][c] = 'b'
            next_state[r][c+1] = 'o'
            yield 'right', next_state

        # push left
        if c < len(state[0]) - 1 and state[r][c+1] in accessible_locations and state[r][c-1] != 'x':
            next_state = deepcopy(state)
            next_state[r][c] = 'b'
            next_state[r][c-1] = 'o'
            yield 'left', next_state


def normalised_player_position(accessible_locations):
    max_r = max(p[0] for p in accessible_locations)
    max_c = max(p[1] for p in accessible_locations if p[0] == max_r)

    return max_r, max_c


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


def heuristic(map_, depth_maps):
    boxes = list(find_boxes(map_))
    cost_matrix = [[dm[b] for dm in depth_maps] for b in boxes]
    m = Munkres()
    indexes = m.compute(cost_matrix)
    return sum(cost_matrix[r][c] for r, c in indexes)


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


def check_for_dead_positions(state, stars):
    """Returns true if any stone is in a dead position which is not a target."""

    stones = find_boxes(state)
    for r, c in stones:
        if (r, c) not in stars:
            adj = list(adjacent(state, (r, c)))
            if len(adj) == 1:
                return True
            elif len(adj) == 2 and adj[0][0] != adj[1][0] and adj[0][1] != adj[1][1]:
                for row in state:
                    print(row)
                return True
    return False


def freeze_map(state, accessible_locations):
    """States are considered equivalent when all the stone positions and the top-right accessible location by the
    player is the same. """
    s = frozenset(find_boxes(state))
    return normalised_player_position(accessible_locations), s


def solve(map_):
    targets = find_targets(map_)
    depth_maps = [distances_from_target(map_, t) for t in targets]

    map_ = clean_map(map_)
    h_0 = heuristic(map_, depth_maps)

    max_depth = h_0
    while True:
        q = PriorityQueue()
        q.put((h_0, 0, h_0, map_, ()))
        visited = set()

        while not q.empty():
            f, g, h, state, actions = q.get()

            accessible_locations = accessible_player_positions(state)
            frozen = freeze_map(accessible_locations)
            visited.add(frozen)

            if h == 0:
                return actions

            for direction, next_state in possible_pushes(state, accessible_locations):
                if freeze_map(next_state) not in visited:
                    g_1 = g + 1

                    # ids
                    if g_1 > max_depth:
                        continue

                    # if check_for_dead_positions(next_state, targets):
                    #     continue

                    h_1 = heuristic(next_state, depth_maps)
                    f_1 = g_1 + h_1
                    new_actions = actions + (direction,)
                    q.put((f_1, g_1, h_1, next_state, new_actions))

        max_depth += 1


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
    map1 = ["xx---xxx",
            "xx-*-xxx",
            "xx- ----",
            "---o o*-",
            "-*ob  --",
            "----o --",
            "xxx-*-xx",
            "xxx---xx"]

    print(solve(map1))

    # map1 = clean_map(map1)
    # print(normalised_player_position(map1))

    # map2 = ['-----xxxx',
    #         '-b  -xxxx',
    #         '- oo- ---',
    #         '- o - -*-',
    #         '--- ---*-',
    #         'x--    *-',
    #         'x-   -  -',
    #         'x-   ----',
    #         'x-----xxx']
    #
    # print(solve(map2))
    #
    # map3 = ['----------',
    #         '-**      -',
    #         '-**o  -  -',
    #         '-  -o-- --',
    #         '- o     -x',
    #         '----- - -x',
    #         'xx- o b -x',
    #         'xx-     -x',
    #         'xx-------x']
    #
    # print(solve(map3))

    # targets = find_targets(map3)
    # depth_maps = [distances_from_target(map3, t) for t in targets]
    # print(heuristic(map3, depth_maps))
