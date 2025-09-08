from django.db import models
#this contrib auth is used for user login logout etc
from django.contrib.auth.models import AbstractUser
#below are django ORM classes represents database tables


class User(AbstractUser):
    pass

class Lead(models.Model):
    first_name= models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    age= models.IntegerField(default=0)
#links each lead to an agent,if agent is deleted all leads will be deleted too
    agent= models.ForeignKey("Agent", on_delete=models.CASCADE)
    
#agent who manages leads  
class Agent(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE)
   