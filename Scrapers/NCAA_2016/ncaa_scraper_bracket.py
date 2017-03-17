from bs4 import BeautifulSoup
import requests
import random
import re

# URL Variables
base_url = "http://www.ncaa.com/"
end_url = "/basketball-men/d1/"
bracket_url = base_url + "interactive-bracket" + end_url

# Request HTML content
bracket_html = requests.get(bracket_url)

# Parse HTML content
soup = BeautifulSoup(bracket_html.content, "html.parser")

# Initialize Variables
schools = []            # Holds school names as strings
seeds = []              # Holds school seeds as strings
links = []              # Holds links to each school as 'school/SCHOOL_NAME'
bracket = []            # Stores the results of each game as decided by method winner_of()
opponents = []          # Stores lists of 2 tuples containing school name, seed, and link
total_upsets = 0        # Number of upsets in bracket

# Find all school names and seed numbers for game id 2xx (from 1st round)
for game in soup.findAll('section', id=re.compile('game2\d{2}')):
    for school in game.findAll('div', class_='team-name'):
        schools.append(str(school.string))
    for seed in game.findAll('div', class_='team-seed'):
        seeds.append(str(seed.string))

for school in schools:
    # General modifications
    link_text = school
    link_text = link_text.lower()
    link_text = link_text.replace(' ', '-').replace("'", '').replace('.', '')
    link_text = link_text.replace('(', '').replace(')', '')
    link_text = link_text.replace('state', 'st')

    # State specific modifications
    link_text = link_text.replace('-fla', '-fl')
    link_text = link_text.replace('-cal', '-ca')

    # Name specific modifications
    link_text = link_text.replace('steph', 'stephen')
    link_text = link_text.replace('uncw', 'unc-wilmington')

    links.append(link_text)

for i in range(0, len(schools) - 2, 2):
    opponents.append([(schools[i], seeds[i], links[i]), (schools[i+1]), seeds[i+1], links[i+1]])
print(opponents)


east_seeds = ["North Carolina A&T", "Villanova", "Oklahoma", "Michigan State", "Utah", "Wisconsin", "Cincinnati", "Texas A&M", "Georgetown", "Louisville", "Rhode Island", "Tulsa", "Iona", "Yale", "Lehigh", "North Carolina Central"]
south_seeds = ["Kentucky", "Duke", "Wichita State", "California", "Michigan", "Purdue", "West Virginia", "Xavier", "Miami (FL)", "UCLA", "Valparaiso", "Central Michigan", "UC Irvine", "Hofstra", "Louisiana-Lafayette", "Chattanooga"]
west_seeds = ["Maryland", "Arizona", "Iowa State", "Butler", "Oregon", "Connecticut", "Notre Dame", "North Carolina State", "San Diego State", "Texas", "Iowa", "BYU", "UAB", "South Dakota State", "New Mexico State", "High Point"]
midwest_seeds = ["Kansas", "Virginia", "Gonzaga", "Indiana", "Vanderbilt", "LSU", "Baylor", "Dayton", "Florida State", "Boise State", "Providence", "Stephen F. Austin", "Belmont", "Stony Brook", "North Florida", "Montana"]

seeds = [east_seeds, south_seeds, west_seeds, midwest_seeds]

def upset(team1, team2):
    if float(schools[team1]) != float(schools[team2]):
        return abs(round(abs(float(schools[team1]) - float(schools[team2]))*10, 2)*16 - round(random.random()*10, 2))
    else:
        return round(random.random()*20, 2)

def winner_of(team1, team2):
    prob = upset(team1, team2)
    chance = random.random()*100
    if schools[team1] > schools[team2]:
        favorite = team1
        underdog = team2
    else:
        favorite = team2
        underdog = team1
		
    if prob < chance:
        was_upset = False
        winner = favorite
        loser = underdog
    else:
        was_upset = True
        winner = underdog
        loser = favorite
    return [winner, loser, was_upset]

def seed(s):
    return s - 1

def format_bracket_entry(match):
    u = 0
    team1 = match[0][0]
    team2 = match[0][1]
    result_list = winner_of(team1, team2)
    upset_percent = upset(team1, team2)
    del opponents[team1]
    del opponents[team2]
    w = result_list[0]
    l = result_list[1]
    winners.append(w)
    if result_list[2]:
        acts_on = " UPSETS "
        u += 1
    else:
        acts_on = " beats "
    bracket.append("\t" + w + acts_on + l + "\tUpset %: " + str(upset_percent))
    return winners, u

def populate_bracket(matchups):
    regions = ["West", "East", "South", "Midwest"]
    n = len(seeds[0]) + 1
    r = 64
    u = 0
    while r > 1:
        if r == 64:
            print("Round of " + str(r) + "\n")
        elif r == 32:
            print("\nRound of " + str(r) + "\n")
        elif r == 16:
            print("\nSweet " + str(r) + "\n")
        elif r == 8:
            print("\nElite " + str(r) + "\n")
        elif r == 4:
            print("\nFinal " + str(r) + "\n")
        elif r == 2:
            print("\nChampionship\n")

        if r == 64:
            results1 = []
            for i in range(0,4):
                print regions[i]
                j = 0
                while j < r/8:
                    format_bracket_entry(matchups)
					
        if r == 32:
            results2 = []
            for i in regions:
                print(i)
                j = 0
                while j < r/8:
                    format_bracket_entry(results1)
                    j += 1
        if r == 16:
            results3 = []
            for i in regions:
                print(i)
                j = 0
                while j < r/8:
                    format_bracket_entry(results2)
                    j += 1
        if r == 8:
            results4 = []
            for i in regions:
                print(i)
                j = 0
                while j <= 0:
                    format_bracket_entry(results3)
                    j += 1
        if r == 4:
            results5 = []
            for i in ["East vs. West", "South vs. Midwest"]:
                print(i)
                format_bracket_entry(results4)
        if r == 2:
            format_bracket_entry(results5)
        r /= 2
        print("Total Number of Upsets", u)

