import Config as cfg


def opportunity_cost(n, N=cfg.POPULATION, h=cfg.HETEROGENEITY):
    return 1 - ((n - 1) / (N - 1)) ** h


def payoff(played, agent_cooperate, partner_cooperate, O):
    if not played:
        return cfg.EXIT, cfg.EXIT
    elif agent_cooperate and partner_cooperate:
        return cfg.REWARD - O, cfg.REWARD - O
    elif not agent_cooperate and not partner_cooperate:
        return cfg.PUNISHMENT, cfg.PUNISHMENT
    elif agent_cooperate and not partner_cooperate:
        return cfg.SUCKER, cfg.TEMPTATION - O
    else:
        return cfg.TEMPTATION - O, cfg.SUCKER
