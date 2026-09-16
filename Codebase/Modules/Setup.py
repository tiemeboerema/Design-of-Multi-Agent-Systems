import random

from Generators.AgentGenerator import AgentGenerator
from Generators.NeighborhoodGenerator import NeighborhoodGenerator


def setup_agents():
    return AgentGenerator().generate_agents()


def setup_neighborhoods():
    return NeighborhoodGenerator().generate_neighborhoods()


def initiate(agents, neighborhoods):
    for agent in agents:
        neighborhood = random.choice(neighborhoods)
        neighborhood.add_agent(agent)
        agent.neighborhood_id = neighborhood.id
