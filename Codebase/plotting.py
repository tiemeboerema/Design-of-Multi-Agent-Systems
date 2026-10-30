import pandas as pd
import numpy as np
from scipy.stats import t
from pathlib import Path
import matplotlib.pyplot as plt

def aggregate_with_ci_mult(data: pd.DataFrame, group_cols: str | list[str], outcome_cols: dict) -> pd.DataFrame:
    """
    Calculate means and 95% confidence intervals for each group.

    group_cols: column or list of columns to group by.
    outcome_cols: mapping from source column names to plot names.
    """
    if isinstance(group_cols, str):
        group_cols = [group_cols]

    rows = []

    for group_values, group in data.groupby(group_cols):
        if len(group_cols) == 1:
            group_values = (group_values,)

        row = dict(zip(group_cols, group_values))

        for source_col, plot_col in outcome_cols.items():
            values = group[source_col].dropna()
            n = len(values)
            mean = values.mean()

            if n > 1:
                se = values.std(ddof=1) / np.sqrt(n)
                margin = t.ppf(0.975, df=n - 1) * se
                lower = max(0, mean - margin)
                upper = min(1, mean + margin)
            else:
                lower = np.nan
                upper = np.nan

            row[f'{plot_col}_mean'] = mean
            row[f'{plot_col}_lower'] = lower
            row[f'{plot_col}_upper'] = upper

        rows.append(row)

    return pd.DataFrame(rows)

def aggregate_with_ci(data: pd.DataFrame, group_col: str, outcome_cols: dict) -> pd.DataFrame:
    """
    Calculate means and 95% confidence intervals for each group.

    outcome_cols: mapping from source column names to plot names.
    """
    rows = []

    for group_value, group in data.groupby(group_col):
        row = {group_col: group_value}

        for source_col, plot_col in outcome_cols.items():
            values = group[source_col].dropna()
            n = len(values)
            mean = values.mean()

            if n > 1:
                se = values.std(ddof=1) / np.sqrt(n)
                margin = t.ppf(0.975, df=n - 1) * se
                lower = max(0, mean - margin)
                upper = min(1, mean + margin)
            else:
                lower = np.nan
                upper = np.nan

            row[f'{plot_col}_mean'] = mean
            row[f'{plot_col}_lower'] = lower
            row[f'{plot_col}_upper'] = upper

        rows.append(row)

    return pd.DataFrame(rows)

def create_plot(title: str, data: pd.DataFrame, selected_var: str, xbottom: int, xtop: int) -> None:
    """
    Plot means and 95% confidence interval bands.
    """
    outcomes = {
        'Trust': ('Reading Signals', 'o'),
        'Trust Strangers': ('Trust Strangers', '^'),
        'Market': ('Market Size', 's'),
    }

    if 'Mobility_self_mean' in data.columns:
        outcomes['Mobility_self'] = ('Mobility', 'v')

    for col, (label, marker) in outcomes.items():
        mean = data[f'{col}_mean'].to_numpy()
        lower = data[f'{col}_lower'].to_numpy()
        upper = data[f'{col}_upper'].to_numpy()
        x = data[selected_var].to_numpy()

        line, = plt.plot(x, mean, marker=marker, markersize=8, label=label)
        plt.fill_between(x, lower, upper, color=line.get_color(), alpha=0.25, linewidth=0)

    plt.title(title)
    plt.xlabel(selected_var)
    plt.ylabel('Means')
    plt.xlim(xbottom, xtop)
    plt.ylim(0, 1)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()


def plot_mobility(data: pd.DataFrame) -> None:
    outcome_cols = {
        'Mean Trust': 'Trust',
        'Mean Market': 'Market',
        'Mean Trust Strangers': 'Trust Strangers',
    }

    # Group by mobility and calculate means and confidence intervals.
    agg_data = aggregate_with_ci( data, 'Mobility', outcome_cols).sort_values('Mobility')
    create_plot('Statistics versus Mobility', agg_data, 'Mobility', 0, 1)

def plot_neighborhood_size(data: pd.DataFrame) -> None:
    outcome_cols = {
        'Mean Trust': 'Trust',
        'Mean Market': 'Market',
        'Mean Trust Strangers': 'Trust Strangers',
    }

    agg_data = aggregate_with_ci(data, 'Neighborhood Size', outcome_cols).sort_values('Neighborhood Size')
    create_plot('Statistics versus Neighborhood Size', agg_data, 'Neighborhood Size', 10, 100)

def plot_agent_memory(results_dir: str = "Results") -> None:
    """
    Plots trust measurements against agent memory size,
    using the shared aggregation and plotting functions.
    """
    outcome_cols = {
        'Mean Trust': 'Trust',
        'Mean Market': 'Market',
        'Mean Trust Strangers': 'Trust Strangers',
    }

    all_data = []

    for memory_size in range(10, 201, 10):
        file_path = (Path(results_dir) / f"memory_results_size{memory_size}.csv")

        if not file_path.exists():
            print(f"Warning: Missing file {file_path}")
            continue

        data = pd.read_csv(file_path)

        data['Memory Size'] = memory_size
        all_data.append(data)

    if not all_data:
        print("No agent memory result files found.")
        return

    # Combine observations from all memory sizes.
    combined_data = pd.concat(all_data, ignore_index=True)

    agg_data = aggregate_with_ci( combined_data, 'Memory Size', outcome_cols).sort_values('Memory Size')
    create_plot('Statistics versus Memory Size', agg_data, 'Memory Size', 10, 200)

