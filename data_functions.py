import pandas as pd
import numpy as np

def catch_players(file, top):
    # returns a list with top players' ID
    players = pd.read_csv(file, header = None, names = ['date', 'rank', 'id', 'points'])

    top_players = []
    for player in players.index:
        if player == top:
            break
        top_players.append(players.loc[player, 'id'])
        
    return top_players

def catch_games(file, top_players, surface, sets):
    # returns a dataframe with games of one year of top players in one surface
    games = pd.read_csv(file)
    
    col = ['surface', 'tourney_date', 'winner_id', 'loser_id', 'score', 'best_of',
           'winner_rank', 'winner_rank_points', 'loser_rank', 'loser_rank_points',
           'tourney_level']

    for column in games:
        if column not in col:
            games.pop(column)

    for game in games.index:
        if (games.loc[game, 'winner_id'] not in top_players) or \
           (games.loc[game, 'loser_id'] not in top_players) or \
           (games.loc[game, 'surface'] != surface) or \
           (games.loc[game, 'best_of'] != sets):
            games.drop(game, inplace = True)

    games.reset_index(inplace = True)
    games.pop('index')
    
    return games

def catch_all_games(files, rank, top, surface = 'Hard', sets = 3):
    # returns a dataframe with games of top players in one surface (default: hard)
    players = catch_players(rank, top)
    games = pd.DataFrame(columns = ['surface',
                                    'tourney_date',
                                    'tourney_level',
                                     'winner_id',
                                     'loser_id',
                                     'score',
                                     'best_of',
                                     'winner_rank',
                                     'winner_rank_points',
                                     'loser_rank',
                                     'loser_rank_points'])

    for file in files:
        data = catch_games(file, players, surface, sets)
        games = pd.concat([games, data], sort = False)

    games.reset_index(inplace = True)
    games.pop('index')
    games.pop('surface')
    games.pop('best_of')
    games = games.reindex(columns = ['tourney_date',
                                     'tourney_level',
                                     'score',
                                     'winner_id',
                                     'winner_rank',
                                     'winner_rank_points',
                                     'loser_id',
                                     'loser_rank',
                                     'loser_rank_points'])

    return games

def split_games(games):
    # split a dataframe
    players_id = []
    
    for game in games.index:
        if games.loc[game, 'winner_id'] not in players_id:
            players_id.append(games.loc[game, 'winner_id'])
        if games.loc[game, 'loser_id'] not in players_id:
            players_id.append(games.loc[game, 'loser_id'])
    
        games.loc[game, 'winner_id'] = players_id.index(games.loc[game, 'winner_id'])
        games.loc[game, 'loser_id']  = players_id.index(games.loc[game, 'loser_id'])

    sep = int(len(games.index)/2)
    games_fit  = games.iloc[:sep, :]
    games_test = games.iloc[sep:, :]
    
    for game in games_test.index:
        if (games_test.loc[game, 'winner_id'] > max(games_fit['winner_id'].max(), games_fit['loser_id'].max())) or \
           (games_test.loc[game, 'loser_id'] > max(games_fit['winner_id'].max(), games_fit['loser_id'].max())):
            games_test.drop(game, inplace = True)
        
    games_test.reset_index(inplace = True)
    games_test.pop('index')
    
    return games_fit, games_test, players_id

def catch_data(games, fit):
    # receives a dataframe with games and returns data to optimize
    players_id = []
    players = []
    results = []
    bounds = []
    
    if fit:
        games, trash, players_id = split_games(games)
    else:
        trash, games, players_id = split_games(games)
    
    for i in range(len(players_id)):
        players.append(np.random.random())
        players.append(np.random.random())
        bounds.append((0, None))
        bounds.append((None, None))
            
    for game in games.index:
        results.append([games.loc[game, 'winner_id'],
                        games.loc[game, 'loser_id']])
    
    if fit:
        return players_id, players, results, bounds, games
    else:
        return results, games
