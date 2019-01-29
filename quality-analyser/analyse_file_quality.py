import argparse
import json
import os
import urllib.parse
import urllib.request

import data
import parse_repos


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file'
                        , type=str
                        , help='A json file containing all repos and files.\n')
    parser.add_argument('output_file'
                        , type=str
                        , help='A json file where report will be writen.\n')
    return parser.parse_args()


def build_sonar_request(project, file):
    return 'http://localhost:9000/api/measures/component?component={}:{}&metricKeys={}' \
        .format(urllib.parse.quote(project), urllib.parse.quote(file), ",".join(data.METRICS))


def exec_request(request):
    try:
        return json.loads(urllib.request.urlopen(request).read().decode())
    except urllib.error.HTTPError:
        print("Request \"{}\" responded with 404 ... ")
        return dict()


def compute_quelity(input_file):
    input_data = parse_repos.extract_all_repo_names(input_file)
    # pprint(data)
    res = dict()
    for project, files in input_data.items():
        # pprint(files)
        res[project] = list()
        for file, merges in files.items():
            if os.path.splitext(file)[1] == '.java':
                # print(build_sonar_request(project, file))
                res[project].append(dict(file=file
                                         , merges=merges
                                         , quality=exec_request(build_sonar_request(project, file))))
            # print(quality)
    return res


if __name__ == '__main__':
    args = parse_args()
    res = compute_quelity(args.input_file)
    f = open(args.output_file, 'w')
    f.write(json.dumps(res))
    f.close()
