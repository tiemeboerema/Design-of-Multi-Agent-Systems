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
    mean_market = np.zeros(cfg.RUNS)
    mean_extra = None

    for run in range(cfg.RUNS):
        # Propensity to base trust on signal reading
        trust = np.zeros(cfg.POPULATION)

        # Propensity to leave the neighborhood and enter the open market
        market = np.zeros(cfg.POPULATION)

        # One more trust variable we care about
        extra = None

        agents, neighborhoods = setup()
        for i in range(cfg.ITERATIONS):
            move_agents(agents, neighborhoods)
            pairs = form_all_pairs(agents, neighborhoods)
            resolve_all_pairs(pairs, neighborhoods)

        # Collect data necessary for plotting
        for agent in agents:
            trust[agent.id] = agent.p_trust
            market[agent.id] = agent.p_market
        mean_trust[run] = np.mean(trust)
        mean_market[run] = np.mean(market)

    return mean_trust, mean_market


if __name__ == "__main__":
    run()
    # running here is random, running in main is not.
