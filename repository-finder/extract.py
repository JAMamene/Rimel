import json
import sys

import requests
from argparser import parse_args


def get_token():
    with open('../token', 'r') as file:
        token = file.read().replace('\n', '')
        if token == '':
            print('NO TOKEN PROVIDED, NEED TO PROVIDE A TOKEN FILE WITH TOKEN LUL')
        return token


HEADER = {'Authorization': 'token ' + get_token()}
JSON_PATH = '../repositories.json'
LANGUAGE = 'java'


def get_repos(page_nb, max_size):
    url = 'https://api.github.com/search/repositories?q=language:' + LANGUAGE + ' size:<' + str(max_size) \
          + ' is:public&page=' + str(page_nb)
    res = requests.get(url, headers=HEADER).json()['items']
    return res


def has_enough_commits(commits_url, min_commits):
    return len(requests.get(commits_url[:-6] + '?page=' + str(min_commits // 30), headers=HEADER).json()) != 0


def not_likely_android(repo_name):
    return repo_name.lower().find("android") == -1


if __name__ == "__main__":
    args = parse_args()
    repo_list = []
    i = 1
    sys.stdout.write("[%s]" % (" " * args.nb_repo))
    sys.stdout.flush()
    sys.stdout.write("\b" * (args.nb_repo + 1))
    finished = False
    while True:
        if finished:
            break
        for repo in get_repos(i, args.max_size):
            if not_likely_android(repo['full_name']) and has_enough_commits(repo['commits_url'], args.min_commits):
                repo_details = {'name': repo['full_name'], 'clone': repo['clone_url']}
                repo_list.append(repo_details)
                sys.stdout.write("-")
                sys.stdout.flush()
                if len(repo_list) > args.nb_repo - 1:
                    finished = True
                    break
        i += 1
    sys.stdout.write("\n")
    with open(JSON_PATH, 'w') as fp:
        json.dump(repo_list, fp)
