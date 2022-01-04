from django.test import TestCase
from rest_framework.test import APIRequestFactory, APITestCase
from rest_framework import status

# Create your tests here.

from electionapp.models import VotingParameters

factory = APIRequestFactory()

class VotingParametersTestCase(TestCase):
    def setUp(self):
        VotingParameters.objects.create(n_greedy=10, n_optimizing=15, n_center=5)

    def test_vote(self):
        """  """
        # once done, make sure base cases are the same with same np.random.seed
        pass