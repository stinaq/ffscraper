from bs4 import BeautifulSoup
import requests



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

def parse_story_text(html):
  story_container = html.find("div", {"id": "storytext"})
  return story_container.find_all('p')


def create_capter(url):
  # return all things needed to visit next chapter, including new url?
  html = request_page(url)
  
  # if chapter_has_next(html):
  #   return
  return {
    'has_next': chapter_has_next(html),
    'paragraphs': parse_story_text(html)
  }

def chapter_has_next(html):
  all_buttons = html.find_all('button')

  return any(button.text == 'Next >' for button in all_buttons)

def parse_story_title(html):
  profile_top = html.find('div', {'id':'profile_top'})
  return profile_top.b.text

def request_page(url):
  r = requests.get(url)
  return BeautifulSoup(r.content, 'html.parser')

def create_story(story_id):
  story = {}
  base_url = 'https://www.fanfiction.net/s/'
  first_page = request_page(base_url + str(story_id))
  story['title'] = parse_story_title(first_page)
  
  story['chapters'] = create_capter(base_url + str(story_id))

  return story


story_id = 12300213

story = create_story(story_id)

print story



# all_ps = soup.find("div", {"id": "storytext"})

# print all_ps