from Experiment import run
from pathlib import Path
import pandas as pd
import csv
from tqdm import tqdm
import Config as cfg

MOBILITIES = range(0, 11)
SIZES = range(10, 110, 10)
RESULTS_PATH = Path("Codebase/Results")


def perform_full_run() -> None:
    """
    Performs 20 runs for each combination of mobility and neighborhood size
    and collects the resulting trust and market propensities in a CSV.
    """
    df = pd.DataFrame(columns=["Mobility", "Neighborhood Size", "Mean Trust", "Mean Market"])
    for mobil in tqdm(MOBILITIES):
        cfg.MOBILITY = mobil / 10
        for neigh_size in SIZES:
            cfg.NEIGHBORHOOD_SIZE = neigh_size
            trust, market = run()
            for val in range(cfg.RUNS):
                df.loc[len(df)] = [mobil / 10, neigh_size, trust[val], market[val]]
            df.to_csv(RESULTS_PATH / "default_results.csv", index=False)


def main() -> None:
    perform_full_run()


if __name__ == "__main__":
    main()