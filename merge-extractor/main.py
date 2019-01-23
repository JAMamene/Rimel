import urllib.request
import json
import re
import requests
import subprocess
import os
from cd import cd

def get_token():
    with open('../token', 'r') as file:
        str = file.read().replace('\n', '')
        if str == '':
            print('NO TOKEN PROVIDED, NEED TO PROVIDE A TOKEN FILE WITH TOKEN LUL')
        return str


USERNAME = 'fitzzzz'
TOKEN = get_token()
CSV_PATH = './repositories.csv'
REPOSITORIES_DIRECTORY = "./repositories"


def get_all_commit(owner, repo_name, branche):
    url = 'https://api.github.com/repos/%s/%s/commits?sha=%s' % (owner, repo_name, branche)
    headers = {'Authorization': 'token ' + TOKEN}
    resp = requests.get(url, headers=headers)
    return resp.json()


def get_repositories_branch(owner, repo_name):
    url = 'https://api.github.com/repos/%s/%s/branches' % (owner, repo_name)
    headers = {'Authorization': 'token ' + TOKEN}
    resp = requests.get(url, headers=headers)
    return resp.json()


def git_clone(url):
    try:
        p = subprocess.Popen(["git", "clone", url],
                                cwd=REPOSITORIES_DIRECTORY, stdout=subprocess.DEVNULL)
        p.communicate()
        p.wait()
    except Exception:
        print('not possible to clone repository : %s' % url)
        raise Exception


def get_base_commit(repo_name, repo_url, left_commit, right_commit):
    if not os.path.isdir('./repositories/%s' % repo_name):
        git_clone(repo_url)
    with cd('./repositories/%s' % repo_name):
        result = subprocess.run(["git", "merge-base", left_commit, right_commit], stdout=subprocess.PIPE)
        return result.stdout


def extract_merge_information(commit, repo_url, repo_name):
    left_parent, right_parent = commit['parents']
    return {
        'url': repo_url,
        'left': left_parent['sha'], 
        'right': right_parent['sha'], 
        'result': commit['sha'],
        'base': get_base_commit(repo_name, repo_url, left_parent['sha'], right_parent['sha'])
    }  

def get_merges(commits, repo_url, repo_name):
    merges = []
    for commit in commits:
        parents = commit['parents']
        if len(parents) == 2:
            merge_info = extract_merge_information(commit, repo_url, repo_name)
            merges.append(merge_info)
    return merges



def get_repositories_merges():
    informations = []
    merges = []
    with open('repositories.csv', 'r') as f:
        lines = f.readlines()
        for line in lines:
            owner, repo_name, repo_url = line.split(',')
            branches = get_repositories_branch(owner, repo_name)
            for branche in branches:
                commits = get_all_commit(owner, repo_name, branche['name'])
                merges = merges + get_merges(commits, repo_url, repo_name)
    return merges                

def write_merges(merges):
    with open('./merges.csv', 'w') as f:
        f.write('url,left,right,result,base\n')
        f.flush()
        print("%d merge(s) found"  % len(merges))
        for merge in merges:
            f.write('%s,%s,%s,%s,%s\n' % (merge['url'], merge['left'], merge['right'], merge['result'], merge['base']))
            f.flush()

def remove_duplicated_entries(l):
    return [dict(t) for t in {tuple(d.items()) for d in l}]


if __name__ == "__main__":
    if not os.path.isdir(REPOSITORIES_DIRECTORY):
        os.mkdir(REPOSITORIES_DIRECTORY)
    merges = get_repositories_merges()    
    write_merges(remove_duplicated_entries(merges))