import Config as cfg
import pandas as pd
import csv

from Experiment import run
from pathlib import Path
from tqdm import tqdm

SIZES = range(10, 110, 10)
RESULTS_PATH = Path("Codebase/Results")


def perform_endogenous_mobility_run() -> None:
    """
    Performs 20 runs for all neighborhood sizes and collects the resulting
    means of mobility, trust, market propensities, and stranger trust in a CSV.
    """
    cfg.MOVE_FREE = True
    cfg.USE_MEMORY = False

    df = pd.DataFrame(columns=["Neighborhood Size", "Mean Mobility", "Mean Trust", "Mean Market", "Mean Trust Strangers"])
    for neigh_size in tqdm(SIZES):
        cfg.NEIGHBORHOOD_SIZE = neigh_size
        mobility, trust, market, trust_strangers = run()
        for val in range(cfg.RUNS):
            df.loc[len(df)] = [neigh_size, mobility[val], trust[val], market[val], trust_strangers[val]]
        df.to_csv(RESULTS_PATH / "endogenous_mobility_results2.csv", index=False)


def main() -> None:
    perform_endogenous_mobility_run()


if __name__ == "__main__":
    main()
