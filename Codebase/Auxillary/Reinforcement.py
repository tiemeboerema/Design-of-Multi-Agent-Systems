# -- Generated using Claude -----------------------------------#
def bush_mosteller(P_a, pi_a):
    if pi_a >= 0:
        return P_a + (1 - P_a) * pi_a
    else:
        return P_a + P_a * pi_a


def reinforce(
    propensity, chose_true_option, payoff
):  # propensity can be p_cooperate, p_trust, or p_market
    if chose_true_option:
        P_a = propensity
    else:
        P_a = 1 - propensity

    P_a_next = bush_mosteller(P_a, payoff)

    if chose_true_option:
        return P_a_next
    else:
        return 1 - P_a_next


# -- ---------------------- -----------------------------------#
