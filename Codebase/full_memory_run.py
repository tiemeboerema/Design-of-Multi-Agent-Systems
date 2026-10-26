import Config as cfg
import pandas as pd
import csv

from Experiment import run
from pathlib import Path
from tqdm import tqdm

MOBILITIES = range(0, 11)
SIZES = range(10, 110, 10)
MEMORY_SIZES = range(0, 5)
RESULTS_PATH = Path("Codebase/Results")


def perform_memory_run() -> None:
    """
    Performs 20 runs for each combination of mobility, neighborhood size, and memory size
    and collects the resulting trust and market propensities in a CSV.
    """
    df = pd.DataFrame(columns=["Mobility", "Neighborhood Size", "Memory Size", "Mean Trust", "Mean Market", "Mean Trust Strangers"])
    for mobil in tqdm(MOBILITIES):
        cfg.MOBILITY = mobil / 10
        for neigh_size in SIZES:
            cfg.NEIGHBORHOOD_SIZE = neigh_size
            for mem_size in MEMORY_SIZES:
                cfg.MEMORY_SIZE = mem_size
                print(f"Running for mobility={cfg.MOBILITY}, neighborhood size={cfg.NEIGHBORHOOD_SIZE}, memory size={cfg.MEMORY_SIZE}")
                trust, market, trust_strangers = run()
                for val in range(cfg.RUNS):
                    df.loc[len(df)] = [mobil / 10, neigh_size, mem_size, trust[val], market[val], trust_strangers[val]]
            df.to_csv(RESULTS_PATH / "memory_results.csv", index=False)


def main() -> None:
    perform_memory_run()


if __name__ == "__main__":
    main()