import json
import os
import sys

import plotly as py
import plotly.graph_objs as go
from scipy import stats

metrics = ["blocker_violations", "bugs", "code_smells", "cognitive_complexity", "comment_lines", "class_complexity",
           "function_complexity", "confirmed_issues", "critical_violations", "complexity",
           "duplicated_blocks", "info_violations", "violations", "lines", "major_violations", "minor_violations"]

graphs_folder = "../graphs"

x_merge_values = []
y_quality_metrics = dict()


def create_folder(path):
    if not os.path.exists(path):
        os.mkdir(path)


def get_filename(item):
    return item.split("/")[len(item.split("/")) - 1]


def process_all_metrics(project_name, project_json):
    print("Processing data for project " + project_name + "...")
    for file_json in project_json:
        if file_json["quality"] == {}:
            print("Found no data, skipping file " + get_filename(file_json["file"]) + " in project " + project_name)
            continue
        x_merge_values.append(file_json["merges"])
        lines = 1
        for metric_json in file_json["quality"]["component"]["measures"]:
            if metric_json["metric"] is "lines":
                lines = float(metric_json["value"])
                break
        for metric_json in file_json["quality"]["component"]["measures"]:
            if metric_json["metric"] is "lines":
                y_quality_metrics[metric_json["metric"]].append(float(metric_json["value"]))
            else:
                y_quality_metrics[metric_json["metric"]].append(
                    float(metric_json["value"]) / lines)

    if len(x_merge_values) <= 1:
        print("--> One or Zero points to plot for " + project_name + ", no graphs will be generated!")
        return


def generate_graph(x, y, metric_name):
    if len(x) != len(y):
        print(
            "Cannot plot " + metric_name + " : mismatch between merges and metric data")
        return
    if metric_name is "lines":
        metric_name_clean: str = metric_name.replace("_", " ").capitalize()
    else:
        metric_name_clean: str = metric_name.replace("_", " ").capitalize() + " weighted by number of line"
    trace = go.Scatter(
        x=x,
        y=y,
        mode='markers',
        name=metric_name_clean)
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    line = []
    for i in x:
        line.append(slope * i + intercept)
    trace2 = go.Scatter(
        x=x,
        y=line,
        mode='lines',
        marker=go.scatter.Marker(color='rgb(237, 14, 69)'),
        name='Trend'
    )
    data = [trace, trace2]
    layout = dict(title="{} according to the number of merges per file".format(metric_name_clean),
                  xaxis={'title': dict(text='Merges')},
                  yaxis={'title': dict(text=metric_name_clean)})
    figure = go.Figure(data=data, layout=layout)
    py.offline.plot(figure, filename=graphs_folder + "/" + metric_name + ".html", auto_open=False)


def main(argv):
    if len(argv) < 2:
        print("Pass the json output of the SonarQube script as arg (../quality-analyser)")
        return
    json_path = argv[1]

    for metric in metrics:
        y_quality_metrics[metric] = []

    create_folder(graphs_folder)
    with(open(json_path)) as file:
        json_object = json.load(file)
        for project in json_object:
            process_all_metrics(project, json_object[project])

    for m in metrics:
        generate_graph(x_merge_values, y_quality_metrics[m], m)

    print(len(x_merge_values))


if __name__ == "__main__":
    main(sys.argv)
