from datetime import datetime, timedelta
from collections import namedtuple
import json

"""ts = time.strptime('28-05-2017 16:00:00.000+0800', '%d-%m-%Y %H:%M:%S.%f%z')"""

date_format = '%d-%m-%Y %H:%M:%S.%f%z'
Task = namedtuple('Task', ['start', 'end'])


def parse_input(json_str):
    inp = json.loads(json_str)
    num_tasks, it_start, it_finish = inp[0].split(';')
    num_tasks = int(num_tasks)

    it_start = datetime.strptime(it_start.replace('Z', '+0000'), date_format)
    it_finish = datetime.strptime(it_finish.replace('Z', '+0000'), date_format)

    tasks = []
    for i in range(num_tasks):
        name, start, end = inp[i + 1].split(';')
        start = datetime.strptime(start.replace('Z', '+0000'), date_format)
        end = datetime.strptime(end.replace('Z', '+0000'), date_format)

        task = Task(start, end)
        tasks.append(task)

    return num_tasks, it_start, it_finish, tasks


def release_schedule(num_tasks: int, it_start: datetime, it_finish: datetime, tasks: [Task]):
    if num_tasks == 0:
        return (it_finish - it_start).total_seconds()

    latest_end = it_start
    gaps = []
    for task in tasks:
        if task.start > latest_end:
            if task.start >= it_finish:
                gaps.append((latest_end, it_finish))
                break
            else:
                gaps.append((latest_end, task.start))

        if task.end > latest_end:
            latest_end = task.end

    longest_gap = timedelta()
    for gap in gaps:
        if gap[1] - gap[0] > longest_gap:
            longest_gap = gap[1] - gap[0]

    return int(longest_gap.total_seconds())


if __name__ == '__main__':
    test_input = """["3;28-05-2017 13:00:00.000+0800;28-05-2017 16:00:00.000+0800",
"London morning trading check;28-05-2017 05:15:00.000Z;28-05-2017 06:15:00.000Z",
"Tokyo risk testing;28-05-2017 16:15:00.000+0900;28-05-2017 16:45:00.000+0900",
"New York midnight database check;28-05-2017 03:50:00.000-0400;28-05-2017 03:59:00.000-0400"]"""
    print(release_schedule(*parse_input(test_input)))
