# cfb_analysis
Analyzing college football data to create both predictions and rankings of past success

# 1.1: Data Scraping
Location: data_scrape/data_scrape.py

Using the college football API found at https://api.collegefootballdata.com/api/docs/?url=/api-docs.json, I get data from all regular-season games played by FBS teams in 2017 and 2018. 

As an example, I will use 2018's Michigan @ Michigan State game for data. The ESPN box score can be found here: https://www.espn.com/college-football/game?gameId=401012884

I use individual game statistics and get the following data as an example:

```
{
    'info': 'Michigan @ Michigan State: 21-7', 
    'to_margin': -1, 
    'ypp_margin': -3.22, 
    'yds_margin': -301, 
    'result': 0
}
```

"info" : Description of which teams are playing and the score. Away team is listed first. If the game is neutral-site, it will say "vs" instead of "@". This is not used in any model, just helping users follow the games more easily.

"to_margin" : Turnover margin. Equal to number of turnovers committed by the home team minus the number of turnovers committed by the away team. In our example, MSU committed 1 turnover while Michigan committed 2 turnovers for a to_margin of -1.

"ypp_margin" : Yards per play margin. Equal to (total yards) / (passing attempts + rushing attempts), home team minus away team. In our example, MSU achieved 1.84 yards / play, and Michigan achieved 5.06 yards / play, resulting in a ypp_margin of -3.22.

"yds_margin" : Yards margin. Equal to total yards, home team minus away team. In our example, MSU achieved 94 total yards, and Michigan achieved 395 total yards, resulting in a yards_margin of -301.

"result" : Boolean value. 1 if the home team won, 0 if the home team loses. This is the value the model attempts to predict.

Each data result is indexed by the Game ID that ESPN assigns to an individual game. For this game, ESPN assigned a Game ID of 401012884.

# 1.2: Pythagorean Wins
Location: pyth_wins/train_model.py and pyth_wins/pyth_wins.py

Run this command to get the model in the base directory of the repo:

```
python pyth_wins/train_model.py 2017.csv 2018_Edited.csv
```

And then for Pythagorean wins:

```
python pyth_wins/pyth_wins.py model_results.csv
```

The result of the model will be in the file "model_results.csv" in the base directory of the repo.