import random

import Config as cfg
from Auxillary.AgentReadings import will_play
from Auxillary.Payoffs import opportunity_cost, payoff
from Auxillary.Reinforcement import reinforce


def move_agents(agents, neighborhoods):
    for agent in agents:
        if not agent.in_market:
            agent.newcomer = False
        if random.random() < cfg.MOBILITY:
            current_neighborhood = neighborhoods[agent.neighborhood_id]
            current_neighborhood.remove_agent(agent)

            other_neighborhoods = []  # -> claude looked into the codebase and noticed that agents cant move back to their own neighborhood
            for neighborhood in neighborhoods:
                if neighborhood.id != current_neighborhood.id:
                    other_neighborhoods.append(neighborhood)

            new_neighborhood = random.choice(other_neighborhoods)
            new_neighborhood.add_agent(agent)
            agent.newcomer = True
            agent.neighborhood_id = new_neighborhood.id


def try_market(agents):
    for agent in agents:
        agent.in_market = (
            random.random() < agent.p_market
        )  # Mind that here we set the agents to neighbors if they dont try the market implicitly.


def decide_cooperation(agents):
    for agent in agents:
        agent.will_cooperate = (
            random.random() < agent.p_cooperate
        )  # delete# low cooperation means high chance of defecting.


def form_pools(agents, neighborhoods):
    market_pool = []
    for agent in agents:
        if agent.in_market:
            market_pool.append(agent)

    neighborhood_pools = {}
    for neighborhood in neighborhoods:
        neighborhood_pools[neighborhood.id] = []

    for agent in agents:
        if not agent.in_market:
            neighborhood_pools[agent.neighborhood_id].append(agent)

    return market_pool, neighborhood_pools


def pair_in_pool(pool):
    shuffled = pool.copy()  # delete# I am sadly not very familiar with objects, .copy was added by copilot when writing, is this the way to go?
    random.shuffle(shuffled)

    pairs = []
    for i in range(
        0, len(shuffled) - 1, 2
    ):  # This trick ensures that odd agents are left unpaired for the tick implicitly.
        pairs.append((shuffled[i], shuffled[i + 1]))
    return pairs


# -- Adjusted using Claude --------------------------#
def form_all_pairs(agents, neighborhoods):
    try_market(agents)
    decide_cooperation(agents)
    market_pool, neighborhood_pools = form_pools(agents, neighborhoods)

    all_pairs = []
    for agent_1, agent_2 in pair_in_pool(market_pool):
        all_pairs.append((agent_1, agent_2, len(market_pool)))

    for neighborhood in neighborhoods:
        pool = neighborhood_pools[neighborhood.id]
        for agent_1, agent_2 in pair_in_pool(
            neighborhood_pools[neighborhood.id]
        ):
            all_pairs.append((agent_1, agent_2, neighborhood.size()))

    return all_pairs


# -- ---------------------- --------------------------#


def score_pair(agent, partner, n):
    played, agent_used_signal, partner_used_signal = will_play(
        agent, partner, agent.in_market
    )

    O = opportunity_cost(n, cfg.POPULATION, cfg.HETEROGENEITY)
    payoff_agent, payoff_partner = payoff(
        played, agent.will_cooperate, partner.will_cooperate, O
    )

    agent.cumulative_payoff += payoff_agent
    partner.cumulative_payoff += payoff_partner

    return (
        played,
        agent_used_signal,
        partner_used_signal,
        payoff_agent,
        payoff_partner,
    )


# -- Generated using Claude --------------------------#
def find_role_models(neighborhoods):
    """Per neighbourhood, the member with the highest cumulative_payoff --
    confirmed against mod_learning.f90's localBest/localMaxPayoff. Uses
    each agent's home neighbourhood (neighborhood_id), matching PermAddress.
    Returns {neighborhood_id: agent_or_None (None if the neighbourhood is
    currently empty)}."""
    role_models = {}

    for neighborhood in neighborhoods:
        best_agent = None
        for agent in neighborhood.members:
            if (
                best_agent is None
                or agent.cumulative_payoff > best_agent.cumulative_payoff
            ):
                best_agent = agent
        role_models[neighborhood.id] = best_agent

    return role_models


def social_learn(agent, role_model):
    """Component-wise imitation -- confirmed against mod_learning.f90:
    each of the three propensities gets its own independent coin flip,
    50/50 chance to copy that single value from the role model. Not a
    full copy of the whole action vector at once."""
    if random.random() < 0.5:
        agent.p_cooperate = role_model.p_cooperate
    if random.random() < 0.5:
        agent.p_market = role_model.p_market
    if random.random() < 0.5:
        agent.p_trust = role_model.p_trust


def learn(agent, agent_payoff, used_signal, played, role_models):
    """The either/or gate from mod_learning.f90: an agent either
    reinforces from its own experience, or imitates its neighbourhood's
    role model -- never both in the same tick."""
    role_model = role_models[agent.neighborhood_id]

    if (
        role_model is None
        or role_model.cumulative_payoff <= agent.cumulative_payoff
    ):
        if played:
            agent.p_cooperate = reinforce(
                agent.p_cooperate, agent.will_cooperate, agent_payoff
            )
        agent.p_trust = reinforce(agent.p_trust, used_signal, agent_payoff)
        agent.p_market = reinforce(
            agent.p_market, agent.in_market, agent_payoff
        )

    elif not role_model.newcomer:
        social_learn(agent, role_model)


# -- ---------------------- --------------------------#


def resolve_all_pairs(pairs, neighborhoods):
    scored = []
    for agent, partner, n in pairs:
        result = score_pair(agent, partner, n)
        scored.append((agent, partner, *result))

    role_models = find_role_models(neighborhoods)

    for (
        agent,
        partner,
        played,
        agent_used_signal,
        partner_used_signal,
        payoff_agent,
        payoff_partner,
    ) in scored:
        learn(agent, payoff_agent, agent_used_signal, played, role_models)
        learn(
            partner, payoff_partner, partner_used_signal, played, role_models
        )
