"""
Activity spreads only from a single node
"""

from __future__ import division
from data.raw.freeassociations.read_data import load_vocabulary

import numpy as np
import pdb
import copy


def WTA(activations, visited, j, activated):
    """
    Return the index of a unit with the highest activity level which has not
    been visited yet and which is not a current winner.

    Input
    -----
    activations:    a list with activation levels for each node/word
    visited:        list of indices of visited nodes
    j:              current winner
    activated:      list of indices of previously activated nodes
                    (past winners)

    Output
    ------
    k:              the index of a winning node
    """
    # sort activations
    sorted_idx = np.argsort(activations)[::-1]

    k = -1
    # pick the most activated note different from the current winner
    # and previously visited nodes
    for nb in sorted_idx:
        if (nb not in visited) and (nb != j):
            assert nb not in activated
            k = nb
            break

    return k


def spread_activity(init_nodes, target, W, threshold=0.0, max_visited=11):
    """
    Spread the activity in the semantic network.
    Every word is assigned a unique word id.
    Weighted edges between nodes are stored in the adjacency matrix W.

    Input
    -----
        init_nodes:     initial nodes where the spreading starts
        target:         stop if current node is the target
        W:              NxN weight matrix, N is the number of nodes
        max_visited:    number of nodes to visit on the search path
        threshold:      spreading threshold

    Output
    ------
        activities:     N dimensional array with activity level for every node
        visited:        visited nodes along the way
    """
    # number of nodes
    N = np.alen(W)

    # reverse the order for the queue
    cues = copy.deepcopy(init_nodes)

    # nodes to visit, queue
    activated = []  # copy.deepcopy(cues)

    # visited nodes
    visited = []

    activations = np.zeros(N)
    # activations[cues] = 1.

    counter = 0
    I = np.zeros((3, N))

    for idx, cue in enumerate(cues):
        I[idx, cue] = 1.

    j = -1
    while len(visited) < max_visited:
        # spread the activity from a winning node
        if j > -1:
            i = W[j].nonzero()[0]
            activations[i] += np.where(W[j, i] >= threshold,
                                       W[j, i], 0)*activations[j]

        # add external input to activate the cues
        if counter < 3:
            activations += I[counter]

        if j > -1:
            visited.append(j)

        if j == target:
            break

        j = WTA(activations, visited, j, activated)

        counter += 1

    assert len(visited) == max_visited or j == target

    return activations, visited

if __name__ == "__main__":
    W, ids, voc = load_vocabulary()

    cues = ['river', 'note', 'account']
    target = 'bank'

    cues_id = [voc[cue] for cue in cues]

    activations, order = spread_activity(init_nodes=cues_id,
                                         target=voc[target],
                                         W=W,
                                         threshold=.0,
                                         max_visited=10)
    for i, ord_idx in enumerate(order):
        print i+1, ids[ord_idx], activations[ord_idx]
