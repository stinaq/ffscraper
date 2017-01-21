from bs4 import BeautifulSoup
import requests

def parse_story_text(html):
  story_container = html.find("div", {"id": "storytext"})
  return story_container.find_all('p')

def parse_next_url(html):
  all_buttons = html.find_all('button')
  next_button = next(button for button in all_buttons if button.string == 'Next >')
  link_text = next_button['onclick']
  return 'https://www.fanfiction.net' + link_text.split('\'')[1]

def create_capter(url):
  # return all things needed to visit next chapter, including new url?
  html = request_page(url)

  chapter = {}
  chapter['paragraphs'] = parse_story_text(html)
  chapter['has_next'] = chapter_has_next(html)

  if chapter['has_next']:
    chapter['next_url'] = parse_next_url(html)

  return chapter

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
  has_next_chapter = chapter_has_next(first_page)
  
  story['chapters'] = []
  url = base_url + str(story_id)

  while has_next_chapter:
    chapter = create_capter(url)

    if chapter['has_next']:
      has_next_chapter = chapter['has_next']
      url = chapter['next_url']
    else:
      has_next_chapter = False

    story['chapters'].append(chapter)

  return story

def create_file(story):
  file_name = story['title'].replace(' ', '-') + '.txt'
  with open("output/" + file_name, "w") as text_file:
    text_file.write(story['title'] + '\n\n')
    for chapter in story['chapters']:
      for paragraph in chapter['paragraphs']:
        text_file.write('   ' + str(paragraph.string) + '\n')
      text_file.write('\n\n')

story_id = 12314240

story = create_story(story_id)
create_file(story)

print story
