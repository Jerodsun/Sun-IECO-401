# if there is a tie, then there is no score, move on to next round - track ties

from .participants import Candidate, GreedyVoter, CenterInformedVoter, PrimaryOptimizingVoter
import math
import random
import numpy as np
from collections import Counter

class Runner(object):
    def __init__(self,
                 n_greedy=300, n_optimizing=500, n_center=300, dist_type_v="uniform", dist_type_c="uniform",
                 reelection=.75, c_min = 2, c_max = 10,
                 alpha=0.0375, mu=0, mu_2 = 0, delta=0.025, sigma=0.1, c_lambda=1, run_steps=100, seed=500):
        
        self.n_voters = n_greedy + n_optimizing + n_center
        self.n_greedy = n_greedy
        self.n_optimizing = n_optimizing
        self.n_center = n_center
        self.dist_type_v = dist_type_v
        self.dist_type_c = dist_type_c
        self.reelection = reelection # percent chance the incumbent chooses to run for reelection
        self.alpha = alpha
        self.mu = mu # mean
        self.mu_2 = mu_2
        self.delta = delta
        self.sigma = sigma # standard deviation
        self.c_lambda = c_lambda
        self.run_steps = run_steps
        
        self.c_min = c_min
        self.c_max = c_max
        
        self.voters = self.make_voters(self.n_greedy, self.n_optimizing, self.n_center, self.dist_type_v)
        self.candidates = None
        
        np.random.seed(seed) # always stable first voters, candidates order
        
    def _make_distribution(self, n_voters, dist_type):
        """ make the specified distribution of voters """
        if dist_type == "uniform":
            voter_dist = np.random.uniform(low=-1, high=1, size=(n_voters, 2))
            return voter_dist
        
        if dist_type == "normal":
            voter_dist = np.random.normal(self.mu, self.sigma, (n_voters, 2))
            return voter_dist
        
        if dist_type =="bimodal_normal":
            voter_dist_a = np.random.normal(self.mu, self.sigma, (math.floor(n_voters/2), 2))
            voter_dist_b = np.random.normal(self.mu, self.sigma, (math.ceil(n_voters/2), 2))
            return np.concatenate((voter_dist_a, voter_dist_b), axis=0)
        
    def generate_candidates(self, dist_type):
        pass
    
    def make_center_voter_array(self, n_center, dist_type):
        
        if n_center == 0:
            return np.array([])
        voter_dist = self._make_distribution(n_center, dist_type)
        voters_list = ['cv%i' % i for i in range(n_center)]
        voters = np.array([CenterInformedVoter(x, y, i) for (x,y),i in zip(voter_dist,voters_list)])
        
        return voters
    
    def make_greedy_voter_array(self, n_greedy, dist_type):
        
        if n_greedy == 0:
            return np.array([])
        
        voter_dist = self._make_distribution(n_greedy, dist_type)
        voters_list = ['gv%i' % i for i in range(n_greedy)]
        voters = np.array([GreedyVoter(x, y, i) for (x,y),i in zip(voter_dist,voters_list)])
        
        return voters
                            
    def make_optimizing_voter_array(self, n_optimizing, dist_type):

        if n_optimizing == 0:
            return np.array([])
        
        voter_dist = self._make_distribution(n_optimizing, dist_type)
#         print(voter_dist)
        voters_list = ['ov%i' % i for i in range(n_optimizing)]
#         print(voters_list)
        voters = np.array([PrimaryOptimizingVoter(x, y, i) for (x,y),i in zip(voter_dist,voters_list)])
        
        return voters
    
   
    def make_voters(self, n_greedy, n_optimizing, n_center, dist_type):
                
        optimizers = self.make_optimizing_voter_array(n_optimizing, dist_type)
        greedy = self.make_greedy_voter_array(n_greedy, dist_type)
        center = self.make_center_voter_array(n_center, dist_type)
        
        all_voters = np.hstack((optimizers, greedy, center))

        return all_voters
        
    def get_voters(self):
        return self.voters
    
    def get_candidate_count(self):
        if type(self.candidates) == None:
            return 0

        return len(self.candidates)
    
    def _calculate_distance(self, x: float, y: float, pol_x: float, pol_y: float):
        """ calculate the distance between two (x,y) points """
        distance = ( (x - pol_x)**2 + (y - pol_y)**2 )**(0.5)
        return distance
        
    def process_all_voters(self, voters, candidates):
        """
        :param voters: list of all voter instances
        :param candidates: list of all candidate instances

        :return: candidate list with number of closest voters
        """
        ls = [0] * len(candidates)
        for v in voters:
            choice = None
            scores = [self._calculate_distance(v.pol_x, v.pol_y, c.pol_x, c.pol_y) for c in candidates]
            index_min = np.argmin(scores)
            ls[index_min] = ls[index_min] + 1

        return dict(zip(candidates, ls))


    def _make_new_candidates(self, c_min, c_max, dist_type, reelection):
        
        n_candidates = np.random.randint(2, 11)
#         n_candidates = 4
        
        reelection = np.random.choice((0,1), n_candidates, p=(1-reelection, reelection))
        
        candidate_dist = self._make_distribution(n_candidates, dist_type)
        candidate_list = ['C%i' % i for i in range(n_candidates)]
        
        candidates = np.array([Candidate(x, y, i, r) for (x,y),i,r in zip(candidate_dist,candidate_list, reelection)])
        self.candidates = candidates
        return candidates
        
    def _run_primary_voting(self):        
        closest_candidates = self.process_all_voters(self.voters, self.candidates)
        for v in self.voters:
            res = v.vote_choice(self.candidates, closest_candidates)

        ls = {c : 0 for c in self.candidates}
        
#         print(ls)
        
        for v in self.voters:
            if v.candidate_choice is not None:
                vchoice = v.candidate_choice
#                 print(vchoice)
                ls[vchoice] += 1
        
        return ls
    
    def _run_general_voting(self, primary_results):
                
        top_2 = Counter(primary_results).most_common(2)
        top_2_ls = [c[0] for c in top_2]
        
#         print(top_2_ls)

        ls = {c : 0 for c in top_2_ls}
        
        for v in self.voters:
            res = v.closest_candidate(top_2_ls)
            ls[res] += 1
        
        return ls
    

    def _run_voting(self):
        self._make_new_candidates(self.c_min, self.c_max, self.dist_type_c, self.reelection)
        
        primary_results = self._run_primary_voting()
    
        results = self._run_general_voting(primary_results)
        
        return Counter(results)
    
    def vote_cycle(self):
        results = self._run_voting()
        winner = max(results, key=results.get)
        
        for v in self.voters:
            v.reward(winner)
    
    def run(self):
        for i in range(self.run_steps):
            self.vote_cycle()
    
    def aggregate_scores(self):
        
        optimizers = [i.current_score() for i in self.voters if i.voter_type == "PrimaryOptimizingVoter"]
        greedy = [i.current_score() for i in self.voters if i.voter_type == "GreedyVoter"]
        center = [i.current_score() for i in self.voters if i.voter_type == "CenterInformedVoter"]

        optimizer_avg = sum(optimizers) / len(optimizers)
        greedy_avg = sum(greedy) / len(greedy)
        center_avg = sum(center) / len(center)
        
        return optimizer_avg, greedy_avg, center_avg

if __name__ == "__main__":
    j = Runner()
    j.get_voters()
    j.run()
    # j.candidates
    j.get_voters()
    print(j.aggregate_scores())
