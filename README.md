This README is an overivew and technical guide to our NLP project for Codeup.
NLP Project
For this project, we will be scraping data from GitHub repository README files. The goal will be to build a model that can predict what programming language a repository is, given the text of the README file.

ACQUIRE:

The goal for the acquire phase is to scrape data from the github website. We elected to cycle through github repositories that were filtered as being greater than 1 star and most forked. The search results for this search limited the search results to 10 entries per page, so our aim is to loop through ~14 pages of search results to achieve the stated requirement of at least 100 repositories.



