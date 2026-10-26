import random
import pandas as pd

import matplotlib.pyplot as plt


def create_plot(data: pd.DataFrame, selected_var: str, xbottom: int, xtop: int) -> None:
    """
    Plots a selected variable (mobility/neigh_size) against various measures of trust.
    """
    plt.plot(data[selected_var], data['Trust'], marker='o', label='Reading Signals')
    plt.plot(data[selected_var], data['Market'], marker='s', label='Market Size')
    plt.plot(data[selected_var], data['Trust Strangers'], marker='p', label='Trust Strangers')
    if 'Mobility_self' in data.columns:
        plt.plot(data[selected_var], data['Mobility_self'], marker='v', label='Mobility')

    plt.xlabel(f'{selected_var}')
    plt.ylabel('Means')
    plt.xlim(xbottom, xtop)
    plt.ylim(0, 1)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()


def plot_mobility(data: pd.DataFrame) -> None:
    """
    Plots mobility against various trust measurements.
    """
    agg_data = pd.DataFrame(columns=['Mobility', 'Trust', 'Market', 'Trust Strangers'])
    for i in range(11):
        mobility = i / 10
        mobility_values = data.loc[data['Mobility'] == mobility]

        mean_trust = mobility_values['Mean Trust'].mean()
        mean_market = mobility_values['Mean Market'].mean()
        mean_trust_strangers = mobility_values['Mean Trust Strangers'].mean()

        agg_data.loc[len(agg_data)] = [mobility, mean_trust, mean_market, mean_trust_strangers]

    create_plot(agg_data, 'Mobility', 0, 1)


def plot_neighborhood_size(data: pd.DataFrame) -> None:
    """
    Plots neighborhood size against various trust measurements.
    """
    agg_data = pd.DataFrame(columns=['Neighborhood Size', 'Trust', 'Market', 'Trust Strangers'])
    for size in range(10, 110, 10):
        neigh_size_values = data.loc[data['Neighborhood Size'] == size]

        mean_trust = neigh_size_values['Mean Trust'].mean()
        mean_market = neigh_size_values['Mean Market'].mean()
        mean_trust_strangers = neigh_size_values['Mean Trust Strangers'].mean()

        agg_data.loc[len(agg_data)] = [size, mean_trust, mean_market, mean_trust_strangers]

    create_plot(agg_data, "Neighborhood Size", 10, 100)


def plot_endogenous_mobility(data: pd.DataFrame) -> None:
    """
    Plots neighborhood size against various trust measurements,
    now also including endogenous mobility.
    """
    agg_data = pd.DataFrame(columns=['Neighborhood Size', 'Mobility_self', 'Trust', 'Market', 'Trust Strangers'])
    for size in range(10, 110, 10):
        neigh_size_values = data.loc[data['Neighborhood Size'] == size]

        mean_trust = neigh_size_values['Mean Trust'].mean()
        mean_market = neigh_size_values['Mean Market'].mean()
        mean_trust_strangers = neigh_size_values['Mean Trust Strangers'].mean()
        mean_mobility = neigh_size_values['Mean Mobility'].mean()

        agg_data.loc[len(agg_data)] = [size, mean_mobility, mean_trust, mean_market, mean_trust_strangers]

    create_plot(agg_data, "Neighborhood Size", 10, 100)


def main():
    # Basic run plots
    data = pd.read_csv("Codebase/Results/basic_results.csv")
    plot_mobility(data)
    plot_neighborhood_size(data)

    # Endogenous mobility plots
    data = pd.read_csv("Codebase/Results/endogenous_mobility_results2.csv")
    plot_endogenous_mobility(data)

    # Agent memory plots


if __name__ == "__main__":
    main()