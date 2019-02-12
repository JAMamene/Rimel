import json
import os
import subprocess
import time
import urllib.request

METRICS = ["blocker_violations", "bugs", "code_smells", "cognitive_complexity", "comment_lines", "class_complexity",
           "function_complexity", "confirmed_issues", "critical_violations", "complexity",
           "duplicated_blocks", "info_violations", "violations", "lines", "major_violations", "minor_violations"]


def build_scanner_command(scanner_path: str, project_key: str, src: str, binaries: str) -> str:
    return '{}/sonar-scanner -Dsonar.projectKey={} -Dsonar.sources={} -Dsonar.java.binaries={}' \
        .format(scanner_path,
                project_key, src,
                binaries)


def run_command(command: str, path) -> str:
    curdir = os.curdir
    os.chdir(path)
    tmp = time.time()
    p = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = p.communicate()
    if err.decode() != "":
        raise Exception(err.decode())
    os.chdir(curdir)
    return output.decode()


def build_sonar_request(project, file_name):
    return 'http://localhost:9000/api/measures/component?component={}:{}&metricKeys={}'.format(project,
                                                                                               file_name,
                                                                                               ",".join(METRICS))


def exec_request(request):
    return json.loads(urllib.request.urlopen(request).read().decode())


def check_key_exists(key):
    req = "http://localhost:9000/api/components/search?qualifiers=TRK"
    res = json.loads(urllib.request.urlopen(req).read().decode())
    for project in res["components"]:
        if project["key"] == key:
            return True
    return False
