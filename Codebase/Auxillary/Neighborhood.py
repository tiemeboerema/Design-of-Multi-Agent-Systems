class Neighborhood:
    def __init__(self, neighborhood_id):
        self.id = neighborhood_id
        self.members = []

    def add_agent(self, agent):
        self.members.append(agent)
        agent.neighborhood_id = self.id

    def remove_agent(self, agent):
        self.members.remove(agent)
        agent.neighborhood_id = None

    def size(self):
        return len(self.members)

    def __repr__(self):
        return f"Neighborhood(id={self.id}, size={self.size()})"
