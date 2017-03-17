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


def add_day(date):
    return time.strftime("%Y/%m/%d", time.localtime(time.mktime(time.strptime(date, "%Y/%m/%d")) + 24 * 60 * 60))


# OPEN FILE for appending
games_file = open("game_score.csv", 'a')
header_row = 'date,team matchup,1st half score, 2nd half score, final score, winner\n'
games_file.write(header_row)
# loop through all <a><span> school name </span></a>
t = start_date
start_time = time.mktime(time.strptime(start_date, "%Y/%m/%d"))
end_time = time.mktime(time.strptime(end_date, "%Y/%m/%d"))

while start_time <= time.mktime(time.strptime(t, "%Y/%m/%d")) <= end_time:
    url = base_url + t
    # request data
    scores_html = requests.get(url)
    # pass to BS4
    soup = BeautifulSoup(scores_html.content, "html.parser")

for matchups in soup.find_all("table", {'class': 'linescore'}):
    tr1 = matchups.contents[1].contents
    tr2 = matchups.contents[2].contents
    try:
        team_matchup = tr1[0].a.string + ',' + tr2[0].a.string
        team_href = tr1[0].a['href'] + ',' + tr2[0].a['href']
        first_half_score = tr1[1].string + ',' + tr2[1].string
        second_half_score = tr1[2].string + ',' + tr2[2].string
        final_score = tr1[3].string + ',' + tr2[3].string
        if 'winner' in tr1[4]['class']:
            value1 = 1
            value2 = 0
        else:
            value1 = 0
            value2 = 1
        winner_of_game = str(value1) + ',' + str(value2)
        normal_date = time.strftime('%d/%m/%Y', time.strptime(t, '%Y/%m/%d'))
        games_file.write(
            t + ',' + team_matchup + ',' + first_half_score + ',' + second_half_score + ',' + final_score + ',' + winner_of_game + '\n')  # append team to file
    except:
        pass

t = add_day(t)
games_file.close()
