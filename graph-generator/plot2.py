import json
import os
import sys

import plotly as py
import plotly.graph_objs as go
import numpy

metrics = ["blocker_violations", "bugs", "code_smells", "cognitive_complexity", "comment_lines", "class_complexity",
           "function_complexity", "confirmed_issues", "critical_violations", "complexity",
           "duplicated_blocks", "info_violations", "violations", "lines", "major_violations", "minor_violations"]

complexity_metrics = ["class_complexity", "function_complexity", "complexity"]
lines_metric = ["lines", "comment_lines"]
other_metrics = ["blocker_violations", "bugs", "code_smells", "confirmed_issues", "critical_violations",
                 "duplicated_blocks", "info_violations", "violations", "major_violations", "minor_violations"]

graphs_folder = "../graphs"

all_values = []

all_before = []
all_after = []
relative = []

all_open = []
all_close = []
all_high = []
all_low = []


def create_folder(path):
    if not os.path.exists(path):
        os.mkdir(path)


def get_filename(item):
    return item.split("/")[len(item.split("/")) - 1]


def process_all_metrics(project_name, project_json):
    print("Processing data for project " + project_name + "...")
    for filename in project_json:
        all_conflicts_json = project_json[filename]
        for conflict_json in all_conflicts_json:
            for i in range(0, len(metrics)):
                metric = metrics[i]
                before = find_value(conflict_json["before"]["component"]["measures"], metric)
                after = find_value(conflict_json["after"]["component"]["measures"], metric)
                all_values[i].append(float(after) - float(before))
                all_before[i].append(float(before))
                all_after[i].append(float(after))


def find_value(metric_array, metric):
    for metric_object in metric_array:
        if metric_object["metric"] == metric:
            return metric_object["value"]
    print("Could not find value for " + metric)


def process_collected_values():
    print("Processing averages...")
    for i in range(0, len(metrics)):
        std = numpy.std(all_values[i])
        avg = numpy.average(all_values[i])
        all_open.append(avg + std)
        all_close.append(avg - std)
        all_high.append(numpy.amax(all_values[i]))
        all_low.append(numpy.amin(all_values[i]))


def generate_candlesticks():
    graph_names = ["complexityMetrics", "linesMetrics", "otherMetrics"]
    all_selected = [complexity_metrics, lines_metric, other_metrics]
    for i in range(0, len(all_selected)):
        data = [generate_single_candle(all_selected[i])]
        py.offline.plot(data, filename=graphs_folder + "/" + graph_names[i] + ".html", auto_open=False)


def generate_single_candle(selected):
    opened = []
    close = []
    low = []
    high = []
    for metric in selected:
        opened.append(all_open[metrics.index(metric)])
        close.append(all_close[metrics.index(metric)])
        low.append(all_low[metrics.index(metric)])
        high.append(all_high[metrics.index(metric)])
    return go.Candlestick(x=selected, open=opened, close=close, low=low, high=high, showlegend=False)


def generate_histogram():
    for i in range(0, len(metrics)):
        avg_before = numpy.average(all_before[i])
        avg_after = numpy.average(all_after[i])
        if avg_before == 0:
            print("Cannot calculate relative increase because average is 0, value for " + metrics[
                i] + " will be replaced with 0")
            relative.append(0)
        else:
            val = (avg_after - avg_before) / avg_before * 100
            print("Average relative difference for " + metrics[i] + " after a merge: " + str(val) + "%")
            relative.append(val)
    trace = go.Histogram(x=metrics, y=relative, histfunc="sum")
    data = [trace]
    py.offline.plot(data, filename=graphs_folder + "/beforeAfterRelative.html", auto_open=False)


def main(argv):
    if len(argv) < 2:
        print("Pass the json output of the SonarQube script as arg (../file-quality-analyser)")
        return
    json_path = argv[1]

    for _ in metrics:
        all_values.append([])
        all_before.append([])
        all_after.append([])

    create_folder(graphs_folder)
    with(open(json_path)) as file:
        json_object = json.load(file)
        for project in json_object:
            process_all_metrics(project, json_object[project])

    process_collected_values()
    generate_candlesticks()
    generate_histogram()


if __name__ == "__main__":
    main(sys.argv)
