import Config as cfg
import numpy as np
from tqdm import tqdm
from Modules import Setup
from Modules.Update import form_all_pairs, move_agents, resolve_all_pairs


def setup():
    agents = Setup.setup_agents()
    neighborhoods = Setup.setup_neighborhoods()
    Setup.initiate(agents, neighborhoods)
    return agents, neighborhoods


def run():
    mean_trust = np.zeros(cfg.RUNS)
    mean_market_entry = np.zeros(cfg.RUNS)
    mean_trust_strangers = np.zeros(cfg.RUNS)
    mean_mobility = np.zeros(cfg.RUNS)

    for run in range(cfg.RUNS):
        # Propensity to base trust on signal reading
        trust = np.zeros(cfg.POPULATION)

        # Proportion of agents that actually enter the market
        market_entry = np.zeros(cfg.ITERATIONS)

        # Proportion of agents that trusted and cooperated
        trust_strangers = np.zeros(cfg.ITERATIONS)

        # Propensity to move to another neighborhood
        mobility = np.zeros(cfg.POPULATION)

        agents, neighborhoods = setup()
        for i in range(cfg.ITERATIONS):
            move_agents(agents, neighborhoods)
            pairs = form_all_pairs(agents, neighborhoods)
            market_entry[i] = (sum(agent.in_market for agent in agents) / cfg.POPULATION)
            trust_strangers[i] = resolve_all_pairs(pairs, neighborhoods)

        # Collect trust propensities
        for agent in agents:
            trust[agent.id] = agent.p_trust
            mobility[agent.id] = agent.p_move
            
        mean_trust[run] = np.mean(trust)
        mean_market_entry[run] = np.mean(market_entry)
        mean_trust_strangers[run] = np.mean(trust_strangers) 
        mean_mobility[run] = np.mean(mobility)

    if cfg.MOVE_FREE:
        return mean_mobility, mean_trust, mean_market_entry, mean_trust_strangers
    return None, mean_trust, mean_market_entry, mean_trust_strangers


if __name__ == "__main__":
    run()
    # running here is random, running in main is not.
