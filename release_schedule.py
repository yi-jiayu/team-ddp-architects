from datetime import datetime, timedelta
from collections import namedtuple
import json

"""ts = time.strptime('28-05-2017 16:00:00.000+0800', '%d-%m-%Y %H:%M:%S.%f%z')"""

date_format = '%d-%m-%Y %H:%M:%S.%f%z'
Task = namedtuple('Task', ['start', 'end'])


def parse_input(parsed_json):
    num_tasks, it_start, it_finish = parsed_json[0].split(';')
    num_tasks = int(num_tasks)

    it_start = datetime.strptime(it_start.replace('Z', '+0000'), date_format)
    it_finish = datetime.strptime(it_finish.replace('Z', '+0000'), date_format)

    tasks = []
    for i in range(num_tasks):
        name, start, end = parsed_json[i + 1].split(';')
        start = datetime.strptime(start.replace('Z', '+0000'), date_format)
        end = datetime.strptime(end.replace('Z', '+0000'), date_format)

        task = Task(start, end)
        tasks.append(task)

    return num_tasks, it_start, it_finish, tasks


def find_longest_gap(num_tasks: int, it_start: datetime, it_finish: datetime, tasks: [Task]):
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
    parsed_json = json.loads(test_input)
    print(find_longest_gap(*parse_input(parsed_json)))

    test_case_2 = """["70;28-05-2017 20:00:00.000-0400;29-05-2017 14:00:00.000-0400","Hong Kong market maintenance;29-05-2017 19:23:32.379+0800;29-05-2017 20:54:21.183+0800","London trading test;29-05-2017 10:20:19.995+0000;29-05-2017 12:51:56.098+0000","New York trading test;29-05-2017 06:13:48.564-0400;29-05-2017 08:12:55.084-0400","Australia risk marking test;29-05-2017 18:00:00.000+1000;29-05-2017 19:00:00.000+1000","New York trading test;29-05-2017 06:52:21.115-0400;29-05-2017 08:12:32.214-0400","Australia market condition check;29-05-2017 21:12:51.119+1000;29-05-2017 22:07:19.790+1000","Australia trading test;29-05-2017 21:03:05.824+1000;29-05-2017 22:23:23.529+1000","New York trading test;29-05-2017 07:17:45.882-0400;29-05-2017 08:07:35.401-0400","Australia market condition check;29-05-2017 21:18:39.858+1000;29-05-2017 22:50:17.612+1000","London market maintenance;29-05-2017 10:29:06.763+0000;29-05-2017 12:18:29.239+0000","Australia trading test;29-05-2017 20:12:35.973+1000;29-05-2017 22:03:59.091+1000","Australia trading test;29-05-2017 20:12:08.964+1000;29-05-2017 22:07:50.193+1000","Australia market maintenance;29-05-2017 20:03:40.632+1000;29-05-2017 21:54:56.826+1000","London market maintenance;29-05-2017 10:39:58.158+0000;29-05-2017 12:45:52.482+0000","Japan database backup;29-05-2017 19:37:25.394+0900;29-05-2017 21:20:17.419+0900","Japan market maintenance;29-05-2017 19:19:45.535+0900;29-05-2017 20:34:57.250+0900","Australia trading test;29-05-2017 20:29:24.997+1000;29-05-2017 22:10:27.761+1000","Australia market condition check;29-05-2017 21:21:08.726+1000;29-05-2017 22:48:40.364+1000","New York risk marking test;29-05-2017 06:38:54.637-0400;29-05-2017 08:27:20.630-0400","Japan market condition check;29-05-2017 19:00:00.000+0900;29-05-2017 22:00:00.000+0900","New York risk marking test;29-05-2017 07:16:17.819-0400;29-05-2017 07:51:21.048-0400","Japan trading test;29-05-2017 19:27:02.191+0900;29-05-2017 21:09:10.121+0900","Hong Kong database backup;29-05-2017 18:51:35.714+0800;29-05-2017 20:06:22.266+0800","London risk marking test;29-05-2017 10:07:53.884+0000;29-05-2017 11:35:59.240+0000","Hong Kong market condition check;29-05-2017 19:14:27.654+0800;29-05-2017 19:31:22.436+0800","Hong Kong risk marking test;29-05-2017 18:31:16.525+0800;29-05-2017 19:31:10.575+0800","New York database backup;29-05-2017 07:24:26.511-0400;29-05-2017 08:19:46.935-0400","Japan risk marking test;29-05-2017 19:33:54.694+0900;29-05-2017 20:45:25.971+0900","London database backup;29-05-2017 10:26:21.838+0000;29-05-2017 12:56:08.202+0000","London risk marking test;29-05-2017 10:29:23.381+0000;29-05-2017 12:04:40.952+0000","India market maintenance;29-05-2017 16:30:00.000+0530;29-05-2017 17:30:00.000+0530","London trading test;29-05-2017 11:17:33.470+0000;29-05-2017 12:31:08.725+0000","Japan trading test;29-05-2017 19:13:03.921+0900;29-05-2017 21:17:08.114+0900","London trading test;29-05-2017 10:25:53.827+0000;29-05-2017 12:16:49.343+0000","New York market condition check;29-05-2017 07:10:22.429-0400;29-05-2017 08:22:09.151-0400","Hong Kong database backup;29-05-2017 19:04:05.899+0800;29-05-2017 20:42:15.963+0800","Hong Kong market maintenance;29-05-2017 18:26:52.612+0800;29-05-2017 19:51:39.210+0800","Australia market condition check;29-05-2017 20:37:01.265+1000;29-05-2017 22:55:54.819+1000","Japan trading test;29-05-2017 19:50:17.756+0900;29-05-2017 21:06:55.893+0900","Hong Kong risk marking test;29-05-2017 18:05:05.335+0800;29-05-2017 19:52:42.995+0800","London risk marking test;29-05-2017 10:09:01.829+0000;29-05-2017 11:59:21.887+0000","Japan market condition check;29-05-2017 19:17:09.897+0900;29-05-2017 21:14:22.894+0900","New York risk marking test;29-05-2017 07:02:28.041-0400;29-05-2017 08:39:31.343-0400","Hong Kong trading test;29-05-2017 19:01:42.686+0800;29-05-2017 20:07:41.621+0800","London market maintenance;29-05-2017 10:59:09.211+0000;29-05-2017 12:09:02.695+0000","Japan risk marking test;29-05-2017 20:20:38.232+0900;29-05-2017 20:30:43.729+0900","Japan market maintenance;29-05-2017 20:17:40.314+0900;29-05-2017 21:19:47.989+0900","New York trading test;29-05-2017 10:00:00.000-0400;29-05-2017 15:00:00.000-0400","New York database backup;29-05-2017 07:26:43.296-0400;29-05-2017 08:39:16.529-0400","Australia risk marking test;29-05-2017 20:34:16.140+1000;29-05-2017 22:07:34.737+1000","Japan market maintenance;29-05-2017 19:46:29.549+0900;29-05-2017 21:12:46.926+0900","London market condition check;29-05-2017 10:12:22.949+0000;29-05-2017 11:44:12.008+0000","London market maintenance;29-05-2017 10:57:51.419+0000;29-05-2017 12:28:06.941+0000","New York market maintenance;29-05-2017 07:13:50.336-0400;29-05-2017 08:41:25.118-0400","London trading test;29-05-2017 11:22:36.630+0000;29-05-2017 12:40:41.579+0000","Japan database backup;29-05-2017 19:20:04.193+0900;29-05-2017 21:44:30.300+0900","Hong Kong trading test;29-05-2017 6:00:00.000+0800;29-05-2017 11:00:00.000+0800","Australia market maintenance;29-05-2017 20:47:12.782+1000;29-05-2017 22:21:11.171+1000","Japan market condition check;29-05-2017 20:01:29.339+0900;29-05-2017 21:46:36.227+0900","Australia risk marking test;29-05-2017 20:25:38.690+1000;29-05-2017 22:10:50.970+1000","New York market maintenance;29-05-2017 06:53:10.181-0400;29-05-2017 08:36:45.822-0400","London database backup;29-05-2017 10:43:59.383+0000;29-05-2017 11:49:03.658+0000","Japan market maintenance;29-05-2017 20:01:19.525+0900;29-05-2017 21:55:05.839+0900","Australia trading test;29-05-2017 20:51:04.640+1000;29-05-2017 22:39:39.547+1000","Japan market maintenance;29-05-2017 19:58:23.143+0900;29-05-2017 20:56:46.511+0900","London database backup;29-05-2017 2:00:00.000Z;29-05-2017 6:00:00.000Z","London database backup;29-05-2017 10:27:00.789+0000;29-05-2017 11:56:37.848+0000","New York risk marking test;29-05-2017 07:25:59.812-0400;29-05-2017 08:54:03.784-0400","New York trading test;29-05-2017 06:30:33.405-0400;29-05-2017 08:18:46.702-0400","New York trading test;29-05-2017 07:24:10.174-0400;29-05-2017 07:32:23.802-0400"]"""

    parsed_json = json.loads(test_case_2)
    print(find_longest_gap(*parse_input(parsed_json)))
