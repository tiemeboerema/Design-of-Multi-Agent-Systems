# Do I Know You? The Effects of Agent Mobility and Ongoing Relationships on Trust and Market Formation

This repository provides contains the code for our report, extending the analysis of Macy and Sato (2002).

## Reproduction

To reproduce our results, follow the reproduction guide below.

First, clone the repository:
```
git clone https://github.com/tiemeboerema/Design-of-Multi-Agent-Systems
```

Navigate to the correct directory:
```
cd Design-of-Multi-Agent-Systems
```

Install required dependencies in venv using uv:
```
uv sync
```

To reproduce our results intended to reproduce the results of Macy and Sato (2002), run full_basic_run.py. It is expected that you run this from the project root directory.

```
uv run Codebase/full_basic_run.py
```

## Additions

We make two additions to the original model. The first is giving agents individual mobility propensities, allowing them to choose whether to move themselves, rather than having mobility as an experimental variable. The related analysis can be run as follows:

```
uv run Codebase/full_endogenous_run.py
```

Our other addition is the inclusion of agent memory. Due to the relatively large number of combinations of experimental parameters (11 mobilities, 10 neighborhood sizes, 20 memory sizes = 2200 experimental conditions) for which we perform 20 runs each, the original runs were performed on Habrok using the script main.sh in the Codebase/dispatch folder. Partial experiments can still be run locally as follows:

```
uv run Codebase/full_memory_run.py --mem_size {MEMORY_SIZE}
```

Where {MEMORY_SIZE} should be replaced with the desired memory size to use.


## Plotting

The numerous CSV files in the Codebase/Results directory can be converted into plots by running:

```
uv run Codebase/plotting.py
```

This outputs the following plots in order:

- Mobility values against trust measures.
- Neighborhood size values against trust measures.
- Neighborhood size values against trust measures, using endogenous mobility.
- Mobility values against trust measures, for different agent memory sizes.
- Mobility values against trust measures, using agent memory aggregates.
