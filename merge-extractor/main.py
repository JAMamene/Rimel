import json
import os
import subprocess
import requests
from cd import cd


def get_token():
    with open('../token', 'r') as file:
        str = file.read().replace('\n', '')
        if str == '':
            print('NO TOKEN PROVIDED, NEED TO PROVIDE A TOKEN FILE WITH TOKEN LUL')
        return str


TOKEN = get_token()
JSON_PATH = '../repositories.json'
REPOSITORIES_DIRECTORY = "../repositories"
CSV_PATH = '../merges.csv'


def get_all_commit(owner, repo_name, branch):
    url = 'https://api.github.com/repos/%s/%s/commits?sha=%s' % (owner, repo_name, branch)
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
        print(Exception)
        raise Exception


def get_base_commit(repo_name, repo_url, left_commit, right_commit):
    if not os.path.isdir(REPOSITORIES_DIRECTORY + '/%s' % repo_name):
        git_clone(repo_url)
    with cd(REPOSITORIES_DIRECTORY + '/%s' % repo_name):
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
    merges = []
    with open(JSON_PATH, 'r') as f:
        data = json.load(f)
        for repo_info in data:
            owner = repo_info['name'].split('/')[0]
            repo_name = repo_info['name'].split('/')[1]
            branches = get_repositories_branch(owner, repo_name)
            for branch in branches:
                commits = get_all_commit(owner, repo_name, branch['name'])
                merges = merges + get_merges(commits, repo_info['clone'], repo_name)
    return merges


def write_merges(merges):
    with open('%s' % CSV_PATH, 'w') as f:
        f.write('url,left,right,result,base\n')
        f.flush()
        print("%d merge(s) found" % len(merges))
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
