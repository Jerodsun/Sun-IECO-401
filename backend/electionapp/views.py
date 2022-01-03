from django.shortcuts import render
from rest_framework import views, viewsets, status
from rest_framework.response import Response

import json

from .models import VotingParameters
from .serializers import VotingParametersSerializer

from .functions.runner import Runner

# Create your views here.

class VotingParametersView(viewsets.ModelViewSet):
    
    serializer_class = VotingParametersSerializer
    queryset = VotingParameters.objects.all()
    http_method_names = ['get', 'post']

    def create(self, request):
        serializer = VotingParametersSerializer(data=request.data)
        if serializer.is_valid():
            d = serializer.validated_data
            # print(d)
            # use the function here
            j = Runner(n_greedy=d['n_greedy'], n_optimizing = d['n_optimizing'], n_center = d['n_center'], dist_type_v = d['distribution_choice'])
            j.run()
            greedy, optimizing, center = j.aggregate_scores()

            serializer.save()
            return Response({'message':'success', 'greedy': greedy, 'optimizing' : optimizing, 'center' : center, 'params': d})
        return Response({'message':'error'})
