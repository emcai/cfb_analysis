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

def build_resume(file_name, ratings):
    resume_ranks = {}
    game_points = {}
    info_points = {}
    with open(file_name) as csvfile:
        reader = csv.reader(csvfile)
        csvfile.readline()
        for row in reader:
            team1 = row[0]
            rate1 = float(row[1])
            team2 = row[2]
            rate2 = float(row[3])
            if team1 not in ratings or team2 not in ratings:
                continue
            if team1 not in game_points:
                game_points[team1] = []
                info_points[team1] = []
            game_points[team1].append(game_score(rate1, ratings[team2]))
            info_points[team1].append((game_score(rate1, ratings[team2]), team2, rate1))
            if team2 not in game_points:
                game_points[team2] = []
                info_points[team2] = []
            game_points[team2].append(game_score(rate2, ratings[team1]))
            info_points[team2].append((game_score(rate2, ratings[team1]), team1, rate2))
    for team in game_points:
        resume_ranks[team] = round(sum(game_points[team]) / len(game_points[team]), 2)

    sorted_ranks = sorted(resume_ranks.items(), key=lambda kv: kv[1], reverse=True)
    for team in sorted_ranks:
        print(team[0] + " " + str(team[1]))
    for g in info_points:
        print(g + " " + str(info_points[g]))

def game_score(pyth_win, rating):
    if pyth_win >= 0.99:
        pyth_win = 0.99
    elif pyth_win <= 0.01:
        pyth_win = 0.01
    return norm.ppf(pyth_win, loc=rating, scale=17)

def main():
    if len(sys.argv) != 3:
        print("Usage: <model results file> <sp+ ratings file>")
        exit()
    ratings = load_ratings(sys.argv[2])
    build_resume(sys.argv[1], ratings)

if __name__ == '__main__':
    main()
