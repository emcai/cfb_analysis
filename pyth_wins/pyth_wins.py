import csv
import sys

def load_data(file_name):
	wins = {}
	with open(file_name) as csvfile:
		reader = csv.reader(csvfile)
		csvfile.readline()
		for row in reader:
			print(row)
			if row[0] not in wins:
				wins[row[0]] = float(row[1])
			else:
				wins[row[0]] += float(row[1])
			if row[2] not in wins:
				wins[row[2]] = float(row[3])
			else:
				wins[row[2]] = float(row[3])

def main():
	if len(sys.argv) != 2:
		print("Usage: <model results file>")
		exit()
	print(load_data(sys.argv[1]))

if __name__ == '__main__':
	main()