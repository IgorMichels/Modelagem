import pandas as pd

def catch_players(file, top):
    # return a list with top players' ID
    players = pd.read_csv(file, header = None, names = ['date', 'rank', 'id', 'points'])

    top_players = []
    for player in players.index:
        if player == top:
            break
        top_players.append(players.loc[player, 'id'])
        
    return top_players

def catch_games(file, top_players, surface):
    # return a dataframe with games of one year of top players in one surface
    games = pd.read_csv(file)
    
    col = ['surface', 'tourney_date', 'winner_id', 'loser_id', 'score', 'best_of',
           'winner_rank', 'winner_rank_points', 'loser_rank', 'loser_rank_points']

    for column in games:
        if column not in col:
            games.pop(column)

    for game in games.index:
        if (games.loc[game, 'winner_id'] not in top_players) or \
           (games.loc[game, 'loser_id'] not in top_players) or \
           (games.loc[game, 'surface'] != surface):
            games.drop(game, inplace = True)

    games.reset_index(inplace = True)
    games.pop('index')
    
    return games

def catch_all_games(files, rank, top, surface = 'Hard'):
    # return a dataframe with games of top players in one surface (default: hard)
    players = catch_players(rank, top)
    games = pd.DataFrame(columns = ['surface',
                                    'tourney_date',
                                     'winner_id',
                                     'loser_id',
                                     'score',
                                     'best_of',
                                     'winner_rank',
                                     'winner_rank_points',
                                     'loser_rank',
                                     'loser_rank_points'])

    for file in files:
        data = catch_games(file, players, surface)
        games = pd.concat([games, data])

    games.reset_index(inplace = True)
    games.pop('index')
    games.pop('surface')

    return games