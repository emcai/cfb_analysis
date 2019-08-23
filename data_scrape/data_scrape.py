import requests
import json
import string
import csv

game_list = {}
stats_list = []
games_url = 'https://api.collegefootballdata.com/games' 			#list of games
stats_url = 'https://api.collegefootballdata.com/games/teams' 		#statistics of games for each team
conferences = ["ACC", "B12", "B1G", "SEC", "PAC", "CUSA", "MAC", "MWC", "Ind", "SBC", "AAC"]
exclusion_list = []

#get indices of the relevant data, given the API output
def find_indexes(stats):
	to_return = [-1, -1, -1, -1]
	for x in range(len(stats)):
		if stats[x]["category"] == "totalYards":
			to_return[0] = x
		elif stats[x]["category"] == "rushingAttempts":
			to_return[1] = x
		elif stats[x]["category"] == "completionAttempts":
			to_return[2] = x
		elif stats[x]["category"] == "turnovers":
			to_return[3] = x
	if to_return[0] == -1 or to_return[1] == -1 or to_return[2] == -1 or to_return[3] == -1:
		return None
	if int(stats[to_return[0]]["stat"]) == 0:
		return None
	return to_return

#make API call to get game IDs of all FBS games
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
			#mark the game winner
			if result["away_points"] < result["home_points"]:
				game_list[result["id"]]["result"] = 1
			else:
				game_list[result["id"]]["result"] = 0

#Parses all data in a given conference/game/team and adds it to the stats_list list
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
		#check if API results are well-formatted
		if result["id"] not in game_list:
			continue
		game = result["id"]
		if len(result["teams"]) != 2:
			#print("\n\n\n" + result["teams"][0])
			exclusion_list.append((result["teams"][0]["school"], result["teams"][1]["school"]))
			continue

		#parse API data
		team_1_stats = result["teams"][0]["stats"]
		team_2_stats = result["teams"][1]["stats"]
		team_1_indexes = find_indexes(team_1_stats)
		team_2_indexes = find_indexes(team_2_stats)
		if team_1_indexes == None or team_2_indexes == None:
			#print("\n\n\n".join(['%s:: %s' % (key, value) for (key, value) in result["teams"][0].items()]))
			exclusion_list.append((result["teams"][0]["school"], result["teams"][1]["school"]))
			continue

		#calculate yards per play margin
		team_1_ypp = float(team_1_stats[team_1_indexes[0]]["stat"]) / (float(team_1_stats[team_1_indexes[1]]["stat"]) + float(team_1_stats[team_1_indexes[2]]["stat"].split('-')[1]))
		team_2_ypp = float(team_2_stats[team_2_indexes[0]]["stat"]) / (float(team_2_stats[team_2_indexes[1]]["stat"]) + float(team_2_stats[team_2_indexes[2]]["stat"].split('-')[1]))
		
		#build the result dict
		relevant = {}
		relevant["info"] = game_list[game]["info"]
		relevant["to_margin"] = int(team_1_stats[team_1_indexes[3]]["stat"]) - int(team_2_stats[team_2_indexes[3]]["stat"])
		relevant["ypp_margin"] = round(team_1_ypp - team_2_ypp, 2)
		relevant["yds_margin"] = int(team_1_stats[team_1_indexes[0]]["stat"]) - int(team_2_stats[team_2_indexes[0]]["stat"])
		relevant["result"] = game_list[game]["result"]

		stats_list.append(relevant)
		del game_list[game]

def main():
	#get 2018 data
	for conf in conferences:
		game_scrape(2018, conf=conf)
		results_scrape(2018, conf=conf)

	csv_columns = ["info", "to_margin", "ypp_margin", "yds_margin", "result"]
	with open('2018.csv', 'w') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
		writer.writeheader()
		for data in stats_list:
			writer.writerow(data)

	print(exclusion_list)
	game_list.clear()
	stats_list.clear()

	#get 2017 data
	for conf in conferences:
		game_scrape(2017, conf=conf)
		results_scrape(2017, conf=conf)

	csv_columns = ["info", "to_margin", "ypp_margin", "yds_margin", "result"]
	with open('2017.csv', 'w') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
		writer.writeheader()
		for data in stats_list:
			writer.writerow(data)

if __name__ == '__main__':
	main()