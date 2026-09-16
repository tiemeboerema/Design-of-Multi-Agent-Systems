import random

import Config as cfg


def signal_read_correct_prob(trustworthiness):
    """This function takes into account the trustworthiness of the partner. A completely untrustworthy partner will send a clear signal, so will a trustworthy one.
    In between we linearly add uncertainty the right signal will be sent with the halfway point being completely random."""
    return 0.5 + abs(trustworthiness - 0.5)


def _read_signal(agent, partner):
    return random.random() < signal_read_correct_prob(partner.p_cooperate)


def trusts(agent, partner, in_market):
    used_signal_reading = (
        random.random() < agent.p_trust
    )  # delete# I am unsure why we check r < p_trust over checking if it is larger, worth checking later.

    if used_signal_reading:
        read_signal = _read_signal(agent, partner)
        true_signal = partner.will_cooperate
        if read_signal:
            decision = true_signal
        else:
            decision = not true_signal
    else:
        decision = (
            (not in_market) and (not partner.newcomer) and (not agent.newcomer)
        )  # delete# Third part is not strictly neccessary, but this is how the paper made the diagram, and worth explaining.

    return decision, used_signal_reading


def will_play(agent, partner, in_market):
    agent_trusts, agent_used_signal_reading = trusts(agent, partner, in_market)
    partner_trusts, partner_used_signal_reading = trusts(
        partner, agent, in_market
    )

    played = agent_trusts and partner_trusts
    return played, agent_used_signal_reading, partner_used_signal_reading
