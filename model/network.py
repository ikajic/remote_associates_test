from __future__ import division
from utils import step, remove_array_duplicates, mult

import numpy as np
import data.freeassociations.dataio as dio


class Network(object):
    """
    Neural-network of the RAT solving.
    >>> problem = ['cottage', 'swiss', 'cake']
    >>> target = 'cheese'

    >>> network = Network()
    >>> network.setup_problem(problem, target)
    >>> network.run()

    >>> print('Solution found: %d' % network.solution())
    """

    def __init__(self, **kwargs):
        """
        Set up equation parameters in the network and load the data to
        construct the semantic layer.
        For a human-readable format of equations refer to the paper.

        Input
        -----
            max_visited:    maximal allowed number of guesses, default 3
            stim_len:       length of stimulus and winner activity, default 50
        """
        # maximal number of nodes visited in the first layer
        self.max_visited = kwargs.get('max_visited', 4)

        # stimulus length and the duration of activity for a WTA unit
        self.stim_len = kwargs.get('stim_len', 50)

        # connection matrix with associative strengths
        self.W, self.ids, self.voc = dio.load_vocabulary()

        # number of units
        self.N = np.alen(self.W)

        assert self.N == len(self.ids) == len(self.voc)

        self.rho_w = 1-0.995  # integration constant for the WTA layer

        self.c1 = 1.        # excitatory connection
        self.c2 = 1.        # normalization constant
        self.c3 = 1.        # inhibitory neuron constant
        self.c4 = 50.       # inhibitory layer constant
        self.c5 = 0.1       # noise amplitude

        self.noise_offset = 0.05/self.c5

        self.theta_w = 1.    # threshold for the WTA layer
        self.I_amp = 1.      # amplitude of the clamped imput

    def setup_problem(self, cues, target, t_max=10000, isi=100):
        """
        Initialize the activities in each layer and activate the RAT problem
        cues.

        Input
        -----
        cues:   list with three words and the target, RAT problem cues
        t_max:  simulation duration
        isi:    inter-stimulus interval
        """
        self.t_max = t_max                  # simulation duration
        array_shape = (self.t_max, self.N)

        self.a = np.zeros(array_shape)      # semantic layer unit activities
        self.z = np.zeros(array_shape)      # winning units
        self.I = np.zeros(array_shape)      # external input
        self.w = np.zeros(array_shape)      # WTA layer unit activities
        self.y = np.zeros((array_shape[0], 1))  # single inhibitory WTA neuron
        self.r = np.zeros(array_shape)      # inhibitory layer unit activities

        # get numerical ids for word cues and the target
        self.cue_ids = [self.voc[c] for c in cues]
        self.target = self.voc[target]

        # equally spaced cue-onsets of the duration stim_len
        start = self.stim_len
        stop = len(self.cue_ids)*(self.stim_len+isi)+self.stim_len
        step = self.stim_len + isi
        onsets = np.arange(start, stop, step)

        # set external input to 1 for the cue nodes
        for i, c in enumerate(self.cue_ids):
            self.I[onsets[i]:onsets[i]+self.stim_len, c] = self.I_amp

    def _terminate_condition(self, t):
        """
        Returns True if the target has been found or a certain number of
        guesses made.
        """
        terminate = False

        # target node has been activated
        target_active = self.r[t-self.stim_len:t, self.target].sum()

        # or certain number of words visited
        if self.r[t-self.stim_len].sum() == self.max_visited or\
           target_active:
            self.t_max = t-1
            terminate = True

        return terminate

    def run(self):
        """
        Run the network simulation by evaluating model equations at every time
        step.
        """
        # integration constant
        rho_a = 1./(self.stim_len)

        # simulation time
        time = np.arange(0, self.t_max)

        for t in time[1:]:
            # stop simulation if target found or max guesses
            if self._terminate_condition(t):
                break

            #  ----- Semantic Layer -----
            # winning/active units
            self.z[t-1] = step(self.w[t-1], self.theta_w)

            # unit activities
            self.a[t] = self.a[t-1] + rho_a*(mult(self.W,
                                                  self.z[t-1],
                                                  self.a[t-1]) +
                                             self.I[t-1])
            # ----- WTA Layer -----
            eta = np.random.random(self.N) - self.noise_offset

            # normalise activities to 0-1
            divisor = np.max([1., self.a[t-1].max()])

            self.w[t] = self.w[t-1] + self.rho_w * \
                (self.c1*self.z[t-1] +
                 self.c2*self.a[t-1]/divisor -
                 self.c3*self.y[t-1] -
                 self.c4*self.r[t-1] +
                 self.c5*eta)

            self.y[t] = self.z[t-1].sum()

            # ----- Inhibitory Layer -----
            # -2 added because of discreete update lags
            self.r[t] = (self.r[t-1] +
                         step(self.z[t-self.stim_len:t].sum(axis=0),
                              self.stim_len-2)).clip(max=1)

            # several winners are not allowed
            if self.y[t] > 1:
                raise Exception('Multiple winners')

            # rectify WTA activities to 0 (if needed)
            self.w[t] = self.w[t].clip(min=0)

    def visited(self):
        """
        Return a list of visited nodes.
        """
        # assert nodes have been visited
        assert self.r.sum() != 0

        x = np.where(self.r > 0)[1]
        visited = remove_array_duplicates(x)

        return visited

    def solution(self):
        "Return True if solution has been found"
        return self.target in self.visited()


if __name__ == '__main__':
    problem = ['cottage', 'swiss', 'cake']
    target = 'cheese'

    param = {'max_visited': 20,
             'stim_len': 50}

    network = Network(**param)
    network.setup_problem(problem, target)
    network.run()

    print('Solution found: %d' % network.solution())
