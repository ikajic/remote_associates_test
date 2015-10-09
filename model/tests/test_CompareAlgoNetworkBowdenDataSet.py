import unittest
import numpy as np

from algorithm.sa import spread_activity
from model.network import Network

import pdb


class CompareAlgoNetworkBowdenDataSet(unittest.TestCase):
    """
    Compares the algorithm and the network performance for the Bowden et al.
    (2003) dataset.
    Maximal number of searched items is 8.
    """

    def setUp(self):
        self.net = Network()
        path = '../../ratdata/bowden/rat_items'
        self.items = np.loadtxt(path, dtype=np.character)
        self.nr_words = 10
        self.net.max_visited = self.nr_words

    def testEqual(self):
        equal = 0
        not_equal = []

        for i, rat_item in enumerate(self.items):
            # words
            cues, target = rat_item[:3], rat_item[3]

            # word ids
            cue_ids = [self.net.voc[c] for c in cues]
            target_id = self.net.voc[target]

            # run the algorithm simulation
            _, visited_alg = spread_activity(init_nodes=cue_ids,
                                             target=target_id,
                                             W=self.net.W,
                                             max_visited=self.nr_words)

            # ...and the network simulation
            self.net.setup_problem(cues, target)
            print '\n', i, cues, target, target_id

            # WTA can fail if noise added to two equal numbers is not enough
            # to pick a winner. If this happens, the simulation is repeated
            ok = True
            while ok:
                try:
                    self.net.run()
                    ok = False
                except BaseException:
                    print 'WTA failed, retrying the run!'
                    continue

            l1, l2 = visited_alg, list(self.net.visited())

            if target_id in set(l1) and target_id not in set(l2) or\
                    target_id not in set(l1) and target_id in set(l2):
                not_equal.append(i)
            else:
                print 'ok', equal
                equal += 1

            print 'A:', l1
            print 'N:', l2

        print not_equal

if __name__ == "__main__":
    unittest.main()
