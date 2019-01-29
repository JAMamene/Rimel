import plotly as py
import plotly.graph_objs as go
import seaborn as sns

# Create random data with numpy
import numpy as np
import json
from scipy import stats

merge_json = "../merges-conflicts.json"
min_data_points = 5


def get_filename(item):
    return item.split("/")[len(item.split("/")) - 1]


if __name__ == "__main__":
    with(open(merge_json)) as file:
        json_object = json.load(file)
        for project in json_object:
            x = []
            for filename in json_object[project]:
                x.append(json_object[project][filename])

            if len(x) >= min_data_points:
                y = np.random.randn(len(x))
                trace = go.Scatter(
                    x=x,
                    y=y,
                    mode='markers'
                )

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

                name = get_filename(project).replace(".git", "") + "-scatter.html"
                py.offline.plot(data, filename=name)
