import json


def parse_input(input_file: str):
    f = open(input_file)
    data = json.load(f)
    f.close()
    return data


def extract_repository_name(repository_url):
    return repository_url.rsplit('/', 1)[-1][:-4]


def extract_all_repo_names(input_file: str):
    res = dict()
    for git_url, files in parse_input(input_file).items():
        res[extract_repository_name(git_url)] = files
    return res
