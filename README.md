# NBA-Business-Analytics
Given a sample size of statistics from 460 games between two NBA seasons, created a complex algorithm in Python to correctly predict total international viewership of NBA games. Uses factors like team market size, day of the week, and number of all stars within the teams to help utilize the prediction algorithm. 

# Additional files
**game_data.csv**<br />
o This dataset includes incoming wins and losses (i.e., record going into a game), dates, and selected game stats for each game in the 2016-17 and 2017-18 season. <br />

**player_data.csv <br />**
o This dataset includes performance stats for each player in each game in the 2016-17 and 2017-18 seasons. It also includes indicators for whether the player was selected as an All-Star for the season in question and whether the player was active for the game. Game statistics are only included for games in the training set – not in the test set. All-Star status and active vs. inactive status is provided for all games. <br />

**training_set.csv <br />**
o This dataset includes total viewership for each international country for each game in the 2016-17 and 2017-18 seasons. Included are 1,000 games from each season. <br />

**predictions.csv <br />**
o This dataset includes a list of games in the 2016-17 and 2017-18 seasons for which we predicted total international viewership (i.e., the sum across all countries). Included are 230 games from each season. <br />

# The Process
In determining the viewership numbers for the given games, the factors @gct38 and I decided to consider were day of the week, number of all stars in the game, average win percentage of the two teams playing, market size, and number of superstars. <br /> <br />
For day of the week, we gave weekend games (including friday) a higher multiplier, as well as Christmas day and opening weekend as those are popular days for the NBA. <br /> <br />
For number of all-stars, the more all-stars that were playing, the higher multiplier used. <br /> <br />
For win percentage, the higher the average win percentage, the higher the multiplier used in the algorithm. If both teams were under a win percentage of 35% , they would be penalized further. <br /> <br />
For market size, each market is ranked as 1, 2, or 3, 3 being a large market, 1 being a small market. If both markets were 3, there would be a large multiplier. If the average market was >= 2, there was an average multiplier, and a low one if the combination was any lower than 2. <br /> <br />
For number of superstars, which is if the player was in the top 15 in jersey sales for the given season, the more superstars meant a higher multiplier. <br /> <br />

Once we got all of the multipliers (a percentage) for a certain game, each multiplier was applied to each country's highest viewership total and added together. <br />
This was repeated for every country to acquire the total viewership for a specific game and repeated for 460 different games. <br />

# Resources
NBA 2K18 (team market sizes(listed as small, medium, and large in game))

Resources used for our "Superstar Category": <br />
http://www.nba.com/article/2018/04/17/stephen-curry-golden-state-warriors-lead-most-popular-merchandise-list-2017-18
http://www.nba.com/article/2017/04/11/nba-most-popular-jersey-sales-2016-17-regular-season

Resources used to get team records, start/end dates of season: <br />
https://en.wikipedia.org/wiki/2016%E2%80%9317_NBA_season#Regular_season
https://en.wikipedia.org/wiki/2017%E2%80%9318_NBA_season
