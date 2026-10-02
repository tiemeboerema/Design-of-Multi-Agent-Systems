SEED = 42

POPULATION = 1000
NEIGHBORHOOD_SIZE = 10
N_NEIGHBORHOODS = POPULATION // NEIGHBORHOOD_SIZE


MOVE_FREE = True #if true, agents can decide how to move, otherwise it uses the original mobility parameter
MOBILITY = 0.1

HETEROGENEITY = 0.2

ITERATIONS = 10000
RUNS = 1


#Prisoners Dilemma Payoffs
REWARD = 0.7
TEMPTATION = 1.0
SUCKER = -0.5
PUNISHMENT = -0.2
EXIT = -0.2