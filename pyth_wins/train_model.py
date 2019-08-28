import numpy as np
import csv
import sys

from sklearn import metrics
from sklearn.linear_model import LogisticRegression

def load_data(file_name):
	dataset = []
	with open(file_name,encoding = "ISO-8859-1") as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			dataset.append(row)
	dataset = dataset[1:]
	X_data = np.array(dataset)[:,1:4].astype(float)
	Y_data = np.array(dataset)[:,4].astype(int)

	games = [row[0] for row in dataset]
	games = extract_games(games)

	return X_data, Y_data, games

def extract_games(games):
	game_list = []
	for game in games:
		tmp_string = game.split(':')[0]
		tmp_arr = []
		if len(tmp_string.split('@')) > 1:
			tmp_string = tmp_string.split('@')
			tmp_arr.append(tmp_string[0].strip())
			tmp_arr.append(tmp_string[1].strip())
		else:
			tmp_string = tmp_string.split('vs')
			tmp_arr.append(tmp_string[0].strip())
			tmp_arr.append(tmp_string[1].strip())
		game_list.append(tmp_arr)
	return game_list


def main():
	if len(sys.argv) != 3:
		print("Usage: <training file> <testing file>")
		exit()
	X_train, Y_train, games = load_data(sys.argv[1])
	X_test, Y_test, games = load_data(sys.argv[2])

	clf = LogisticRegression()
	clf.fit(X_train, Y_train)
	Y_predicted = clf.predict(X_test)
	Y_prob = clf.predict_proba(X_test)

	csv_columns = ["team1", "t1pyth", "team2", "t2pyth"]
	with open('model_results.csv', 'w') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
		writer.writeheader()
		for x in range(len(Y_prob)):
			result = {}
			result["team1"] = games[x][0]
			result["t1pyth"] = round(1 - Y_prob[x][1], 3)
			result["team2"] = games[x][1]
			result["t2pyth"] = round(Y_prob[x][1], 3)
			writer.writerow(result)

if __name__ == '__main__':
	main()