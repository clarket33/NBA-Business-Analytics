##PREDICTION ALGORITHM###
#Factors:
#  1) day of week
#  2) # of all stars
#  3) win percentage
#  4) market size
#  5) # of superstars


#import csv module so we can read/write csv
#import datetime to help find day of week
import csv
import datetime


#parses the data files
def parsing(filename):
    #creation of empty list first
    file = list()
    #opening the csv data file
    with open(filename, newline = '') as csvfile:
        reading = csv.reader(csvfile)
        for row in reading:
            temp = list(row)
            file.append(temp)
    return file

#given a date, compute the day of the week using datetime module and date class
#date is given in MM/DD/YYYY format
def day(date):
    a = date.split('/')
    day_of_week = datetime.date(int(a[2]), int(a[0]), int(a[1])).strftime("%A")
    return day_of_week


#helper function, will raise/lower the 
#percentages for certain dates
def dateStats(date):
    if date[0:5] == "12/25":
        return .25
    elif date[0:10] == "10/25/2016":
        return .20
    elif date[0:10] == "10/26/2016" or date[0:10] == "10/27/2016" or \
         date[0:10] == "10/28/2016" or date[0:10] == "10/29/2016" or date[0:10] == "10/30/2016":
        return .1
    elif date[0:10] == "10/17/2017":
        return .20
    elif date[0:10] == "10/18/2017" or date[0:10] == "10/19/2017" or \
         date[0:10] == "10/20/2017" or date[0:10] == "10/21/2017" or date[0:10] == "10/22/2017":
        return .05    
    else:
        return 0.0

#helper function to training_predictions function
#returns a percentage for every day
def day_percentage(day):
    if day == "Sunday":
        return 0.03    # +3% for a Sunday game
    elif day == "Monday":
        return -0.02    # -2% for Monday games
    elif day == "Tuesday":
        return -0.02     # -2% for Tuesday games
    elif day == "Wednesday":
        return -0.02     # -2% for Wednesday games
    elif day == "Thursday":
        return -0.02     # -2% for Thursday games
    elif day == "Friday":
        return 0.01     # +1% for Friday games
    elif day == "Saturday":
        return 0.03     # +3% for Saturday games
    
#helper function to training_predictions function
def wins(win_loss):
    #if the win percentage is less than 35%, penalize the game
    if win_loss < .35:
        return (win_loss-.2)/10
    return (win_loss) / 10
    

#helper function to training_predictions function
#adds viewers due to market sizes, bigger markets = more views
def market(market_size):
    if market_size < 2:
        return -0.01
    elif market_size <= 2.9:
        return 0.02
    elif market_size > 2.9:
        return 0.04

#aid in error checking
#how this will get graded
#percent error of all the games combined
def mape(game_predictions):
    num_games = 0
    error = 0
    for game in game_predictions:
        num_games += 1
        error += abs(game_predictions[game][0] - game_predictions[game][1])/game_predictions[game][0]
    error *= (1/num_games)
    return error

#percent error of each game, outputted to csv file
#outputted to csv in same order as the games that occur
def mape_per(game_predictions, training, games):
    #create a list so that when outputting to csv, will be in same order as the games that occur
    item = list()
    for line in training:
        if line[0] == "Season": 
            continue
        if line[1] not in item:
            item.append(line[1])
    
    
    file = open('training_set_percent_errors.csv', 'w')
    file.write("% Error, Actual, Prediciton, Game ID, Season, Date, Day of Week, # All Stars, Team 1, Team 2, Market Tier, Winningest %, # Superstars\n")
    for game in item:
        error = abs(game_predictions[game][0] - game_predictions[game][1])/game_predictions[game][0]
        file.write("{:.3f} %, {}, {}, {}, {}\n".format(error*100, str(game_predictions[game][0]), str(game_predictions[game][1]), game, games[game]))
    file.close()

#creates dictionary
#keys: game ids
#values: list
def create_dict(game_data):
    games = dict()
    for line in game_data:
        #skip the header line
        if line[1] == "Game_ID":
            continue
        #if game id isn't a key yet, create the game id and corresponding list as values
        if line[1] not in games:
            games[line[1]] = [line[0], line[2], day(line[2]), 0]
    return games



#all stars by team
#doesn't account for whether or not they're active/inactive
#returns a dict keys: team name
#values: # of all stars on that team for each season (a list)
#        0th index: 2016-17 season
#        1st index: 2017-18 season
def all_stars_team(player_list):
    teams = dict()
    spot = 0
    season = "2016-17"
    used = list()
    for line in player_list:
        #skip the header line
        if line[1] == "Game_ID":
            continue
        if(season != line[0]):
            spot = 1
            used.clear()
        season = line[0]        
        #if team isn't an entry in dict yet, create entry
        if line[3] not in teams:
            teams[line[3]] = [0,0]
            
        #if the player is an all star and is the same game
        if line[6] != "None" and (line[5] not in used):
            teams[line[3]][spot] += 1
            used.append(line[5])    
    return teams

