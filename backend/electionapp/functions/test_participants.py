import unittest

from participants import Candidate, GreedyVoter, CenterInformedVoter, PrimaryOptimizingVoter
from runner import Runner

import math
import random
import numpy as np
from collections import Counter


class TestParticipants(unittest.TestCase):
    def setUp(self):
        pass
    def test_candidates(self):
        self.a = Candidate(3, 2, "A", 0)
        self.b = Candidate(5, 4, "B", 0)
        self.c = Candidate(35, 34, "C", 0)

    def test_voters(self):
        self.j = PrimaryOptimizingVoter(5.5, 2.5, "J")
        self.k = PrimaryOptimizingVoter(1.5, 2.5, "K")

        self.p = GreedyVoter(2, 1, "P")
        self.q = GreedyVoter(0, 0, "Q")
        self.r = GreedyVoter(3, 4, "R")

        self.s = CenterInformedVoter(5.5, 4, "S")
        self.t = CenterInformedVoter(1.5, 4, "T")

        self.runner = Runner()

    def test_vote_choice(self):
        self.j.vote_choice([self.a, self.b, self.c], self.voterchoice)
        self.p.vote_choice([self.a, self.b, self.c], self.voterchoice)
        self.s.vote_choice([self.a, self.b, self.c], self.voterchoice)

    def test_process_voters(self):
        self.voterchoice = self.runner.process_all_voters(
            [self.j, self.k, self.l, self.m, self.p, self.q, self.r, self.s, self.t], [self.a, self.b, self.c])
    
if __name__ == '__main__':
    unittest.main()