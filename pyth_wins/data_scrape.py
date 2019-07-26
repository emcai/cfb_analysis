import requests
import json
import string
import copy

game_list = {}
stats_list = {}
games_url = 'https://api.collegefootballdata.com/games' 			#list of games
stats_url = 'https://api.collegefootballdata.com/games/teams' 		#statistics of games for each team
conferences = ["ACC", "B12", "B1G", "SEC", "PAC", "CUSA", "MAC", "MWC", "Ind", "SBC", "AAC"]

def game_scrape(year, conf = None, team = None):
	if conf is not None:
		data = {
			'year' : year,
			'conference' : conf
		}
	else:
		data = {
			'year' : year,
			'team' : team
		}

	response = requests.get(games_url, params=data)
	if not response.ok:
		response.raise_for_status()

	results = response.json()
	for result in results:
		if result["id"] not in game_list:
			game_string = ""
			if result["neutral_site"] == False:
				game_string += (result["away_team"] + " @ " + result["home_team"] + ": " + str(result["away_points"]) + "-" + str(result["home_points"]))
			else:
				game_string += (result["away_team"] + " vs " + result["home_team"] + ": " + str(result["away_points"]) + "-" + str(result["home_points"]))
			game_list[result["id"]] = {"info" : game_string}
			if result["away_points"] < result["home_points"]:
				game_list[result["id"]]["result"] = 1
			else:
				game_list[result["id"]]["result"] = 0

def results_scrape(year, conf = None, game = None, team = None):
	if game is not None:
		data = {
			'year' : year,
			'gameId' : game
		}
	elif conf is not None:
		data = {
			'year' : year,
			'conference' : conf
		}
	else:
		data = {
			'year' : year,
			'team' : team
		}

	response = requests.get(stats_url, params=data)
	if not response.ok:
		response.raise_for_status()

	results = response.json()
	for result in results:
		if result["id"] not in game_list:
			continue
		game = result["id"]
		team_1_stats = result["teams"][0]["stats"]
		team_2_stats = result["teams"][1]["stats"]

		team_1_ypp = float(team_1_stats[11]["stat"]) / (float(team_1_stats[6]["stat"]) + float(team_1_stats[9]["stat"].split('-')[1]))
		team_2_ypp = float(team_2_stats[11]["stat"]) / (float(team_2_stats[6]["stat"]) + float(team_2_stats[9]["stat"].split('-')[1]))
		print(round(team_1_ypp, 2))
		print(round(team_2_ypp, 2))
		relevant = {}
		relevant["info"] = game_list[game]["info"]
		relevant["to_margin"] = int(team_1_stats[3]["stat"]) - int(team_2_stats[3]["stat"])
		relevant["ypp_margin"] = round(team_1_ypp - team_2_ypp, 2)
		relevant["yds_margin"] = int(team_1_stats[11]["stat"]) - int(team_2_stats[11]["stat"])
		relevant["result"] = game_list[game]["result"]

		stats_list[game] = relevant
		del game_list[game]


def main():

	#Code to get all game IDs
	'''
	for conf in conferences:
		print(conf)
		game_scrape(2018, conf=conf)
		print(len(game_list))
	'''

	#Code to print info for a single team
	'''
	game_scrape(2018, team="TCU")
	print(game_list)
	'''

	game_scrape(2018, team="Michigan")
	results_scrape(2018, team="Michigan")
	#print(game_list)
	print("\n\n\n")
	print(stats_list)
	#print(results_scrape(2018, game=401012821))
	

if __name__ == '__main__':
	main()