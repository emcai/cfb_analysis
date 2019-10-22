import csv
import sys
from scipy.stats import norm

def load_ratings(file_name):
    sp_ratings = {}
    with open(file_name) as csvfile:
        reader = csv.reader(csvfile)
        csvfile.readline()
        for row in reader:
            sp_ratings[row[0]] = float(row[1])
    return sp_ratings

def build_resume(ratings):
    

def main():
    if len(sys.argv) != 3:
        print("Usage: <model results file> <sp+ ratings file>")
    ratings = load_ratings(sys.argv[2])
    build_resume(ratings)

if __name__ == '__main__':
    main()
