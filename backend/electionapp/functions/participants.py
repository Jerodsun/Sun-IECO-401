import numpy as np
from collections import Counter
import matplotlib.pyplot as plt


class Candidate(object):
    """The candidate class, containing the candidate name, pol_x and pol_y dimensions"""

    def __init__(self, pol_x: float, pol_y: float, name, reelection):
        """
        Initialize Candidate with some base class attributes and a method
        """

        self._candidate_id = name  # candidate id
        self.pol_x = pol_x
        self.pol_y = pol_y
        self.run_reelection = reelection

    def __repr__(self):
        return "Candidate({0}, {1}, {2}, {3})".format(
            self._candidate_id, self.pol_x, self.pol_y, self.run_reelection
        )


class BaseVoter(object):
    """
    BaseVoter is the Abstract Base Class for the Greedy, Primary Optimizing and Center Informed Voter Classes.

    """

    def __init__(self, pol_x: float, pol_y: float, name):
        """
        Initialize BaseVoter with some base class attributes and a method
        """
        self._voter_id = name  # voter name or numerical id
        self.candidate_ranking = dict()  # calculated candidate rankings
        self.candidate_choice = None  # calculated candidate choice
        self.pol_x = pol_x
        self.pol_y = pol_y
        self._sequence = 0
        self._score = 0
        self.voter_type = "BaseVoter"

    def __repr__(self):
        return "Voter({0}, {1}, {2}, {3}, {4})".format(
            self.voter_type, self._voter_id, self.pol_x, self.pol_y, self._score
        )

    def calculate_distance(self, candidate: Candidate):
        distance = (
            (candidate.pol_x - self.pol_x) ** 2 + (candidate.pol_y - self.pol_y) ** 2
        ) ** (0.5)
        return distance

    def _calculate_distance(self, x: float, y: float, pol_x: float, pol_y, float):
        distance = ((x - pol_x) ** 2 + (y - pol_y) ** 2) ** (0.5)
        return distance

    def current_score(self):
        return self._score

    def calculate_reward(self, candidate):
        """calculate, but do not award, the reward function"""
        dist = self.calculate_distance(candidate)
        rwd = 0.5 - dist ** 2

        return rwd

    def reward(self, candidate):
        """reward function for successful candidate"""
        rwd = self.calculate_reward(candidate)
        self._score += rwd
        return rwd

    def closest_candidate(self, candidatelist):
        """get the closest candidate from the list"""
        scores = [self.calculate_distance(candidate) for candidate in candidatelist]
        index_max = np.argmax(scores)
        closest = candidatelist[index_max]
        return closest

        # graph and explain reward function choice


class GreedyVoter(BaseVoter):
    """
    Greedy Voter always chooses the option closest to the voter in every primary election and general election.
    """

    def __init__(self, pol_x: float, pol_y: float, name):

        """
        Initialize GreedyVoter
        """

        BaseVoter.__init__(self, pol_x, pol_y, name)
        self.voter_type = "GreedyVoter"

    def vote_choice(self, candidatelist, voterchoice=None):
        self.candidate_choice = None  # reset

        #         print(scores)

        i = self.closest_candidate(candidatelist)
        self.candidate_choice = i

        return i


class CenterInformedVoter(BaseVoter):
    """
    CenterInformedVoter tries to center the choice on what the voter believes will be the outcome,
    as long as there is no negative payoff
    """

    def __init__(self, pol_x: float, pol_y: float, name):

        """
        Initialize CenterInformedVoter
        """

        BaseVoter.__init__(self, pol_x, pol_y, name)
        self.voter_type = "CenterInformedVoter"

    def _process_candidates(self, candidatelist):
        """process candidates, save to self.candidate_ranking"""

        self.candidate_ranking = {
            candidate: self.calculate_distance(candidate) for candidate in candidatelist
        }

        return

    def vote_choice(self, candidatelist, voterchoice):
        """
        param voterchoice: the result of process_all_voters, candidate list with number of closest voters

        return: candidate choice
        """
        self._process_candidates(candidatelist)

        c = Counter(self.candidate_ranking)
        # finding 3 closest values
        chigh = c.most_common()[::-1]
        if len(chigh) > 3:
            chigh3 = chigh[:3]
        else:
            chigh3 = chigh

        v = Counter(voterchoice)
        vhigh = v.most_common()

        self.candidate_choice = None  # reset

        #         print(vhigh)

        for i in vhigh:
            #             print(i[0])
            if self.calculate_reward(i[0]) > 0:
                self.candidate_choice = i[0]
                return i[0]


class PrimaryOptimizingVoter(BaseVoter):
    """
    PrimaryOptimizingVoter tries to center the choice on what the voter believes will be the outcome
    """

    def __init__(self, pol_x: float, pol_y: float, name):

        """
        Initialize PrimaryOptimizingVoter
        """

        BaseVoter.__init__(self, pol_x, pol_y, name)
        self.voter_type = "PrimaryOptimizingVoter"

    def _process_candidates(self, candidatelist):
        """process candidates, save to self.candidate_ranking"""

        self.candidate_ranking = {
            candidate: self.calculate_distance(candidate) for candidate in candidatelist
        }

        return

    def vote_choice(self, candidatelist, voterchoice):
        """
        param voterchoice: the result of process_all_voters, candidate list with number of closest voters

        if the voter's candidate is in the top 3, select that candidate. Else select the next closest candidate in the top

        return: candidate choice
        """
        self._process_candidates(candidatelist)

        c = Counter(self.candidate_ranking)
        # finding 3 lowest values
        chigh = c.most_common()[::-1]
        if len(chigh) > 3:
            chigh3 = chigh[:3]
        else:
            chigh3 = chigh

        v = Counter(voterchoice)
        vhigh = v.most_common(3)  # finding 3 highest values

        self.candidate_choice = None  # reset

        #         print(chigh3)
        #         print(vhigh)

        for i in vhigh:
            for j in chigh3:
                if i[0] == j[0]:
                    self.candidate_choice = i[0]
                    #                     print(self.candidate_choice)
                    return i[0]

        # not in top 3

        for i in vhigh:
            for j in chigh:
                if i[0] == j[0]:
                    self.candidate_choice = i[0]
                    #                     print(self.candidate_choice)
                    return i[0]
