from __future__ import division

import numpy as np
import matplotlib
import matplotlib.pyplot as pl

from data.freeassociations.dataio import load_vocabulary
from algorithm.bowden import simulate_test, get_difficulties
from model.utils import nearest_value


def simulate_threshold(thresholds, nr_words):
    """
    Simulations with different thresholds.
    """
    results = np.zeros(len(thresholds))
    pos = np.zeros((len(thresholds), 3))

    for i, th in enumerate(thresholds):
        print('Threshold = %.2f' % th)

        param = {'theta': th,
                 'nr_words': nr_words
                 }

        positions,  _ = simulate_test(**param)

        pos[i, :] = get_difficulties(positions)
        nr_items = len(positions)
        p_corr = len(np.where(positions > -1)[0])/float(nr_items)
        results[i] = 100*p_corr

    return pos, results


def simulate_number_of_words(nr_words):
    """
    Simulations with a varying number of responses to a RAT problem.
    """
    threshold = 0

    results = np.zeros(len(nr_words))
    pos = np.zeros((len(nr_words), 3))

    for i, nr_w in enumerate(nr_words):
        print('Testing words = %d' % nr_w)
        param = {'theta': threshold,
                 'nr_words': nr_w
                 }

        positions,  _ = simulate_test(**param)

        pos[i, :] = get_difficulties(positions)
        nr_items = len(positions)
        p_corr = len(np.where(positions > -1)[0])/float(nr_items)
        results[i] = 100*p_corr

    return pos, results

if __name__ == "__main__":
    font = {'family': 'serif',
            'serif': 'Times New Roman',
            'size': 28}
    legend_fs = 24
    matplotlib.rc('font', **font)

    # Association data, needed for statistics
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
    posw, results_w = simulate_number_of_words(words)

    # Plot all results
    pl.plot(words, results_w, label='all', linewidth=lw, color=colors[-1])

    # Plot individual curves
    for diff in difficulties:
        pl.plot(words, posw.T[diff], label=labs[diff],
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
    words = 30
    thresholds = np.arange(min_threshold, max_threshold, step_threshold)
    post, results_t = simulate_threshold(thresholds, words)

    # Plot all results
    pl.plot(thresholds, results_t, label='all', linewidth=lw, color=colors[-1])

    # Plot individual curves
    for diff in difficulties:
        pl.plot(thresholds, post.T[diff], label=labs[diff],
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
            maxP = post.T[idx].max()
            midP, idx_th = nearest_value(post.T[idx], maxP*drop)
            theta = thresholds[idx_th]

            perc, idx_p = nearest_value(values, theta)
            p = percentiles[idx_p]

            print('Drop by %.d%% for %s items at theta = %.2f (%.0fth percentile)' % 
                  (drop*100, lab, theta, p))

        print('\n')

    if 0:
        pl.savefig('img/performance.pdf', bbox_inches='tight')

    pl.show()
