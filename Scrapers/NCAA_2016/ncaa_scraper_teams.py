import requests
from bs4 import BeautifulSoup

# NCAA_2017 Scraper

# construct urls
base_url = "http://www.ncaa.com/"
end_url = "/basketball-men/d1/"
scores_url = base_url + "scoreboard" + end_url
standings_url = base_url + "standings" + end_url

# request data
standings_html = requests.get(standings_url)

# pass to BS4
soup = BeautifulSoup(standings_html.content, "html.parser")

def appendToFile(file_name, search):
	# OPEN FILE for appending
	teams_file = open(file_name, 'a')
	# loop through all <a><span> school name </span></a>
	for data in soup.select(search):
		data1 = data.string
		data2 = data.parent.parent.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.string
		teams_file.write(data1 + ',' + data2 + '\n') #append team to file
	teams_file.close() # CLOSE FILE!

appendToFile("team_names.csv", ".ncaa-standing-conference-team-link span")