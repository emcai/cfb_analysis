import requests
import json

game_list = {}
games_url = 'https://api.collegefootballdata.com/games' 			#list of games
stats_url = 'https://api.collegefootballdata.com/games/teams' 		#statistics of games for each team
conferences = ["ACC", "B12", "B1G", "SEC", "PAC", "CUSA", "MAC", "MWC", "Ind", "SBC", "AAC"]

def game_scrape(year, conf):
	data = {
		'year' : year,
		'conference' : conf
	}

	response = requests.get(games_url, params=data)
	if not response.ok:
		response.raise_for_status()

	results = response.json()
	for result in results:
		if result["id"] not in game_list:
			game_list[result["id"]] = {}

def results_scrape(year, game):
	data = {
		'year' : year,
		'gameId' : game
	}

	response = requests.get(stats_url, params=data)
	if not response.ok:
		response.raise_for_status()

	results = response.json()
	print(results)

def main():

	'''
	for conf in conferences:
		print(conf)
		game_scrape(2018, conf)
		print(len(game_list))
	'''

	results_scrape(2018, 401013169)

if __name__ == '__main__':
	main()