#creates a dictionary with every country's highest viewing total
#stored
def highestViewers(countries, highestViews):
    for country in countries:
        maxVal = 0
        for game in countries[country]:
            if countries[country][game][1] > maxVal:
                maxVal = countries[country][game][1]
        highestViews[country] = maxVal

#adding entries to dictionaries season1 and season2
#keys: team name
#values: list [win percentage, # of superstars on the team]
#number of superstars calculated from top15 jersey sales 
#for each season courtesy of nba.com
def seasonStats(filename, season1, season2):
    #opening the csv data file
    with open(filename, newline = '') as csvfile:
        reading = csv.reader(csvfile)
        for row in reading:
            season1[row[0]] = [row[1], row[3]]
            season2[row[0]] = [row[2], row[4]]

#creating a dict by with games played broadcasted by country
def country_dict(training, games):
    countries = dict()
    for line in training:
        if line[1] == "Game_ID":
            continue        
        countries[line[5]] = dict()
    for line in training:
        if line[1] == "Game_ID":
            continue
        countries[line[5]][line[1]] = (games[line[1]], int(line[6]))
    return countries
            
#adding the market tiers to market dict
def market_tiers():
    ''' Market Size Dictionary (Large = 3, Medium = 2, Small = 1)
        Market Sizes retrieved from NBA 2k18'''
    markets = dict()
    markets['DEN'] = 2
    markets['SAC'] = 2
    markets['MIN'] = 2
    markets['SAS'] = 2    
    markets['POR'] = 2
    markets['IND'] = 2
    markets['ORL'] = 2
    markets['MIA'] = 2     
    markets['MIL'] = 2
    markets['CHA'] = 2
    markets['CLE'] = 2
    markets['HOU'] = 3    
    markets['LAC'] = 3
    markets['PHX'] = 3
    markets['LAL'] = 3
    markets['GSW'] = 3  
    markets['DAL'] = 3
    markets['CHI'] = 3
    markets['PHI'] = 3
    markets['DET'] = 3    
    markets['BKN'] = 3
    markets['NYK'] = 3
    markets['BOS'] = 3
    markets['ATL'] = 3     
    markets['WAS'] = 3
    markets['TOR'] = 3
    markets['NOP'] = 1
    markets['OKC'] = 1    
    markets['UTA'] = 1
    markets['MEM'] = 1    
    return markets





#this function will edit a dict for every game in player_list file
#gives the number of all stars playing in that game
def addAllStars(player_list, games):
    #going thru player_data file line by line
    for line in player_list:
        #make sure not at the first line
        if line[1] == "Game_ID":
            continue
        #checking if that player is an all star
        #3rd index of the list and increment it by 1 if all star is for the game
        if line[6] != "None":
            games[line[1]][3] += 1

#adds the teams that are playing in the game
#to the games dictionary
def addTeams(games, game_data):
    count = 0
    team1 = None
    for game in game_data:
        if game[3] == 'Team':
            continue
        if count % 2 == 0:
            team1 = game[3]
        else:
            games[game[1]].append((team1, game[3]))
        count+=1
        
#adds the size of the largest market in the game to the data
def addMarkets(games, markets):
    for game in games:
        market1 = markets[games[game][4][0]]
        market2 = markets[games[game][4][1]]
        games[game].append(float((market1 + market2))/2)

#will use the dictionaries of season1 and season2 stats 
#and append them to end of each entry in games dict
#adding in the average of the two winning percentages
#adding the total # of superstars between the two teams
def addStats(games, season1, season2):
    for key in games:
        #depending on which season the game is played in, will either use season1 or season2 dict
        if games[key][0] == "2016-17":
            percent1 = float(season1[games[key][4][0]][0])
            percent2 = float(season1[games[key][4][1]][0])
            games[key].append((percent1 + percent2)/2)            
            games[key].append(int(season1[games[key][4][0]][1]) + int(season1[games[key][4][1]][1]))
        elif games[key][0] == "2017-18":
            percent1 = float(season2[games[key][4][0]][0])
            percent2 = float(season2[games[key][4][1]][0])
            games[key].append(max(percent1, percent2))              
            games[key].append(int(season2[games[key][4][0]][1]) + int(season2[games[key][4][1]][1]))


