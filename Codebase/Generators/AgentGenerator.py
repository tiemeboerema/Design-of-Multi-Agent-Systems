import Config as cfg
from Auxillary.Agent import Agent


class AgentGenerator:
    def __init__(self):
        self._id = 0

    def generate_agents(self, size=cfg.POPULATION):
        population = []
        for _ in range(size):
            population.append(self.generate_agent())
        return population

    def generate_agent(self):
        agent = Agent(self._id)
        self._id += 1
        return agent
