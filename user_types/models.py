from django.db import models
from django.contrib.auth.models import User
from backend.model_choices import *
from backend.models import Skill, Activity, Organisation



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(
        max_length=4,
        choices=TITLE_CHOICES,
        blank=True
    )
    mobile = models.CharField(max_length=20,blank=True)
    postcode = models.CharField(max_length=10,blank=True)
    # address, and many other possible common properties

    def __str__(self):
        return ('%s %s' % (self.user.first_name, self.user.last_name))


class Volunteer(UserProfile): # extends UserProfile
#class Volunteer(models.Model):
#    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    skills = models.ManyToManyField(Skill)
    activitys = models.ManyToManyField(Activity)
    range = models.PositiveSmallIntegerField(choices=RANGE_CHOICES,null=True)

    def __str__(self):
        return ('%s %s' % (self.user.first_name, self.user.last_name))


class Org_user(models.Model): # has one to one rel with UserProfile
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    organisations = models.ManyToManyField(Organisation)

    def __str__(self):
        return ('%s %s' % (self.user.first_name, self.user.last_name))
