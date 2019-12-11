"""
A module for obtaining repo readme and language data from the github API.

Before using this module, read through it, and follow the instructions marked
TODO.

After doing so, run it like this:

    python acquire.py

To create the `data.json` file that contains the data.
"""
import os
import json
from typing import Dict, List, Optional, Union, cast
import requests
import pandas as pd

from bs4 import BeautifulSoup

from env import github_token, github_username

# TODO: Make a github personal access token.
#     1. Go here and generate a personal access token https://github.com/settings/tokens
#     2. Save it in your env.py file under the variable `github_token`
# TODO: Add your github username to your env.py file under the variable `github_username`
# TODO: Add more repositories to the `REPOS` list below.

# REPOS = [
#     "gocodeup/codeup-setup-script",
#     "gocodeup/movies-application",
#     "torvalds/linux",
# ]

headers = {"Authorization": f"token {github_token}", "User-Agent": github_username}

if headers["Authorization"] == "token " or headers["User-Agent"] == "":
    raise Exception(
        "You need to follow the instructions marked TODO in this script before trying to use it"
    )

def get_urls(n):
    if os.path.exists('urls_titanic.csv'):
        return pd.read_csv('urls_titanic.csv').urls.tolist()

    url = 'https://github.com/search?o=desc&p=1&q=titanic&s=stars&type=Repositories'
    urls = [url]

    for page in range(2,20):
        urls.append(f'https://github.com/search?o=desc&p={page}&q=titanic&s=stars&type=Repositories')
    urls = pd.DataFrame({'urls': urls})
    urls.to_csv('urls_titanic.csv', index = False)
    return urls.urls.tolist()

def get_repo_list(n):

    if os.path.exists('repo_names_titanic.csv'):
        return pd.read_csv('repo_names_titanic.csv').repo_names.tolist()

    urls = get_urls(10)

    repo_names = []
    count  = 1
    for url in urls[10:]:
        headers = {'User-Agent': 'Data Science Student'}
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print('Did not reach all urls')
            print(f'\nstopped at page # {count}:')
            print('\n' + url)
            break

        x = response.content
        soup = BeautifulSoup(x, 'html.parser')
        repo_links = soup.select('a[class = v-align-middle]')

        for l in range(len(repo_links)):
            repo_names.append(soup.select('a[class = v-align-middle]')[l].get_text())
        
        count += 1

    repo_names_df = pd.DataFrame({'repo_names':repo_names})
    repo_names_df.to_csv('repo_names_titanic.csv', index = False)

    return  repo_names_df.repo_names.tolist()



def github_api_request(url: str) -> Union[List, Dict]:
    response = requests.get(url, headers=headers)
    response_data = response.json()
    if response.status_code != 200:
        raise Exception(
            f"Error response from github api! status code: {response.status_code}, "
            f"response: {json.dumps(response_data)}"
        )
    return response_data


def get_repo_language(repo: str) -> str:
    url = f"https://api.github.com/repos/{repo}"
    repo_info = github_api_request(url)
    if type(repo_info) is dict:
        repo_info = cast(Dict, repo_info)
        return repo_info.get("language", None)
    raise Exception(
        f"Expecting a dictionary response from {url}, instead got {json.dumps(repo_info)}"
    )


def get_repo_contents(repo: str) -> List[Dict[str, str]]:
    url = f"https://api.github.com/repos/{repo}/contents/"
    contents = github_api_request(url)
    if type(contents) is list:
        contents = cast(List, contents)
        return contents
    raise Exception(
        f"Expecting a list response from {url}, instead got {json.dumps(contents)}"
    )


def get_readme_download_url(files: List[Dict[str, str]]) -> str:
    """
    Takes in a response from the github api that lists the files in a repo and
    returns the url that can be used to download the repo's README file.
    """
    for file in files:
        if file["name"].lower().startswith("readme"):
            return file["download_url"]
    return ""


def process_repo(repo: str) -> Dict[str, str]:
    """
    Takes a repo name like "gocodeup/codeup-setup-script" and returns a
    dictionary with the language of the repo and the readme contents.
    """
    # contents = get_repo_contents(repo)
    # readme_contents = requests.get(get_readme_download_url(contents)).text
    
    # return {
    #     "repo": repo,
    #     "language": get_repo_language(repo),
    #     "readme_contents": readme_contents,
    # }
    contents = get_repo_contents(repo)
    try:
        return {
            "repo": repo,
            "language": get_repo_language(repo),
            "readme_contents": requests.get(get_readme_download_url(contents)).text,
        }
    except:
        return {
        "repo": repo,
        "language": get_repo_language(repo),
        "readme_contents": "error: no README",
        }

def scrape_github_data() -> List[Dict[str, str]]:
    """
    Loop through all of the repos and process them. Returns the processed data.
    """
    if os.path.exists('data_titanic.json'):
        return pd.read_json('data_titanic.json')

    REPOS = get_repo_list(20)
    data = [process_repo(repo) for repo in REPOS]
    json.dump(data, open("data_titanic.json", "w"), indent=1)

    return pd.read_json('data_titanic.json')


if __name__ == "__main__":
    


get_repo_list(10)

pd.read_json('data_titanic.json')