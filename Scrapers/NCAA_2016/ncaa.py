import requests
from bs4 import BeautifulSoup
import random

# Scraping Starts Here
base_url = "http://www.ncaa.com/"
end_url = "/basketball-men/d1/"
scores_url = base_url + "scoreboard" + end_url
standings_url = base_url + "standings" + end_url

standings_html = requests.get(standings_url)

soup = BeautifulSoup(standings_html.content, "html.parser")

schools = {}

for school in soup.select(".ncaa-standing-conference-team-link span"):
    conference = school.parent.parent.parent.parent.parent.previous_sibling.string
    overall_record = school.parent.parent.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.string
    schools[school.string] = overall_record

east_seeds = ["North Carolina A&T", "Villanova", "Oklahoma", "Michigan State", "Utah", "Wisconsin", "Cincinnati",
              "Texas A&M", "Georgetown", "Louisville", "Rhode Island", "Tulsa", "Iona", "Yale", "Lehigh",
              "North Carolina Central"]
south_seeds = ["Kentucky", "Duke", "Wichita State", "California", "Michigan", "Purdue", "West Virginia", "Xavier",
               "Miami (FL)", "UCLA", "Valparaiso", "Central Michigan", "UC Irvine", "Hofstra", "Louisiana-Lafayette",
               "Chattanooga"]
west_seeds = ["Maryland", "Arizona", "Iowa State", "Butler", "Oregon", "Connecticut", "Notre Dame",
              "North Carolina State", "San Diego State", "Texas", "Iowa", "BYU", "UAB", "South Dakota State",
              "New Mexico State", "High Point"]
midwest_seeds = ["Kansas", "Virginia", "Gonzaga", "Indiana", "Vanderbilt", "LSU", "Baylor", "Dayton", "Florida State",
                 "Boise State", "Providence", "Stephen F. Austin", "Belmont", "Stony Brook", "North Florida", "Montana"]

seeds = [east_seeds, south_seeds, west_seeds, midwest_seeds]


def upset(team1, team2):
    if float(schools[team1]) != float(schools[team2]):
        return abs(
            round(abs(float(schools[team1]) - float(schools[team2])) * 10, 2) * 16 - round(random.random() * 10, 2))
    else:
        return round(random.random() * 20, 2)


def winnerOf(team1, team2):
    prob = upset(team1, team2)
    chance = random.random() * 100
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


def populateBracket(seeds):
    regions = ["East", "South", "West", "Midwest"]
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
            for i in range(0, 4):
                print(regions[i])
                for j in [1, 8, 5, 4, 6, 3, 7, 2]:
                    result_list = winnerOf(seeds[i][seed(j)], seeds[i][seed(n - j)])
                    results1.append(result_list[0])
                    w = result_list[0]
                    l = result_list[1]
                    if result_list[2]:
                        acts_on = " UPSETS "
                        u += 1
                    else:
                        acts_on = " beats "
                    print("\t" + w + acts_on + l, "\tUpset %: " + str(upset(seeds[i][seed(j)], seeds[i][seed(n - j)])))

        if r == 32:
            results2 = []
            for i in regions:
                print(i)
                j = 0
                while j < 4:
                    result_list = winnerOf(results1[0], results1[1])
                    upset_percent = upset(results1[0], results1[1])
                    results1.remove(results1[0])
                    results1.remove(results1[0])
                    results2.append(result_list[0])
                    w = result_list[0]
                    l = result_list[1]
                    if result_list[2]:
                        acts_on = " UPSETS "
                        u += 1
                    else:
                        acts_on = " beats "
                    print("\t" + w + acts_on + l, "\tUpset %: " + str(upset_percent))
                    j += 1
        if r == 16:
            results3 = []
            for i in regions:
                print(i)
                j = 0
                while j < 2:
                    result_list = winnerOf(results2[0], results2[1])
                    upset_percent = upset(results2[0], results2[1])
                    results2.remove(results2[0])
                    results2.remove(results2[0])
                    results3.append(result_list[0])
                    w = result_list[0]
                    l = result_list[1]
                    if result_list[2]:
                        acts_on = " UPSETS "
                        u += 1
                    else:
                        acts_on = " beats "
                    print("\t" + w + acts_on + l, "\tUpset %: " + str(upset_percent))
                    j += 1
        if r == 8:
            results4 = []
            for i in regions:
                print(i)
                j = 0
                while j <= 0:
                    result_list = winnerOf(results3[0], results3[1])
                    upset_percent = upset(results3[0], results3[1])
                    results3.remove(results3[0])
                    results3.remove(results3[0])
                    results4.append(result_list[0])
                    w = result_list[0]
                    l = result_list[1]
                    if result_list[2]:
                        acts_on = " UPSETS "
                        u += 1
                    else:
                        acts_on = " beats "
                    print("\t" + w + acts_on + l, "\tUpset %: " + str(upset_percent))
                    j += 1
        if r == 4:
            results5 = []
            for i in ["East vs. West", "South vs. Midwest"]:
                print(i)
                result_list = winnerOf(results4[0], results4[1])
                upset_percent = upset(results4[0], results4[1])
                results4.remove(results4[0])
                results4.remove(results4[0])
                results5.append(result_list[0])
                w = result_list[0]
                l = result_list[1]
                if result_list[2]:
                    acts_on = " UPSETS "
                    u += 1
                else:
                    acts_on = " beats "
                print("\t" + w + acts_on + l, "\tUpset %: " + str(upset_percent))
        if r == 2:
            final_result = winnerOf(results5[0], results5[1])
            w = final_result[0]
            l = final_result[1]
            if result_list[2]:
                acts_on = " UPSETS "
                u += 1
            else:
                acts_on = " beats "
            print("\t" + w + acts_on + l, "\tUpset %: " + str(upset(results5[0], results5[1])))
        r /= 2
        print("Total Number of Upsets", u)


populateBracket(seeds)
# print schools["Villanova"], schools["Kansas"]
# print round(1/abs(float(schools["California"]) - float(schools["Texas A&M"])), 2)
