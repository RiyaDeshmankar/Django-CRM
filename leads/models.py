from django.db import models
#this contrib auth is used for user login logout etc
from django.contrib.auth.models import AbstractUser
#below are django ORM classes represents database tables
from django.db.models.signals import post_save, pre_save
#post_save-	Send notifications or emails 
# pre_save- Modify or validate data before saving

class User(AbstractUser):
    is_organiser=models.BooleanField(default=True)
    is_agent=models.BooleanField(default=False)


class UserProfile(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username
    
class Lead(models.Model):
    first_name= models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    age= models.IntegerField(default=0)
#links each lead to an agent,if agent is deleted all leads will be deleted too
    agent= models.ForeignKey("Agent", on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
#agent who manages leads  
class Agent(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE)
    organisation=models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.user.email
    

def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(post_user_created_signal, sender=User)