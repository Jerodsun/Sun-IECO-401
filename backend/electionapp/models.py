from django.db import models

# Create your models here.

class VotingParameters(models.Model):
    """This is a sample model to store the POST request for the
    calculation. """
    
    created = models.DateTimeField(auto_now_add=True)

    n_greedy = models.IntegerField()
    n_optimizing = models.IntegerField()
    n_center = models.IntegerField()

    NORMAL = 'N'
    UNIFORM = 'U'
    BIMODAL_NORMAL = 'BN'
    
    VOTER_DISTRIBUTION_CHOICES = [
        (NORMAL, 'normal'),
        (UNIFORM, 'uniform'),
        (BIMODAL_NORMAL, 'bimodal_normal')
    ]

    distribution_choice = models.CharField(
        max_length=2,
        choices=VOTER_DISTRIBUTION_CHOICES,
        default=NORMAL,
    )


    class Meta:
        verbose_name_plural = "User Parameters for the Voting Model"