#will predict using given data from training_set
#and will then check with results from training_set
def training_predictions(countries, highestViews, training):
    #game_predictions is a dict; key: game_id; value: [actual, predict]    
    game_predictions = dict()
    
    #index 0 of every value in game_predictions
    #adding the actual # of viewers
    for item in training:
        #skip header line
        if item[0] == "Season":
            continue
        #finds the sum of views by country for every game in training_set
        if item[1] not in game_predictions:
            game_predictions[item[1]] = [0,0]
        game_predictions[item[1]][0] += int(item[6])    
    
    #index 1 of every value in game_predictions
    #adding predicted # of viewers
    for key in countries:
        for game_id in countries[key]:
            highest_views_country = highestViews[key]
            date = countries[key][game_id][0][1]
            day_of_week = countries[key][game_id][0][2]
            superstars = countries[key][game_id][0][7]
            all_stars = countries[key][game_id][0][3]
            win_loss = countries[key][game_id][0][6]
            market_size = countries[key][game_id][0][5]
    
            #each of our 5 factors that will help determine our prediction
            percent_day = day_percentage(day_of_week) * highest_views_country
            percent_allstars = (0.01 * highest_views_country) * all_stars #10% for every all star
            percent_wins = wins(win_loss) * highest_views_country
            percent_market = market(market_size) * highest_views_country
            percent_superstars = (.03 * highest_views_country) * superstars # +10% for every superstar
            percent_date = dateStats(date) * highest_views_country
            
            total_views = (.2*percent_day) + (1*percent_allstars) + (.8*percent_wins) + (.6* percent_market) + (1 * percent_superstars) + (1*percent_date)
            
            if game_id not in game_predictions:
                game_predictions[game_id] = [0,0]
            game_predictions[game_id][1] += round(total_views) 
    return game_predictions


#now we'll 
def test_predictions(teams, season1_stats, season2_stats, markets, highestViews, countries):
    #prediction on the test set file
    test_set = parsing('test_set.csv')
    test_predictions = dict()
    for key in countries:
        for line in test_set:
            country_best = highestViews[key]
            date = line[2]
            if(date == 'Game_Date'):
                continue
            curDay = day(date)
            if date == '2016-17':
                all_stars = teams[line[3]][0] + teams[line[4]][0]
                superstars = int(season1_stats[line[3]][1] + int(season1_stats[line[4]][1]))
                win_p = (float(season1_stats[line[3]][0]) + float(season1_stats[line[4]][0]))/2
            else:
                all_stars = teams[line[3]][1] + teams[line[4]][1]
                superstars = int(season2_stats[line[3]][1]) + int(season2_stats[line[4]][1])
                win_p = (float(season2_stats[line[3]][0]) + float(season2_stats[line[4]][0]))/2
            market_size = (markets[line[3]] + markets[line[4]]) / 2
            
            #each of our 5 factors that will help determine our prediction
            percent_day = day_percentage(curDay) * country_best
            percent_allstars = (0.01 * country_best) * all_stars #+1% for every all star
            percent_wins = wins(win_p) * country_best
            percent_market = market(market_size) * country_best
            percent_superstars = (.03 * country_best) * superstars # +3% for every superstar
            percent_date = dateStats(date) * country_best
            

            total_views = (.2*percent_day) + (1*percent_allstars) + (.8*percent_wins) + (.6* percent_market) + (1 * percent_superstars) + (1*percent_date)
            
            game_id = line[1]
            if game_id not in test_predictions:
                test_predictions[game_id] = 0
            test_predictions[game_id] += round(total_views)  
    return test_predictions



#output function writing to csv file
def output(test_file, test_predictions):
    #opening output file
    file = open('test_set_[Infinity_Gauntlets].csv', 'w')
    #opening the csv test_file data file
    with open(test_file, newline = '') as csvfile:
        reading = csv.reader(csvfile)
        for row in reading:
            if row[0] == "Season":
                for item in row:
                    file.write(item)
                    file.write(",")
                file.write("\n")
                continue
            game_id = row[1]
            for item in row:
                if item == "":
                    file.write(str(test_predictions[game_id]))
                    break
                file.write(item)
                file.write(",")
            file.write("\n")
    file.close()


#MAIN code
if __name__ == "__main__":
    #every csv file parsed into a list of lists
    #like 2D vector
    #first entry is a list of data on the entire line
    #second entry is every item of data on each line
    game_data = parsing('game_data.csv')
    player = parsing('player_data.csv')
    training = parsing('training_set.csv')
    test = parsing('test_set.csv')

    #games: parent dict
    #keys: game ids
    #values: list
    #        0th index: season
    #        1st index: dates of games played
    #        2nd index: day of the week
    #        3rd index: # of total all stars between two teams
    #        4th index: teams played
    #        5th index: market tier (1 for small, 2 for medium, 3 for large)
    #        6th index: higher winning % between the two teams
    #        7th index: # of superstars within both teams (decided by being in top15 jerseys sold)
    games = create_dict(game_data)
    addAllStars(player, games)
    addTeams(games, game_data)

    markets = market_tiers()
    addMarkets(games, markets)
    teams = all_stars_team(player)
    
    
    #setting up a dictionarys for win percentage and # of superstars of every team in 2 seasons
    #will add these stats to each game in games dictionary
    #season1_stats = 2016-17 season
    #season2_stats = 2017-18 season
    season1_stats = dict()
    season2_stats = dict()
    seasonStats('NBA_Team_Stats_2016-17_to_2017-18.csv', season1_stats, season2_stats)
    addStats(games, season1_stats, season2_stats)
    
    countries = country_dict(training, games)
    highestViews = dict()
    highestViewers(countries, highestViews)    
    
    game_predictions = training_predictions(countries, highestViews, training)
    error = mape(game_predictions)
    mape_per(game_predictions, training, games)
                
                
    output('test_set.csv', test_predictions(teams, season1_stats, season2_stats, markets, highestViews, countries))