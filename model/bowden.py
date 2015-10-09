"""
Simulation of the RAT experiment from Bowden et al 2003.
Only RAT items with all 4 words in the FA database are considered (=117).
Parameters in the model are:
    * spreading threshold (theta)
    * number of words (length of the search process
"""


from __future__ import division
from freeassociations.dataio import load_vocabulary

import numpy as np
import matplotlib.pyplot as pl
import pdb

from model.network import Network


def difficulties(positions):
    easy = positions[:16]       # >64%
    mid = positions[16:59]      # 32-64%
    hard = positions[59:]     # <32%

    peas = len((np.where(easy>-1)[0]))/float(len(easy))
    pmid = len((np.where(mid>-1)[0]))/float(len(mid))
    phard = len((np.where(hard>-1)[0]))/float(len(hard))

    return peas, pmid, phard


def simulate_test(**kwargs):
    # Load the problem set
    path_test = '../ratdata/bowden/rat_items'
    items = np.loadtxt(path_test, dtype=np.character)

    # Model parameters
    theta = kwargs.get('theta', 1)
    nr_words = kwargs.get('nr_words', 13)

    W, ids, voc = load_vocabulary()

    nr_items = len(items)
    positions = np.zeros(nr_items, dtype=np.int)

    all_responses = []

    net = Network()
    net.max_visited = nr_words

    for idx in range(nr_items):
        rat_item = items[idx]

        target = voc[rat_item[3]]

        net.setup(rat_item[:3])

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
            target_position = responses.index(target)
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

    print 'Threshold:', param['theta']
    print 'Performance:', success, '/', total
    print 'Success rate:', rate
    print 'Max position', solution_pos.max()
    pl.show()

if __name__ == "__main__":

    param = {'theta': 0,
             'nr_words': 11,
             'delta': 1,
             }

    positions, responses = simulate_test(**param)


    easy = positions[:16]
    mid = positions[16:59]
    hard = positions[59:]

    print 'Easy:', 100*len((np.where(easy>-1)[0]))/float(len(easy))
    print 'Mid:', 100*len((np.where(mid>-1)[0]))/float(len(mid))
    print 'Hard:', 100*len((np.where(hard>-1)[0]))/float(len(hard))

    plot_statistics(positions)
