from django.db import models
from address.models import AddressField
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from ckeditor.fields import RichTextField

from backend.model_choices import *

# Create your models here.

class Postcode(models.Model):
    postcode = models.CharField(max_length=50, unique=True)
    latitude = models.DecimalField(max_digits=14,decimal_places=12)
    longitude = models.DecimalField(max_digits=14,decimal_places=12)

    def __str__(self):
        return self.postcode


class Skill(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name


class Activity(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)

    class Meta:
        ordering = ['tree_id','level','name']

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name


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


class OrganisationType(models.Model):
    name = models.CharField(max_length=255,unique=True)
    acronym = models.CharField(max_length=255,unique=True,blank=True, null=True)

    def __str__(self):
        return self.name


class Organisation(models.Model):
    name = models.CharField(max_length=255,unique=True)
    aims_and_activities = RichTextField(blank=True,null=True)
    email = models.EmailField(blank=True,null=True)
    telephone = models.CharField(max_length=100,blank=True,null=True)
    postcode = models.CharField(max_length=100,blank=True,null=True)
    address = AddressField(blank=True, null=True)
    types = models.ManyToManyField(OrganisationType,through='OrganisationRegistration',blank=True)
    #opportunitys = models.ManyToManyField(Opportunity)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("org_reg:detail", kwargs={'pk':self.pk})


class OrganisationRegistration(models.Model):
    organisation = models.ForeignKey(Organisation)
    type = models.ForeignKey(OrganisationType)
    reg_number = models.CharField(max_length=100,blank=True,null=True)

    def __str__(self):
        return ('%s %s' % (self.type, self.reg_number))



class Opportunity(models.Model):
    name = models.CharField(max_length=255, verbose_name=('Opportunity title'))
    description = RichTextField()
    start_date = models.DateField(blank=True,null=True)
    end_date = models.DateField(blank=True,null=True)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    skills = models.ManyToManyField(Skill,blank=True)
    activitys = models.ManyToManyField(Activity,blank=True)

    def __str__(self):
        return self.name
        return ('%s %s' % (self.name, self.organisation.name))



class Role(models.Model):
    role_name = models.CharField(max_length=255,unique=True)

    def __str__(self):
        return self.role_name
