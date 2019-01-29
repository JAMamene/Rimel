import json
import subprocess

from argparser import parse_args
from cd import cd


def git_reset_hard():
    return subprocess.run(['git', 'reset', '--hard'], stdout=subprocess.PIPE)


def git_checkout(commit):
    return subprocess.run(['git', 'checkout', '-f', commit], stdout=subprocess.PIPE).stdout.decode('utf-8')


def git_merge(commit):
    return subprocess.run(['git', 'merge', commit], stdout=subprocess.PIPE).stdout.decode('utf-8')


def extract_conflict_files(merge_result, project_conflict, result_committer_date, base_sha, result_sha):
    lines = merge_result.split('\n')
    for line in lines:
        if 'Auto-merging' in line:
            file_name = line[13:]
            if file_name not in project_conflict:
                project_conflict[file_name] = 0
                project_conflict['conflicts_history'][file_name] = []
            project_conflict[file_name] += 1
            project_conflict['conflicts_history'][file_name].append({'date': result_committer_date, 'base_sha': base_sha, 'result_sha': result_sha })
    return project_conflict


def extract_merge_conflict(repository_path, left_commit, right_commit, project_conflict, result_committer_date, base_sha, result_sha):
    with cd(repository_path):
        git_reset_hard()
        git_checkout(left_commit)
        merge_result = git_merge(right_commit)
        return extract_conflict_files(merge_result, project_conflict, result_committer_date, base_sha, result_sha)


def extract_repository_name(repository_url):
    return repository_url.rsplit('/', 1)[-1][:-4]


def extract_repository_owner(repository_url):
    return repository_url.rsplit('/', 1)[-2]


def extract_merges_conflict(repositories_path, merge_csv_path):
    with open(merge_csv_path) as file:
        lines = file.readlines()
    projects_conflicts = {}
    for line in lines[1:]:
        url, left_sha, right_sha, result_sha, base_sha, result_committer_date = line.split(',')
        if url not in projects_conflicts:
            projects_conflicts[url] = {}
            projects_conflicts[url]['conflicts_history'] = {}
        repository_name = extract_repository_name(url)
        repository_path = '%s/%s' % (repositories_path, repository_name)
        projects_conflicts[url] = extract_merge_conflict(repository_path, left_sha, right_sha, projects_conflicts[url], result_committer_date[:-1], base_sha, result_sha)
    projects_conflicts = sort_conflicts_history(projects_conflicts)
    return json.dumps(projects_conflicts, indent=2)

def sort_conflicts_history(projects_conflicts):
    for key_project_conflict, project_conflict in projects_conflicts.items():
        for key_file_history, file_history in project_conflict['conflicts_history'].items():
            projects_conflicts[key_project_conflict]['conflicts_history'][key_file_history] = sorted(file_history, key = lambda i: (i['date']), reverse=True) 
    return projects_conflicts

def write_result(json_result):
    with open('../merges-conflicts.json', 'w') as file:
        file.write(json_result)


if __name__ == "__main__":
    args = parse_args()
    json_result = extract_merges_conflict(args.repositories_path, args.merge_csv_path)
    write_result(json_result)
