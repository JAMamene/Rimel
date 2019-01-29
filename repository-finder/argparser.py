import argparse


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('nb_repo'
                        , type=int
                        , help='The number of repositories to find\n')
    parser.add_argument('min_commits'
                        , type=int
                        , help='The minimum number of commits to have.\n')
    parser.add_argument('max_size'
                        , type=int
                        , help='The maximum allowed repository size in KB.\n')
    return parser.parse_args()
