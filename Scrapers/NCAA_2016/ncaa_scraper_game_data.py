import requests
from bs4 import BeautifulSoup
import time

# NCAA_2017 Scraper

# construct url
start_url = "http://www.ncaa.com"
end_url = "/basketball-men/d1/"
base_url = start_url + "scoreboard/" + end_url
start_date = "2015/11/13"
end_date = "2016/03/12"


def addDay(date):
    return time.strftime("%Y/%m/%d", time.localtime(time.mktime(time.strptime(date, "%Y/%m/%d")) + 24*60*60))

# OPEN FILE for appending
#games_file = open("game_score.csv", 'a')
#header_row = 'date,team matchup,1st half score, 2nd half score, final score, winner\n'
#games_file.write(header_row)
# loop through all <a><span> school name </span></a>
t = start_date
start_time = time.mktime(time.strptime(start_date, "%Y/%m/%d"))
end_time = time.mktime(time.strptime(end_date, "%Y/%m/%d"))

while time.mktime(time.strptime(t, "%Y/%m/%d")) >= start_time and time.mktime(time.strptime(t, "%Y/%m/%d")) <= end_time:
	url = base_url + t
	# request data
	html = requests.get(url)
	# pass to BS4
	soup = BeautifulSoup(html.content, "html.parser")

	for urls in soup.find_all("a", {'class':'gamecenter'}):
		print(start_url + urls['href']	)

#games_file.close()	