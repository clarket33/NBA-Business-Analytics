# NBA-Business-Analytics
Given a sample size of statistics from 1000 games between two NBA seasons, the task at hand was to analyze the viewership numbers from the given games and develop an algorithm to predict the viewership numbers of 460 different games, also taking place in those two seasons. Given the data, my partner on the project, @gct38, and I analyzed the different factors that drive up viewership in NBA games in order to arrive at our final predictions.

# The Process
In determining the viewership numbers for the given games, the factors @gct38 and I decided to consider were the day of the week, the number of all stars in the game, the average win percentage of the two teams playing, the average market size between the two teams, and the number of superstars in the game. <br /> <br />
Each factor would make up a small percentage that would be applied to a country's highest viewership total, then added together to get total views for that country.<br /> <br />
The criteria for determining the percentage of each factor is as follows: <br /><br />
-For day of the week, we gave weekend games (including friday) a higher percentage, as well as Christmas day and opening weekend as those are popular days for the NBA. <br /> <br />
-For number of all-stars, the more all-stars that were playing, the higher percentage used. <br /> <br />
-For win percentage, the higher the average win percentage, the higher the percentage used in the algorithm. If both teams were under a win percentage of 35% , they would be penalized further. <br /> <br />
-For market size, each market is ranked as 1, 2, or 3, 3 being a large market, 1 being a small market. If both markets were 3, there would be a large percentage applied. If the average market was >= 2, there was an average percentage applied, and a low one if the combination was any lower than 2. <br /> <br />
-For number of superstars, which is if the player was in the top 15 in jersey sales for the given season, the more superstars meant a higher percentage. <br /> <br />
After a viewership number was arrived at for a certain game for a certain country,
the percentages were applied for every country and added together to acquire the total international viewership for a specific game. We then repeated the process for 460 different games. <br />

# Additional files
**game_data.csv**<br />
o This dataset includes incoming wins and losses (i.e., record going into a game), dates, and selected game stats for each game in the 2016-17 and 2017-18 season. <br />

**player_data.csv <br />**
o This dataset includes performance stats for each player in each game in the 2016-17 and 2017-18 seasons. It also includes indicators for whether the player was selected as an All-Star for the season in question and whether the player was active for the game. Game statistics are only included for games in the training set – not in the test set. All-Star status and active vs. inactive status is provided for all games. <br />

**training_set.csv <br />**
o This dataset includes total viewership for each international country for each game in the 2016-17 and 2017-18 seasons. Included are 1,000 games from each season. <br />

**predictions.csv <br />**
o This dataset includes a list of games in the 2016-17 and 2017-18 seasons for which we predicted total international viewership (i.e., the sum across all countries). Included are 230 games from each season. <br />

# Resources
NBA 2K18 (team market sizes(listed as small, medium, and large in game))

Resources used for our "Superstar Category": <br />
http://www.nba.com/article/2018/04/17/stephen-curry-golden-state-warriors-lead-most-popular-merchandise-list-2017-18
http://www.nba.com/article/2017/04/11/nba-most-popular-jersey-sales-2016-17-regular-season

Resources used to get team records, start/end dates of season: <br />
https://en.wikipedia.org/wiki/2016%E2%80%9317_NBA_season#Regular_season
https://en.wikipedia.org/wiki/2017%E2%80%9318_NBA_season
