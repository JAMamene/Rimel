import json
import requests


def get_token():
    with open('../token', 'r') as file:
        token = file.read().replace('\n', '')
        if token == '':
            print('NO TOKEN PROVIDED, NEED TO PROVIDE A TOKEN FILE WITH TOKEN LUL')
        return token


HEADER = {'Authorization': 'token ' + get_token()}
JSON_PATH = '../repositories.json'
LANGUAGE = 'java'
MAX_SIZE_KB = '2500'
MIN_COMMITS = 300
NB_REPO = 10


def get_repos(page_nb):
    url = 'https://api.github.com/search/repositories?q=language:' + LANGUAGE + ' size:<' \
          + MAX_SIZE_KB + ' is:public&page=' + str(page_nb)
    return requests.get(url, headers=HEADER).json()['items']


def has_enough_commits(commits_url):
    return len(requests.get(commits_url[:-6] + '?page=' + str(MIN_COMMITS // 30), headers=HEADER).json()) != 0


def not_likely_android(repo_name):
    return repo_name.lower().find("android") == -1


if __name__ == "__main__":
    repo_list = []
    i = 2
    print(' ' * NB_REPO + ' |')
    finished = False
    while True:
        if finished:
            break
        for repo in get_repos(i):
            if not_likely_android(repo['full_name']) and has_enough_commits(repo['commits_url']):
                repo_details = {'name': repo['full_name'], 'clone': repo['clone_url']}
                repo_list.append(repo_details)
                print('.', flush=True, end='')
                if len(repo_list) > NB_REPO-1:
                    finished = True
                    break
        i += 1
    with open(JSON_PATH, 'w') as fp:
        json.dump(repo_list, fp)
