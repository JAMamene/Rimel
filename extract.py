import urllib.request
import json
import re
import requests

def get_token():
    with open('token', 'r') as file:
        str = file.read().replace('\n', '')
        if str == '':
            print('NO TOKEN PROVIDED, NEED TO PROVIDE A TOKEN FILE WITH TOKEN LUL')
        return str

HEADER = {'Authorization': 'token ' + get_token()}
JSON_PATH = 'data.json'
LANGUAGE = 'java'
MIN_SIZE_KB = '1000'
MIN_COMMITS = 120
NB_REPO = 6


def get_repos(page_nb):
    url = 'https://api.github.com/search/repositories?q=language:' + LANGUAGE + '&size>' + MIN_SIZE_KB + '&is:public&page=' + str(page_nb)
    return requests.get(url, headers=HEADER).json()['items']

def has_enough_commits(url):
    return len(requests.get(url, headers=HEADER).json()) != 0


if __name__ == "__main__":
    repo_list = []
    i = 10
    print(' ' * NB_REPO + ' |')
    finished = False
    while True:
        if (finished):
            break
        for repo in get_repos(i):
            if has_enough_commits(repo['commits_url'][:-6] + '?page=' + str(MIN_COMMITS//30)):
                repo_details = {}
                repo_details['name'] = repo['full_name']
                repo_details['clone'] = repo['clone_url']
                repo_list.append(repo_details)
                print('.',flush=True, end='')
                if (len(repo_list) > NB_REPO):
                    finished = True
                    break
        i+=1
    with open(JSON_PATH, 'w') as fp:
        json.dump(repo_list, fp)