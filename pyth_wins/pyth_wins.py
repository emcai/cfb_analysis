import csv
import sys

def load_wins(file_name):
	wins = {}
	with open(file_name) as csvfile:
		reader = csv.reader(csvfile)
		csvfile.readline()
		for row in reader:
			#print(row)
			if row[0] not in wins:
				wins[row[0]] = float(row[1])
			else:
				wins[row[0]] += float(row[1])
			if row[2] not in wins:
				wins[row[2]] = float(row[3])
			else:
				wins[row[2]] += float(row[3])
	return wins

def load_ratings(file_name):
    sp_ratings = {}
    with open(file_name) as csvfile:
        reader = csv.reader(csvfile)
        csvfile.readline()
        for row in reader:
            sp_ratings[row[0]] = float(row[1])
    return sp_ratings

def main():
	if len(sys.argv) != 3:
		print("Usage: <model results file> <SP+ ratings file>")
		exit()
	wins = load_wins(sys.argv[1])
	ratings = load_ratings(sys.argv[2])

	for team in model:
		if team in ratings:
			print(team + " " + str(model[team]))

if __name__ == '__main__':
	main()
