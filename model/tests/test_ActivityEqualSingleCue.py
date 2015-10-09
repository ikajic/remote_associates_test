import unittest
import numpy as np

from algorithm.sa import spread_activity
from model.network import Network
import pdb


class TestActivityLevels(unittest.TestCase):
    """
    This test-suite compares the performance of the search algorithm and the
    neural network model:
        a) testActivityEqualSingleCue
            compares the activity of all nodes in
            the algorithm and the network after presenting a single cue.

        b) testActivityEqualThreeCues
            compares the activity of all nodes in
            the algorithm and the network after presenting all three cues.

        c) testOrderEightWords
            compares the order of the explored nodes, and the activity levels
            up to a certain tolerance level

    """

    def setUp(self):
        self.net = Network()

    def testActivityEqualSingleCue(self):
        cue = 'match'
        target = 'fire'

        target_id = self.net.voc[target]

        max_visited = 1
        self.net.max_visited = max_visited

        act_alg, _ = spread_activity(init_nodes=[self.net.voc[cue]],
                                     target=target_id,
                                     W=self.net.W,
                                     max_visited=max_visited)

        self.net.setup_problem([cue], target)
        self.net.run()

        np.testing.assert_almost_equal(act_alg,
                                       self.net.a[self.net.t_max],
                                       decimal=3)

    def testActivityEqualThreeCues(self):
        cues = ['match', 'game', 'stick']
        target = 'fire'

        target_id = self.net.voc[target]
        max_visited = 3
        self.net.max_visited = max_visited

        self.net.setup_problem(cues, target)

        act_alg, _ = spread_activity(init_nodes=self.net.cue_ids,
                                     target=target_id,
                                     W=self.net.W,
                                     max_visited=max_visited)

        self.net.run()
        np.testing.assert_almost_equal(act_alg,
                                       self.net.a[self.net.t_max],
                                       decimal=2)

    def testOrderEightWords(self):
        # number of words along the search path
        nr_words = 8

        cues = ['cottage', 'swiss', 'cake']
        target = 'cheese'

        target_id = self.net.voc[target]

        # get word ids
        cue_ids = [self.net.voc[c] for c in cues]

        act_alg, visited_alg = spread_activity(init_nodes=cue_ids,
                                               target=target_id,
                                               W=self.net.W,
                                               max_visited=nr_words)
        self.net.setup_problem(cues, target)
        self.net.max_visited = nr_words
        self.net.run()

        visited_net = self.net.visited()

        np.testing.assert_equal(visited_alg,
                                visited_net)

        a1 = self.net.a[self.net.t_max, visited_net]
        a2 = act_alg[visited_alg]

        # tolerate diffrences in activities up to 0.1
        np.testing.assert_allclose(a1, a2, rtol=1e-1)

if __name__ == "__main__":
    unittest.main()
