"""
Simulation of the RAT experiment from Bowden et al 2003.
Only RAT items with all 4 words in the FA database are considered (=117).
Parameters in the model are:
    * spreading threshold (theta)
    * number of words (length of the search process
"""


from __future__ import division
from data.raw.freeassociations.read_data import load_vocabulary
from algorithm.simulation import get_difficulties

import numpy as np
import matplotlib.pyplot as pl
import pdb

from model.network import Network


def simulate_test(**kwargs):
    # Load the problem set
    net = Network(**kwargs)

    path_test = '../data/processed/rat_items'
    items = np.loadtxt(path_test, dtype=np.character)
    W, ids, voc = load_vocabulary()

    nr_items = len(items)
    positions = np.zeros(nr_items, dtype=np.int)

    all_responses = []

    for idx in range(nr_items):
        rat_item = items[idx]
        cues, target = rat_item[:3], rat_item[3]
        target_id = voc[target]

        net.setup_problem(cues, target)

        # if WTA fails to pick a winner, try again
        ok = True
        while ok:
            try:
                net.run()
                ok = False
            except BaseException:
                print 'WTA failed, retry the simulation'
                continue

        responses = list(net.visited())
        all_responses.append(responses)

        try:
            # position of the solution
            target_position = responses.index(target_id)
        except ValueError:
            # problem not solved
            target_position = -1

        print idx, rat_item, target_position

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

    print 'Performance:', success, '/', total
    print 'Success rate:', rate
    print 'Max position', solution_pos.max()
    pl.show()

if __name__ == "__main__":

    param = {'nr_words': 5,
             'theta': 0.0
             }

    positions, responses = simulate_test(**param)

    easy, mid, hard = get_difficulties(positions)

    print 'Easy:', 100*easy
    print 'Mid:', 100*mid
    print 'Hard:', 100*hard

    # plot_statistics(positions)
