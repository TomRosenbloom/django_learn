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


class Role(models.Model):
    role_name = models.CharField(max_length=255,unique=True)

    def __str__(self):
        return self.role_name


class Person(models.Model):
    MR = 'MR'
    MRS = 'MRS'
    MS = 'MS'
    SIR = 'SIR'
    TITLE_CHOICES = (
        (MR, 'Mr'),
        (MRS, 'Mrs'),
        (MS, 'Ms'),
        (SIR, 'Sir'),
    )
    MALE = 'MALE'
    FEMALE = 'FEMALE'
    SEX_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )
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
    role = models.ManyToManyField(Role,related_name='role',through='Person_org_role')
    organisation = models.ManyToManyField(Organisation,related_name='organisation',through='Person_org_role')

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
