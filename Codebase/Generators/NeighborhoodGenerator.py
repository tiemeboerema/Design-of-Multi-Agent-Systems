import Config as cfg
from Auxillary.Neighborhood import Neighborhood


class NeighborhoodGenerator:
    def __init__(self):
        self._id = 0

    def generate_neighborhoods(self, count=cfg.N_NEIGHBORHOODS):
        neighborhoods = []
        for _ in range(count):
            neighborhoods.append(self.generate_neighborhood())
        return neighborhoods

    def generate_neighborhood(self):
        neighborhood = Neighborhood(self._id)
        self._id += 1
        return neighborhood
