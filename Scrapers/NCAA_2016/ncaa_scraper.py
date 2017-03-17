import requests
from bs4 import BeautifulSoup
import re

# URL Variables
protocol = "http://"
base = "www.ncaa.com/"
sport = "basketball-men/"
division = "d1/"
bracket_url = protocol + base + "interactive-bracket/" + sport
schools_url = protocol + base + "schools/"

# Request and parse bracket HTML content
soup = BeautifulSoup(requests.get(bracket_url).content, "html.parser")

# Initialize Variables
school_name_links = []  # Holds school names in link-friendly format


# Turn human-readable school names into link-friendly text
def school_to_link(name):
    # General modifications
    link_text = name.lower()
    link_text = link_text.replace(' ', '-').replace("'", '').replace('.', '')
    link_text = link_text.replace('(', '').replace(')', '')
    link_text = link_text.replace('state', 'st')

    # Region specific modifications
    link_text = link_text.replace('-fla', '-fl')
    link_text = link_text.replace('-cal', '-ca')

    # Name specific modifications
    link_text = link_text.replace('steph', 'stephen')
    link_text = link_text.replace('uncw', 'unc-wilmington')

    return link_text

# Populate school name links list with First Four and Round of 64 contenders
for game in soup.findAll('section', id=re.compile('game(1|2)\d{2}')):
    if "has-data" in game.get("class"):
        for school in game.findAll('div', class_='team-name'):
            school_name_links.append(school_to_link(school.string))
    elif "has-partial-data":
        for school in game.find('div', class_='team-name'):
            school_name_links.append(school_to_link(school.string))

# Request and parse HTML content for each school
for school_name in school_name_links:
    school = BeautifulSoup(requests.get(schools_url + school_name).content, "html.parser")
    school.find("table", class_="ncaa-schools-sport-table")
