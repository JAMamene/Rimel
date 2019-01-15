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
CSV_PATH = './result.csv'
LANGUAGE = 'java'
MIN_SIZE_KB = '1000'
MIN_COMMITS = 100


def get_repos():
    url = 'https://api.github.com/search/repositories?q=language:' + LANGUAGE + '&size>' + MIN_SIZE_KB + '&is:public'
    return requests.get(url, headers=HEADER).json()['items']

def get_nb_commit(url, page):
    nb = len(requests.get(url, headers=HEADER).json())


if __name__ == "__main__":
    get_repos()
    repo_list = []
    for repo in get_repos():
        if get_nb_commit(repo['commits_url'][:-6], 0) > MIN_COMMITS:
            repo_list.append(repo['full_name'])
    print(repo_list)