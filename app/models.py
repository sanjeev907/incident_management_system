from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

# Create your models here.

CATEGORIES = (
    ('faridabad', 'faridabad'),
    ('gurugram', 'gurugram'),
    ('ambala', 'ambala'),
    ('karnal', 'karnal'),
    ('hisar', 'hisar'),
    ('panipat', 'panipat'),
)



class User(AbstractUser):       
    phone_number = models.CharField(blank=True,max_length=150)
    state = models.CharField(blank=True,max_length=150)
    country = models.CharField(blank=True,max_length=150)
    fax = models.CharField(blank=True,max_length=150)
    pincode = models.CharField(blank=True,max_length=150)
    address = models.CharField(max_length=150)
    city = models.CharField(max_length=50, choices=CATEGORIES, default='faridabad')
    groups = models.ManyToManyField('auth.Group', blank=True, related_name='app_user')
    user_permissions = models.ManyToManyField('auth.Permission', blank=True, related_name='app_users_permissions')


class Incident(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,  related_name="user_incident")
    incident = models.TextField()
    incident_date = models.DateField(auto_now=True)
    incident_modify_date = models.DateField(auto_now=False)