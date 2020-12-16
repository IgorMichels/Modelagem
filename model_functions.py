from math import exp, log, sqrt
from scipy.optimize import minimize

def find_probability(player1, player2):
    # receives two vectors
    # (player1 = [param11, param 12] and player2 = [param21, param22])
    # returns the probability of player1 beating player2

    ai = player1[0]
    aj = player1[1]
    bi = player2[0]
    bj = player2[1]

    try:
        A = exp(bi * aj)
    except OverflowError:
        if bi * aj > 0:
            return 1 - 1e-6
        else:
            return 1e-6

    try:
        B = exp(bj * ai)
    except OverflowError:
        if bj * ai > 0:
            return 1 - 1e-6
        else:
            return 1e-6
        
    try:
        probability = A/(A + B)
    except ZeroDivisionError:
        return 1

    return probability

def find_parameter(probability):
    # receives the probability of player1 beating player2
    # returns the parameter

    aj = log(probability)
    bj = log(1 - probability)

    player1 = [1, aj]
    player2 = [1, bj]

    return player1, player2

def likelihood(players, results):
    # receives list of players and results
    # returns minus log-likelihood of results and players' parameters
    if type(players[0]) != list:
        list_players = []
        i = 0
        while i < len(players):
            list_players.append([players[i], players[i + 1]])
            i += 2

        players = list_players

    log_likelihood = 0

    for result in results:
        index1 = result[0]
        index2 = result[1]

        probability = find_probability(players[index1], players[index2])
        try:
            log_likelihood += log(probability)
        except ValueError:
            log_likelihood += 1

    return - log_likelihood
