import random
import pandas as pd

import matplotlib.pyplot as plt


def plot_mobility(data: pd.DataFrame) -> None:
    """
    Plots mobility against various trust measurements.
    """
    agg_data = pd.DataFrame(columns=['Mobility', 'Trust', 'Market'])
    for i in range(11):
        mobility = i / 10
        mobility_values = data.loc[data['Mobility'] == mobility]

        mean_trust = mobility_values['Mean Trust'].mean()
        mean_market = mobility_values['Mean Market'].mean()

        agg_data.loc[len(agg_data)] = [mobility, mean_trust, mean_market]

    plt.plot(agg_data['Mobility'], agg_data['Trust'], marker='o', label='Reading Signals')
    plt.plot(agg_data['Mobility'], agg_data['Market'], marker='s', label='Market Size')

    plt.xlabel('Mobility Rate')
    plt.ylabel('Means')
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()


def main():
    data = pd.read_csv("results4.csv")
    plot_mobility(data)




if __name__ == "__main__":
    main()