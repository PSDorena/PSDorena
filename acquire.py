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
from typing import Dict, List
import requests
import pandas as pd 
from bs4 import BeautifulSoup

from requests import get


from env import github_token
from env import user_agent

# TODO: Make a github personal access token.
#     1. Go here and generate a personal access token https://github.com/settings/tokens
#     2. Save it in your env.py file under the variable `github_token`
# TODO: Replace YOUR_GITHUB_USERNAME below with your github username.
# TODO: Add more repositories to the `repos` list.

#repos = ["gocodeup/codeup-setup-script", "gocodeup/movies-application"]

headers = {
    "Authorization": f"token {github_token}",
    "User-Agent": f"{user_agent}",
}

if (
    headers["Authorization"] == "token "
    or headers["User-Agent"] == "YOUR_GITHUB_USERNAME"
):
    raise Exception(
        "You need to follow the instructions marked TODO in this script before trying to use it"
    )

def get_urls(n):
    if os.path.exists('urls.csv'):
        return pd.read_csv('urls.csv').urls.tolist()

    url = 'https://github.com/search?o=desc&q=stars:%3E1&s=forks&type=Repositories'
    urls = [url]

    for page in range(2,n+1):
        urls.append(f'https://github.com/search?o=desc&amp;p={page}&amp;q=stars%3A%3E1&amp;s=forks&amp;type=Repositories')
    urls = pd.DataFrame({'urls': urls})
    urls.to_csv('urls.csv', index = False)
    return urls.urls.tolist()

def get_repo_list(n):

    if os.path.exists('repo_names.csv'):
        return pd.read_csv('repo_names.csv').repo_names.tolist()

    urls = get_urls(n)

    repo_names = []
    count  = 1
    for url in urls:
        headers = {'User-Agent': 'Data Science Student'}
        response = get(url, headers=headers)

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
    repo_names_df.to_csv('repo_names.csv', index = False)

    return  repo_names.repo_names.tolist()


def github_api_request(url: str) -> requests.Response:
    return requests.get(url, headers=headers)


def get_repo_language(repo: str) -> str:
    url = f"https://api.github.com/repos/{repo}"
    return github_api_request(url).json()["language"]


def get_repo_contents(repo: str) -> List[Dict[str, str]]:
    url = f"https://api.github.com/repos/{repo}/contents/"
    return github_api_request(url).json()


def get_readme_download_url(files: List[Dict[str, str]]) -> str:
    """
    Takes in a response from the github api that lists
    the files in a repo and returns the url that can be
    used to download the repo's README file.
    """
    for file in files:
        if file["name"].lower().startswith("readme"):
            return file["download_url"]


def process_repo(repo: str) -> Dict[str, str]:
    """
    Takes a repo name like "gocodeup/codeup-setup-script" and returns
    a dictionary with the language of the repo and the readme contents.
    """
    contents = get_repo_contents(repo)
    return {
        "repo": repo,
        "language": get_repo_language(repo),
        "readme_contents": requests.get(get_readme_download_url(contents)).text,
    }


def scrape_github_data():
    if os.path.exists('data.json'):
        print('data.csv exists in the repository')
        return pd.read_json('data.json')
    """
    Loop through all of the repos and process them. Saves the data in
    `data.json`.
    """
    repos = get_repo_list(10)
    data = [process_repo(repo) for repo in repos]
    json.dump(data, open("data.json", "w"))





if __name__ == "__main__":
    scrape_github_data()

# for repo in repos:  
#     print(process_repo(repo))

#get_repo_list()