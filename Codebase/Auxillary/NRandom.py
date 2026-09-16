import random

import Config as cfg


def seed():
    if cfg.SEED is None:
        random.seed()
        return
    random.seed(cfg.SEED)
