from rest_framework import serializers

from .models import VotingParameters

class VotingParametersSerializer(serializers.ModelSerializer):
    """ Need a better description for what a serializer does """
    # https://www.django-rest-framework.org/tutorial/1-serialization/
    id = serializers.IntegerField(read_only=True)

    n_greedy = serializers.IntegerField()
    n_optimizing = serializers.IntegerField()
    n_center = serializers.IntegerField()
    distribution_choice = serializers.CharField()

    class Meta:
        model = VotingParameters
        fields = ['id', 'created', 'n_greedy', 'n_optimizing', 'n_center', 'distribution_choice']

    def create(self, validated_data):
        return VotingParameters.objects.create(**validated_data)

    def validate(self, data):
        """ Check that the parameters work """
        if (data['n_greedy'] < 1 or data['n_optimizing'] < 1 or data['n_center'] < 1):
            raise serializers.ValidationError("Must have at least 1 voter of type")
            # update code so will not be a problem in the future

        if data['distribution_choice'] not in ["normal", "uniform", "bimodal_normal"]:
            raise serializers.ValidationError("Invalid Distribution Choice")

        return data
