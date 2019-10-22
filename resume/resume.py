from scipy.stats import norm

psu = norm.ppf(0.72, loc=18.5, scale=17)
michigan = norm.ppf(0.28, loc=24.6, scale=17)
print(psu)
print(michigan)
