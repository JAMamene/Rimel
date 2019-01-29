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

json_path = "../sample.json"


def create_folder(path):
    if not os.path.exists(path):
        os.mkdir(path)


def get_filename(item):
    return item.split("/")[len(item.split("/")) - 1]


def get_project_name(s):
    return s.split("/")[len(s.split("/")) - 1].replace(".git", "")


def generate_all_graphs(project_name, project_json):
    x_merge_values = []
    y_quality_metrics = dict()

    for metric in metrics:
        y_quality_metrics[metric] = []

    for file_json in project_json:
        x_merge_values.append(file_json["merges"])
        for metric_json in file_json["quality"]["component"]["measures"]:
            y_quality_metrics[metric_json["metric"]].append(float(metric_json["value"]))

    if len(x_merge_values) <= 1:
        print("--> One or Zero points to plot for " + project_name + ", no graphs will be generated!")
        return

    print("Generating graphs for project " + project_name + "...")
    create_folder(graphs_folder + "/" + project_name)

    for metric in metrics:
        generate_graph(x_merge_values, y_quality_metrics[metric], project_name, metric)


def generate_graph(x, y, project_name, metric_name):
    trace = go.Scatter(x=x, y=y, mode='markers')
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    line = []
    for i in x:
        line.append(slope * i + intercept)
    trace2 = go.Scatter(
        x=x,
        y=line,
        mode='lines',
        marker=go.scatter.Marker(color='rgb(31, 119, 180)'),
        name='Fit'
    )
    data = [trace, trace2]
    py.offline.plot(data, filename=graphs_folder + "/" + project_name + "/" + metric_name + ".html", auto_open=False)


def main(argv):
    if len(argv) < 2:
        print("Pass the json output of the SonarQube script as arg (../quality-analyser)")
        return

    create_folder(graphs_folder)
    with(open(json_path)) as file:
        json_object = json.load(file)
        for project in json_object:
            generate_all_graphs(get_project_name(project), json_object[project])


if __name__ == "__main__":
    main(sys.argv)
