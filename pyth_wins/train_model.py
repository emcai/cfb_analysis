import numpy as np
import csv
import sys

from sklearn import metrics
from sklearn.linear_model import LogisticRegression

def load_data(file_name):
	dataset = []
	with open(file_name) as csvfile:
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
			tmp_arr.append(tmp_string[0])
			tmp_arr.append(tmp_string[1])
		else:
			tmp_string = tmp_string.split('vs')
			tmp_arr.append(tmp_string[0])
			tmp_arr.append(tmp_string[1])
		game_list.append(tmp_arr)
	return game_list


def main():
	if len(sys.argv) != 3:
		print("Usage: <training file> <testing file>")
		exit()
	X_train, Y_train, games = load_data(sys.argv[1])
	X_test, Y_test, games = load_data(sys.argv[2])
	print(games)

	clf = LogisticRegression()
	clf.fit(X_train, Y_train)
	Y_predicted = clf.predict(X_test)
	Y_prob = clf.predict_proba(X_test)

	for x in range(len(Y_prob)):
		print((x + 2, Y_prob[x][1], Y_predicted[x]))

if __name__ == '__main__':
	main()