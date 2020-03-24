from django.db import models
from django import forms
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from django.db import models
from django.contrib.gis.db import models
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver

class User(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    display_name = models.CharField(max_length=15)
    email = models.CharField(max_length=75)
    password = models.CharField(max_length=20)

    def __str__(self):
        return self.first_name

class Package(models.Model):
    origination = models.PointField()
    destination = models.CharField(max_length=250)
    length = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()
    weight = models.IntegerField()
    is_fragile = models.BooleanField()
    destination_length = models.IntegerField()
    cost_of_delivery = models.IntegerField()
    completed = models.BooleanField(default=False)
    users = models.ManyToManyField(User)

    def get_absolute_url(self):
        return reverse('detail', kwargs={'pkg_id': self.id})
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()