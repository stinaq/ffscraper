from bs4 import BeautifulSoup
from requests import requests

r = requests.get('https://www.fanfiction.net/s/12291248/1/Eleanor-s-Wolves')
soup = BeautifulSoup(r.content, 'html.parser')
all_ps = soup.find("div", {"id": "storytext"})

# [
#   {
#     title: 'Something',
#     all_paragraphs: []
#   },
#   {
#     title: 'Something',
#     all_paragraphs: []
#   },
# ]

# get starting point
# request that page
# parse it and add it to data structure, also saving chapter name
# find the next button, and get the link
# go to that link
# do it all over again
