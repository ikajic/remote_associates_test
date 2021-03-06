"""
Simulation of the RAT experiment from Bowden et al 2003.
Only RAT items with all 4 words in the FA database are considered (=117).
Parameters in the model are:
    * spreading threshold (theta)
    * number of words
"""


from __future__ import division

import numpy as np
import matplotlib.pyplot as pl

from spread_activity import spread_activity
from rat.data.raw.freeassociations.read_data import load_vocabulary


def get_difficulties(positions):
    """
    Splits the array of positions into three parts corresponding
    to three diffrent difficulty levels.
    """
    # TODO: automatise division of ranges
    easy = positions[:16]
    mid = positions[16:59]
    hard = positions[59:]

    peasy = len((np.where(easy > -1)[0]))/float(len(easy))
    try:
        pmid = len((np.where(mid > -1)[0]))/float(len(mid))
    except ZeroDivisionError:
        pmid = 0

    try:
        phard = len((np.where(hard > -1)[0]))/float(len(hard))
    except ZeroDivisionError:
        phard = 0

    return peasy, pmid, phard


def simulate_test(**kwargs):
    # Load the problem set
    path_test = '../data/processed/rat_items'
    items = np.loadtxt(path_test, dtype=np.character)

    # Model parameters
    theta = kwargs.get('theta', 0)
    nr_words = kwargs.get('nr_words', 13)

    W, ids, voc = load_vocabulary()

    nr_items = len(items)
    positions = np.zeros(nr_items, dtype=np.int)
    # was = WAS()

    all_responses = []

    for idx in range(nr_items):
        rat_item = items[idx]
        nodes = [voc[word] for word in rat_item]

        target = voc[rat_item[3]]

        activations, responses = spread_activity(init_nodes=nodes[:3],
                                                 target=target,
                                                 W=W,
                                                 max_visited=nr_words,
                                                 threshold=theta)
        all_responses.append(responses)

        # response position
        try:
            target_position = responses.index(target)
        except ValueError:
            target_position = -1

        # print idx, rat_item, target_position

        positions[idx] = target_position

    return np.array(positions, dtype=np.int), all_responses


def plot_statistics(solution_pos):
    total = len(solution_pos)
    fail = (solution_pos == -1).sum()
    success = total-fail
    rate = 100*success/np.float(total)

    # ## Plots
    pl.figure(figsize=(12, 4))
    pl.suptitle('Model Performance (' + str(rate)[:4] + ' %)')

    # model output for each item C/W
    cor_wr = np.where(np.array(solution_pos) > 0, 1, 0)
    for i, sid in enumerate(cor_wr):
        c = 'g'
        if sid == 0:
            c = 'r'
        pl.plot(i, sid, 'o', color=c)

    pl.ylim([-.5, 1.5])
    pl.xlabel('RAT Task ID')
    pl.ylabel('Correct (1) / Wrong (0)')

    print '----'
    print 'Threshold:', param['theta']
    print 'Performance:', success, '/', total
    print 'Success rate:', rate
    print 'Max position', solution_pos.max()
    pl.show()

if __name__ == "__main__":

    param = {'theta': 0,
             'nr_words': 30
             }

    positions, responses = simulate_test(**param)

    easy, mid, hard = get_difficulties(positions)

    print 'Percentage of problems solved:'
    print 'Easy:', 100*easy, '%'
    print 'Mid:', 100*mid, '%'
    print 'Hard:', 100*hard, '%'

    plot_statistics(positions)
