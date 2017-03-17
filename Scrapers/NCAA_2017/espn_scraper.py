import requests
from bs4 import BeautifulSoup
from Scrapers.NCAA_2017.Game import Game
from Scrapers.NCAA_2017.Team import Team

# URL Variables
bracket_url = "http://games.espn.com/tournament-challenge-bracket/2017/en/bracket?ex_cid=TC2017_NCAAMSubNav"
base_team_url = "http://www.espn.com/mens-college-basketball/team/"
schedule_url = "schedule/"
stats_url = "stats/"
id_url = "_/id/"

# Request and parse bracket HTML content
bracket_soup = BeautifulSoup(requests.get(bracket_url).content, "html.parser")

# Initialize Variables
team_ids = []

# Populate team urls list with Round of 64 contenders
for bracket_team in bracket_soup.findAll('span', class_='actual'):
    team_id = bracket_team.get('data-sportsid')
    if int(team_id) > 0:
        team_ids.append(team_id)


# Create link to team
def team_to_url(team_id, category_url=""):
    return base_team_url + category_url + id_url + team_id


def populate_schedule(team, team_id, rows):
    end_index = len(rows)
    for i in range(end_index):
        if len(rows[i].findAll('td')) == 1:
            end_index = i
            break
    for row in rows[:end_index]:
        class_list = row.get('class')
        opponent_id = class_list[1][5:].split('-')[-1]
        table_data = row.findAll('td')
        score_text = table_data[2].find('li', 'score').text
        if score_text == 'Postponed' or score_text == 'Canceled':
            continue
        score = table_data[2].find('a').text.split()[0].split('-')
        did_win = 'win' in table_data[2].find('li', class_='game-status').get('class')
        if did_win:
            team.record[0] += 1
        else:
            team.record[1] += 1
        is_home_team = table_data[1].find('li', class_='game-status').text == 'vs'
        if is_home_team:
            game = Game(team_id, opponent_id, tuple(score))
        else:
            game = Game(opponent_id, team_id, tuple(score))
        game.winner_id = team if did_win else opponent_id
        team.schedule.append(game)


def populate_stats(team, stat_totals):
    game_stats = stat_totals[0].findAll('td', align='right')
    del game_stats[1]
    season_stats = stat_totals[1].findAll('td', align='right')[1:]
    team.game_stats['GP'] = float(game_stats[0].text)
    team.game_stats['PPG'] = float(game_stats[1].text)
    team.game_stats['RPG'] = float(game_stats[2].text)
    team.game_stats['APG'] = float(game_stats[3].text)
    team.game_stats['SPG'] = float(game_stats[4].text)
    team.game_stats['BPG'] = float(game_stats[5].text)
    team.game_stats['TPG'] = float(game_stats[6].text)
    team.game_stats['FG%'] = float(game_stats[7].text)
    team.game_stats['FT%'] = float(game_stats[8].text)
    team.game_stats['3P%'] = float(game_stats[9].text)
    team.season_stats['FGM'] = float(season_stats[0].text)
    team.season_stats['FGA'] = float(season_stats[1].text)
    team.season_stats['FTM'] = float(season_stats[2].text)
    team.season_stats['FTA'] = float(season_stats[3].text)
    team.season_stats['3PM'] = float(season_stats[4].text)
    team.season_stats['3PA'] = float(season_stats[5].text)
    team.season_stats['PTS'] = float(season_stats[6].text)
    team.season_stats['REB'] = float(season_stats[7].text)
    team.season_stats['AST'] = float(season_stats[8].text)
    team.season_stats['STL'] = float(season_stats[9].text)
    team.season_stats['BLK'] = float(season_stats[10].text)
    team.season_stats['TO'] = float(season_stats[11].text)
    team.season_stats['OFFR'] = float(season_stats[12].text)
    team.season_stats['DEFR'] = float(season_stats[13].text)


for team_id in team_ids:
    team_schedule_soup = BeautifulSoup(requests.get(team_to_url(team_id, schedule_url)).content, 'html.parser')
    team_stats_soup = BeautifulSoup(requests.get(team_to_url(team_id, stats_url)).content, 'html.parser')
    team_name = team_schedule_soup.find('a', class_='sub-brand-title').find('b').text
    print(team_name)
    team = Team(team_name)
    populate_schedule(team, team_id, team_schedule_soup.find('table').findAll('tr', {'class': ['evenrow', 'oddrow']}))
    populate_stats(team, team_stats_soup.findAll('tr', class_='total'))
    Game.teams[team_id] = team


def fill_out_bracket():
    i = 1
    contestants = team_ids
    winners = []
    while len(contestants) > 1:
        print('*'*i + 'Round', str(i) + '*'*i)
        for index, team_id in list(enumerate(contestants))[::2]:
            opponent_id = contestants[index + 1]
            game = Game(team_id, opponent_id)
            winner_id = game.predict_winner()
            winners.append(winner_id)
            print('Winner of', Game.teams[team_id].name, 'vs', Game.teams[opponent_id].name, 'is', Game.teams[winner_id].name)
        contestants = winners
        winners = []
        i += 1
