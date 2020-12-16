from math import exp, log, sqrt

def find_probability(player1, player2):
    # receives two vectors
    # (player1 = [param11, param 12] and player2 = [param21, param22])
    # returns the probability of player1 beating player2

    ai = player1[0]
    aj = player1[1]
    bi = player2[0]
    bj = player2[1]

    probability = exp(bi * aj)/(exp(bi * aj) + exp(bj * ai))

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
    
    log_likelihood = 0

    for result in results:
        index1 = result[0]
        index2 = result[1]

        probability = find_probability(players[index1], players[index2])
        log_likelihood += log(probability)

    return - log_likelihood
