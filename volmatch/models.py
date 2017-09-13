from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User
from .model_choices import *

# Create your models here.

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


class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(
        max_length=4,
        choices=TITLE_CHOICES,
        blank=True
    )
    mobile = models.CharField(max_length=20,blank=True)
    postcode = models.CharField(max_length=10,blank=True)

    def __str__(self):
        return ('%s %s' % (self.user.first_name, self.user.last_name))

class Volunteer(UserProfile):
    skills = models.ManyToManyField(Skill)
    activitys = models.ManyToManyField(Activity)

    def __str__(self):
        return ('%s %s' % (self.user.first_name, self.user.last_name))
