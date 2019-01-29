import argparse
import json
import os
import subprocess
import urllib.request
from pprint import pprint

import data


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('sonar_scanner_path'
                        , type=str
                        , help='The path to the sonar scanner executable.\n')
    parser.add_argument('project_key'
                        , type=str
                        , help='The project key.\n')
    parser.add_argument('-s', '--src'
                        , type=str
                        , help='The path to src directory for the project.\n')
    parser.add_argument('-b', '--binaries'
                        , type=str
                        , help='The path to the binaries directory.\n')
    return parser.parse_args()


def build_scanner_command(scanner_path: str, project_key: str, src: str, binaries: str) -> str:
    return '{}/sonar-scanner -Dsonar.projectKey={} -Dsonar.sources={} -Dsonar.java.binaries={}' \
        .format(scanner_path,
                project_key, src,
                binaries)


def run_command(command: str) -> str:
    print(command)
    p = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = p.communicate()
    if err.decode() != "":
        raise Exception(err.decode())
    return output.decode()


def build_sonar_request(project):
    return 'http://localhost:9000/api/measures/component?component={}&metricKeys={}'.format(project,
                                                                                            ",".join(data.METRICS))


def exec_request(request):
    return json.loads(urllib.request.urlopen(request).read().decode())


def format_to_csv_line(data_dict):
    # print(data['component'])
    row: str = data_dict['component']['key']
    for metric in data.METRICS:
        for measure in data_dict['component']['measures']:
            if metric == measure['metric']:
                row += "," + measure['value']
    return row


if __name__ == '__main__':
    args = parse_args()
    if not args.binaries:
        args.binaries = "./target"
    if not args.src:
        args.src = "."
    if not os.path.isdir(args.binaries):
        os.mkdir(args.binaries)
    run_command(
        build_scanner_command(
            args.sonar_scanner_path,
            args.project_key,
            args.src,
            args.binaries))
    res = exec_request(build_sonar_request(args.project_key))
    pprint(res)
    print(format_to_csv_line(res))
