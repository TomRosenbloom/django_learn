from django.db import models
from django.contrib.auth.models import User
from backend.model_choices import *
from backend.models import Skill,Activity



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
