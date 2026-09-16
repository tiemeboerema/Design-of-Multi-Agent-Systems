import random


class Agent:
    def __init__(self, agent_id):
        self.id = agent_id

        self.p_trust = random.random()
        self.p_cooperate = random.random()
        self.p_market = random.random()

        self.neighborhood_id = None

        self.in_market = False
        self.newcomer = False
        self.will_cooperate = None

        self.cumulative_payoff = 0.0

    def action_vector(self):
        return (self.p_trust, self.p_cooperate, self.p_market)

    # -- Generated using Claude --------------------------#
    def __repr__(self):
        return (
            f"Agent(id={self.id}, "
            f"p_trust={self.p_trust:.3f}, "
            f"p_cooperate={self.p_cooperate:.3f}, "
            f"p_market={self.p_market:.3f})"
            f"p_market={self.cumulative_payoff:.3f})"
        )

    # -- ---------------------- --------------------------#
