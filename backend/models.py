from django.db import models
from address.models import AddressField

# Create your models here.

# ok, let's use funding database as example. The tables:
#  project
#  project_status - one-to-one via foreign key
#  funder - one-to-many via lookup table
#  actually to start with I'll just use project and funder as a one-to-one
#  nb could add organisations, where projects involve organisations
class Funder(models.Model):
    funder_name = models.CharField(max_length=255,unique=True)

    def __str__(self):
        return self.funder_name


class Project(models.Model):
    PROPOSED = 'PROP'
    CURRENT = 'CURR'
    COMPLETED = 'COMP'
    STAGE_CHOICES = (
        (PROPOSED, 'Proposed'),
        (CURRENT, 'Current'),
        (COMPLETED, 'Completed'),
    )
    funders = models.ManyToManyField(Funder)
    project_name = models.CharField(max_length=255,unique=True)
    stage = models.CharField(
        max_length=4,
        choices=STAGE_CHOICES,
        blank=True
    )

    def __str__(self):
        return self.project_name


class Organisation(models.Model):
    organisation_name = models.CharField(max_length=255,unique=True)
    aims_and_activities = models.TextField()
    email = models.EmailField(blank=True)
    address = AddressField(blank=True, null=True)

    def __str__(self):
        return self.organisation_name
