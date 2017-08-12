from django.db import models
from address.models import AddressField
from django.contrib.auth.models import User

from backend.model_choices import *

# Create your models here.

class Funder(models.Model):
    funder_name = models.CharField(max_length=255,unique=True)

    def __str__(self):
        return self.funder_name


class Project(models.Model):
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


class Role(models.Model):
    role_name = models.CharField(max_length=255,unique=True)

    def __str__(self):
        return self.role_name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(
        max_length=4,
        choices=TITLE_CHOICES,
        blank=True
    )
    sex = models.CharField(
        max_length=6,
        choices=SEX_CHOICES,
        blank=True
    )
    mobile = models.CharField(max_length=20,blank=True)
    address = AddressField(blank=True, null=True)
    postcode = models.CharField(max_length=10,blank=True)
    range = models.PositiveSmallIntegerField(choices=RANGE_CHOICES,null=True)
    is_volunteer = models.NullBooleanField()
    is_org_member = models.NullBooleanField()

    def __str__(self):
        return ('%s %s' % (self.user.first_name, self.user.last_name))


class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    title = models.CharField(
        max_length=4,
        choices=TITLE_CHOICES,
        blank=True
    )
    dob = models.DateField(blank=True, null=True)
    sex = models.CharField(
        max_length=6,
        choices=SEX_CHOICES,
        blank=True
    )
    mobile = models.CharField(max_length=20,blank=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    address = AddressField(blank=True, null=True)
    is_volunteer = models.NullBooleanField()
    is_org_member = models.NullBooleanField()
    role = models.ManyToManyField(Role,related_name='person_role',through='Person_org_role')
    organisation = models.ManyToManyField(Organisation,related_name='person_organisation',through='Person_org_role')

    def __str__(self):
        return ('%s %s' % (self.first_name, self.last_name))

class Person_org_role(models.Model):
    person = models.ForeignKey('Person')
    organisation = models.ForeignKey('Organisation')
    role = models.ForeignKey('Role')

    class Meta:
        unique_together = (("person", "organisation", "role"),)

    def __str__(self):
        return ('%s, %s, %s' % (self.person, self.role, self.organisation))
