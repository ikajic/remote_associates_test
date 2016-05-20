from __future__ import division

import numpy as np
import matplotlib
import matplotlib.pyplot as pl

from matplotlib.lines import Line2D
from network import Network
from utils import remove_array_duplicates

if __name__ == '__main__':
    font = {'family': 'serif',
            'serif': 'Times New Roman',
            'size': 28}

    matplotlib.rc('font', **font)

    # wrong response so simulation runs a bit longer
    # which leaves extra space after the winner
    # has been picked
    problem = ['river', 'note', 'account']
    target = 'house'

    param = {'max_visited': 5,
             'stim_len': 50}

    # run the simulation
    network = Network(**param)
    network.setup_problem(problem, target)
    network.run()

    # get indices of winning units
    winners = np.where(network.w > network.theta_w)[1]
    unique_win = remove_array_duplicates(winners)

    for i in unique_win:
        print network.ids[i], network.a[network.t_max, i]

    # get activated units which are not winners
    background = np.where(network.a > 0.1)[1]
    background = set(background)

    ids = list(background)
    idswc = list(set(ids) - set(network.cue_ids))

    p, n = len(unique_win), network.t_max
    X = np.linspace(0, 2, n)
    Ya = network.a[:n, ids].T

    # normalize non-cues for a nicer plot, otherwise only cues visible
    nfact = network.a[:n, idswc].max()
    Ya = Ya.clip(max=nfact)/nfact

    pl.figure(figsize=(22, 6))

    # ----------------------- Semantic Layer:       1st plot
    ax = pl.subplot(1, 2, 1)
    ax.set_frame_on(False)
    ax.get_xaxis().tick_bottom()
    ax.axes.get_yaxis().set_visible(False)

    Yy = p - (np.arange(p) + 0.5)
    Xx = [p, ]*p

    # draw gray rectangles
    rects = pl.barh(Yy, Xx, align='center', height=0.75,
                    color='.95', ec='None', zorder=-20)
    pl.xlim(0, p), pl.ylim(0, p)

    # winner onset times, needed for red lines
    active_win = network.z == 1
    wt = remove_array_duplicates(np.where(active_win)[1])
    wt_times = [np.where(network.z[:, i] > 0)[0][0] for i in unique_win]

    # draw everything
    ids = list(unique_win)
    Yw = (network.a[:n, ids].T).clip(max=nfact)/nfact
    Yz = network.z[:n, ids].T

    for i in range(p):
        # write word
        label = network.ids[ids[::-1][i]]
        pl.text(-.1, Yy[i], label, ha="right")

        # plot feedback from WTA
        pt = wt_times[::-1][i]/network.t_max
        pl.axvline(pt*p, (Yy[i]-.375)/p, (Yy[i]+.375)/p,
                   c='r', lw=2, zorder=-15, linestyle='--')

        # plot all activities
        for line in Ya:
            pl.plot(X*p/2, i+.125+.75*line, c='.6',
                    lw=.5, zorder=-10)

        # plot the activity of a word
        pl.plot(X*p/2, i+.125+.75*Yw[i], c='k', lw=3)

        xmin, xmax = ax.get_xaxis().get_view_interval()
        ymin, ymax = ax.get_yaxis().get_view_interval()
        ax.add_artist(Line2D((xmin, xmax), (ymin, ymin),
                      color='black', linewidth=2))
        pl.xlabel('Time (a.u)')

    # ----------------------- Winners:       2nd plot
    ax = pl.subplot(1, 2, 2)
    ax.set_frame_on(False)
    ax.get_xaxis().tick_bottom()
    ax.axes.get_yaxis().set_visible(False)

    Yy = p - (np.arange(p) + 0.5)
    Xx = [p, ]*p
    rects = pl.barh(Yy, Xx, align='center', height=0.75,
                    color='.95', ec='None', zorder=-20)
    pl.xlim(0, p), pl.ylim(0, p)

    for i in range(p):
        label = network.ids[ids[::-1][i]]
        pl.text(-.1, Yy[i], label, ha="right")

        pl.plot(X*p/2, i+.125+.75*Yz[i], c='k', lw=3)

    xmin, xmax = ax.get_xaxis().get_view_interval()
    ymin, ymax = ax.get_yaxis().get_view_interval()
    ax.add_artist(Line2D((xmin, xmax), (ymin, ymin),
                  color='black', linewidth=2))

    pl.xlabel('Time (a.u)')

    if 0:
        pl.savefig('net_activities.pdf', bbox_inches='tight')

    pl.show()
