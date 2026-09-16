import Config as cfg
from Modules import Setup
from Modules.Update import form_all_pairs, move_agents, resolve_all_pairs


def setup():
    agents = Setup.setup_agents()
    neighborhoods = Setup.setup_neighborhoods()
    Setup.initiate(agents, neighborhoods)
    return agents, neighborhoods


def run():
    for _ in range(cfg.RUNS):
        agents, neighborhoods = setup()

        for i in range(cfg.ITERATIONS):
            move_agents(agents, neighborhoods)
            pairs = form_all_pairs(agents, neighborhoods)
            resolve_all_pairs(pairs, neighborhoods)
            print(agents[-1])


if __name__ == "__main__":
    run()
    # running here is random, running in main is not.
