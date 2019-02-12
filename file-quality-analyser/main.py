import argparse
import os
import time

import sonar_utils


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('sc_path'
                        , type=str
                        , help='The path to the sonar scanner executable.\n')
    parser.add_argument('project_path'
                        , type=str
                        , help='The project to analyse.\n')
    parser.add_argument('file_path'
                        , type=str
                        , help='The file to analyse.\n')
    parser.add_argument('project_key'
                        , type=str
                        , help='The project key.\n')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    target_dir = "{}/target".format(args.project_path)
    if not os.path.isdir(target_dir):
        os.mkdir(target_dir)
    if not sonar_utils.check_key_exists(args.project_key):
        sonar_utils.run_command(
            sonar_utils.build_scanner_command(args.sc_path, args.project_key, args.project_path, "./target"),
            args.project_path
        )
    res: dict = {}
    while not res.get("component", dict()).get("measures"):
        res = sonar_utils.exec_request(
            sonar_utils.build_sonar_request(args.project_key, args.file_path)
        )
        time.sleep(1)
    print(res)
