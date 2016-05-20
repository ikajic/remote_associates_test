from __future__ import division

import numpy as np
import matplotlib
import matplotlib.pyplot as pl

from rat.data.raw.freeassociations.read_data import load_vocabulary
from rat.algorithm.simulation import get_difficulties
from rat.model.utils import nearest_value

from simulation import simulate_test


def simulate_threshold(thresholds, nr_words):
    """
    Simulations with different thresholds.
    """
    performance = np.zeros((len(thresholds), 4))

    for i, th in enumerate(thresholds):
        print('Threshold = %.2f' % th)

        param = {'theta': th,
                 'nr_words': nr_words
                 }

        positions,  _ = simulate_test(**param)
        nr_items = len(positions)

        performance[i, :3] = get_difficulties(positions)
        percent_correct = 100*len(np.where(positions > -1)[0])/nr_items
        performance[i, 3] = percent_correct

    return performance


def simulate_number_of_words(nr_words):
    """
    Simulations with a varying number of responses to a RAT problem.
    The simulation is run for the maximal number of words and based on that the
    success rates for a smaller number of words are calculated.
    """

    performance = np.zeros((len(nr_words), 4))
    max_words = nr_words[-1]

    # load an existing file
    try:
        filename = 'nr_words_simulation.npz'
        positions = np.load(filename)['positions']
        print('Loading existing file...')
    except IOError:
        print('Running simulation!')
        positions,  _ = simulate_test(**{'nr_words': max_words})
        np.savez(filename, positions=positions)

    nr_items = float(len(positions))

    for i, nr_w in enumerate(nr_words):
        print('Testing words = %d' % nr_w)
        solutions = np.where(positions < nr_w, positions, -1)

        performance[i, :3] = get_difficulties(solutions)
        percent_correct = 100*len(np.where(solutions > -1)[0])/nr_items
        performance[i, 3] = percent_correct

    return performance

if __name__ == "__main__":
    font = {'family': 'serif',
            'serif': 'Times New Roman',
            'size': 28}
    legend_fs = 24
    matplotlib.rc('font', **font)

    # Association data, needed for statistics below
    W, ids, voc = load_vocabulary()
    weights = W[W.nonzero()]

    # problem difficulty labeling
    difficulties = [0, 1, 2]
    labs = ['easy', 'mid', 'hard']

    lw = 4
    colors = ['#4D4D4D', '#808080', '#CCCCCC', '#000000']
    alphas = [.4, .4, .6]
    ymin, ymax = -2, 105

    fig = pl.figure(figsize=(22, 6), dpi=80, facecolor="white")

    #   ----------------- Vary number of words -----------------
    axes = pl.subplot(121)
    min_nr_words, max_nr_words = 4, 35
    words = np.arange(min_nr_words, max_nr_words)
    try:
        filename = 'perf_words.npz'
        performance_w = np.load(filename)['performance_w']
        print('Loading existing simulation for words')
    except IOError:
        print('Running model simulation (different number of words)')
        performance_w = simulate_number_of_words(words)
        np.savez(filename, performance_w=performance_w)

    # Plot all results
    pl.plot(words, performance_w.T[3], label='all',
            linewidth=lw, color=colors[-1])

    # Plot individual curves
    for diff in difficulties:
        pl.plot(words, 100*performance_w.T[diff], label=labs[diff],
                linewidth=lw, color=colors[diff], alpha=alphas[diff])

        axes.grid(axis='y')
    pl.ylim(ymin, ymax)

    # set x-ticks
    locs, _ = pl.xticks()
    locs[0] = 1     # 4 words = 3 cues + *1* response

    pl.xticks(locs+3, np.array(locs, dtype=np.int))
    pl.xlim(min_nr_words, max_nr_words-1)

    pl.xlabel('Number of words')
    pl.ylabel('Performance (%)')

    axes.spines['right'].set_color('none')
    axes.spines['left'].set_color('none')
    axes.spines['top'].set_color('none')

    axes.xaxis.set_ticks_position('bottom')
    axes.yaxis.set_ticks_position('left')

    #   -------------------- Vary threshold --------------------
    axes = pl.subplot(122)
    min_threshold, max_threshold = 0, .44
    step_threshold = 0.01
    words = 15
    thresholds = np.arange(min_threshold, max_threshold, step_threshold)
    try:
        filename = 'perf_thresh.npz'
        performance_t = np.load(filename)['performance_t']
        print('Loading existing simulation for thresholds.')
    except IOError:
        print('Running algorithmic simulation (different number of threshols)')
        performance_t = simulate_threshold(thresholds, words)
        np.savez(filename, performance_t=performance_t)

    # Plot all results
    pl.plot(thresholds, performance_t.T[3], label='all',
            linewidth=lw, color=colors[-1])

    # Plot individual curves
    for diff in difficulties:
        pl.plot(thresholds, 100*performance_t.T[diff], label=labs[diff],
                linewidth=lw, color=colors[diff], alpha=alphas[diff])

    axes.grid(axis='y')

    pl.ylim(ymin, ymax)
    pl.xlim(min_threshold, max_threshold-step_threshold)

    axes.spines['right'].set_color('none')
    axes.spines['left'].set_color('none')
    axes.spines['top'].set_color('none')

    axes.xaxis.set_ticks_position('bottom')
    axes.yaxis.set_ticks_position('left')

    pl.legend(loc='upper right', prop={'size': legend_fs})
    pl.xlabel(r'Threshold ($\vartheta_s$)')

    pl.locator_params(axis='x', nbins=6)

    # Statistics
    percentiles = np.arange(101)
    values = np.percentile(weights, percentiles)

    drops = 1./np.arange(2, 11)

    for drop in drops:
        for lab, idx in zip(labs, difficulties):
            maxP = performance_t.T[idx].max()
            midP, idx_th = nearest_value(performance_t.T[idx], maxP*drop)
            theta = thresholds[idx_th]

            perc, idx_p = nearest_value(values, theta)
            p = percentiles[idx_p]

            print(('Drop by %.d%% for %s items at theta' +
                  '= %.2f (%.0fth percentile)') %
                  (drop*100, lab, theta, p))

        print('\n')

    if 0:
        pl.savefig('performance.pdf', bbox_inches='tight')

    pl.show()
