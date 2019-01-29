import argparse
import json
import os
import urllib.parse
import urllib.request
from pprint import pprint

import data
import parse_repos


def parse_args():
    parser = argparse.ArgumentParser()

    # parser.add_argument('project_key'
    #                     , type=str
    #                     , help='The project key.\n')
    parser.add_argument('input_file'
                        , type=str
                        , help='A json file containing all repos and files.\n')
    return parser.parse_args()


def build_sonar_request(project, file):
    return 'http://localhost:9000/api/measures/component?component={}:{}&metricKeys={}' \
        .format(urllib.parse.quote(project), urllib.parse.quote(file), ",".join(data.METRICS))


def exec_request(request):
    return json.loads(urllib.request.urlopen(request).read().decode())


if __name__ == '__main__':
    args = parse_args()
    input_data = parse_repos.extract_all_repo_names(args.input_file)
    # pprint(data)
    res = dict()
    for project, files in input_data.items():
        pprint(files)
        res[project] = list()
        for file, merges in files.items():
            quality = None
            # print(file)
            # print(os.path.splitext(file)[1])
            if os.path.splitext(file)[1] == '.java':
                quality = exec_request(build_sonar_request(project, file))
            # print(quality)
            res[project].append(dict(file=file
                                     , merges=merges
                                     , quality=quality))
    pprint(res)
