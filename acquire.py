from requests import get
from bs4 import BeautifulSoup
from os import path
import re
import pandas as pd
import json

import warnings



url = 'https://github.com/search?o=desc&q=stars%3A%3E1&s=forks&type=Repositories'
headers = {'User-Agent': 'Codeup Bayes Data Science'}
response = get(url, headers = headers)
soup = BeautifulSoup(response.content, 'html.parser')

soup.select('.pagination')[0].select_one('a')['href']

soup.select('.next_page')[0]

type(soup)