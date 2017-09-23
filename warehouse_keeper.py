from queue import PriorityQueue
from copy import deepcopy
from collections import deque


def parse_map(map_):
    return [list(row) for row in map_]


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
        if map_[r - 1][c] not in ('-', 'x'):
            yield (r - 1, c)

    if r < len(map_) - 1:
        if map_[r + 1][c] not in ('-', 'x'):
            yield (r + 1, c)

    if c > 0:
        if map_[r][c - 1] not in ('-', 'x'):
            yield (r, c - 1)

    if c < len(map_[0]) - 1:
        if map_[r][c + 1] not in ('-', 'x'):
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


def h(map_, distances):
    return sum(distances[box] for box in find_boxes(map_))


def restore_stars(map_, stars):
    for r, c in stars:
        if map_[r][c] == ' ':
            map_[r][c] = '*'


def get_possible_moves(map_):
    r, c = find_keeper(map_)

    # move up into empty space
    if r > 0 and map_[r - 1][c] == ' ':
        next_state = deepcopy(map_)
        next_state[r][c] = ' '
        next_state[r - 1][c] = 'b'
        yield 'up', next_state

    # push box up into empty space
    if r > 1 and map_[r - 1][c] == 'o' and map_[r - 2][c] in (' ', '*'):
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

    if r < len(map_) - 2 and map_[r + 1][c] == 'o' and map_[r + 2][c] in (' ', '*'):
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

    if c > 1 and map_[r][c - 1] == 'o' and map_[r][c - 2] in (' ', '*'):
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

    if c < len(map_[0]) - 2 and map_[r][c + 1] == 'o' and map_[r][c + 2] in (' ', '*'):
        next_state = deepcopy(map_)
        next_state[r][c] = ' '
        next_state[r][c + 1] = 'b'
        next_state[r][c + 2] = 'o'
        yield 'right', next_state


def modify_string(old, pos, c):
    s = list(old)
    s[pos] = c
    return ''.join(s)


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

    q = PriorityQueue()
    q.put((h(map_, distances), 0, map_, ()))
    visited = set()

    while not q.empty():
        hf, steps, state, actions = q.get()

        frozen = freeze_map(state)
        visited.add(frozen)

        heuristic = h(state, distances)
        if heuristic == 0:
            return actions

        for direction, next_state in get_possible_moves(state):
            if freeze_map(next_state) not in visited:
                new_hf = h(next_state, distances) + steps + 1
                new_actions = actions + (direction,)
                restore_stars(next_state, stars)
                q.put((new_hf, steps+1, next_state, new_actions))

    return None


if __name__ == '__main__':
    map_ = ["xx---xxx",
            "xx-*-xxx",
            "xx- ----",
            "---o o*-",
            "-*ob  --",
            "----o --",
            "xxx-*-xx",
            "xxx---xx"]

    map_ = parse_map(map_)

    print(solve(map_))
