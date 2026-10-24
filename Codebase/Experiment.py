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

    for run in range(cfg.RUNS):
        # Propensity to base trust on signal reading
        trust = np.zeros(cfg.POPULATION)

        # Proportion of agents that actually enter the market
        market_entry = np.zeros(cfg.ITERATIONS)

        agents, neighborhoods = setup()
        for i in range(cfg.ITERATIONS):
            move_agents(agents, neighborhoods)
            pairs = form_all_pairs(agents, neighborhoods)
            market_entry[i] = (sum(agent.in_market for agent in agents) / cfg.POPULATION)
            resolve_all_pairs(pairs, neighborhoods)

        # Collect trust propensities
        for agent in agents:
            trust[agent.id] = agent.p_trust
            
        mean_trust[run] = np.mean(trust)
        mean_market_entry[run] = np.mean(market_entry)

    return mean_trust, mean_market_entry


if __name__ == "__main__":
    run()
    # running here is random, running in main is not.