def plot_endogenous_mobility(data: pd.DataFrame) -> None:
    outcome_cols = {
        'Mean Trust': 'Trust',
        'Mean Market': 'Market',
        'Mean Trust Strangers': 'Trust Strangers',
        'Mean Mobility': 'Mobility_self',
    }

    agg_data = aggregate_with_ci(data, 'Neighborhood Size', outcome_cols).sort_values('Neighborhood Size')
    create_plot('Statistics versus Neighborhood Size with Endogenous Mobility', agg_data, 'Neighborhood Size', 10, 100)

def load_agent_memory_data(results_dir: str) -> pd.DataFrame:
    """
    Load memory_results_sizeN.csv files for N = 10, 20, ..., 200.
    """
    all_data = []

    for memory_size in range(10, 201, 10):
        file_path = (Path(results_dir) / f"memory_results_size{memory_size}.csv")

        if not file_path.exists():
            print(f"Warning: Missing file {file_path}")
            continue

        data = pd.read_csv(file_path)
        data['Memory Size'] = memory_size
        all_data.append(data)

    if not all_data:
        raise FileNotFoundError(f"No agent memory result files found in {results_dir}")

    return pd.concat(all_data, ignore_index=True)


def plot_agent_memory_by_size(results_dir: str = "Results") -> None:
    """
    Plot trust measures against mobility, with a separate
    subplot for each agent memory size.
    """
    data = load_agent_memory_data(results_dir)

    outcome_cols = {
        'Mean Trust': 'Trust',
        'Mean Market': 'Market',
        'Mean Trust Strangers': 'Trust Strangers',
    }

    summary = aggregate_with_ci_mult(data, ['Memory Size', 'Mobility'], outcome_cols)

    memory_sizes = sorted(summary['Memory Size'].unique())

    ncols = 4
    nrows = int(np.ceil(len(memory_sizes) / ncols))

    fig, axes = plt.subplots(nrows, ncols, figsize=(16, 3.5 * nrows), sharex=True, sharey=True, squeeze=False)

    styles = {
        'Trust': ('Reading Signals', 'o'),
        'Market': ('Market Size', 's'),
        'Trust Strangers': ('Trust Strangers', 'p'),
    }

    for i, memory_size in enumerate(memory_sizes):
        ax = axes.flat[i]

        subset = (summary[summary['Memory Size'] == memory_size].sort_values('Mobility'))

        for col, (label, marker) in styles.items():
            x = subset['Mobility'].to_numpy()
            mean = subset[f'{col}_mean'].to_numpy()
            lower = subset[f'{col}_lower'].to_numpy()
            upper = subset[f'{col}_upper'].to_numpy()

            line, = ax.plot(x, mean, marker=marker, markersize=4, label=label)
            ax.fill_between(x, lower, upper, color=line.get_color(), alpha=0.15, linewidth=0)

        ax.set_title(f'Memory Size = {memory_size}')
        ax.grid(True, alpha=0.3)
        ax.set_ylim(0, 1)
        ax.set_xlim(0, 1)

    # Hide unused subplot slots.
    for i in range(len(memory_sizes), nrows * ncols):
        axes.flat[i].set_visible(False)

    fig.supxlabel('Mobility')
    fig.supylabel('Means')
    fig.legend(*axes.flat[0].get_legend_handles_labels(), loc='upper center', ncol=3, bbox_to_anchor=(0.5, 1.0))
    fig.tight_layout(rect=[0.03, 0.02, 1, 0.96])
    plt.show()

def plot_agent_memory_aggregated(results_dir: str) -> None:
    """
    Plot trust measures against mobility.
    """
    data = load_agent_memory_data(results_dir)

    outcome_cols = {
        'Mean Trust': 'Trust',
        'Mean Market': 'Market',
        'Mean Trust Strangers': 'Trust Strangers',
    }

    # Aggregate observations across all memory sizes by mobility.
    summary = aggregate_with_ci(data, 'Mobility', outcome_cols).sort_values('Mobility')
    create_plot('Statistics versus Mobility with Ongoing Relationships', summary, 'Mobility', 0, 1)

def main():
    # Basic run plots
    data = pd.read_csv("Codebase/Results/basic_results.csv")
    plot_mobility(data)
    plot_neighborhood_size(data)

    # Endogenous mobility plots
    data = pd.read_csv("Codebase/Results/endogenous_mobility_results.csv")
    plot_endogenous_mobility(data)

    # Agent memory plots
    # plot_agent_memory("Results")
    plot_agent_memory_by_size("Codebase/Results")
    plot_agent_memory_aggregated("Codebase/Results")

if __name__ == "__main__":
    main()