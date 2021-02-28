from scipy.stats import norm

print(norm.ppf(0.365, loc=17.0, scale=17))

def game_score(pyth_win, rating):
    if pyth_win >= 0.999:
        pyth_win = 0.999
    elif pyth_win <= 0.001:
        pyth_win = 0.001
    return norm.ppf(pyth_win, loc=rating, scale=17)

print(game_score(0.365, 17.0))
