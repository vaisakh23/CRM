from django.db import models
from agents.models import Agent
from users.models import UserProfile


class Lead(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField()
    agent = models.ForeignKey(Agent, null=True, blank=True, on_delete=models.SET_NULL)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    category = models.ForeignKey("category", blank=True, null=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Category(models.Model):
    name = models.CharField(max_length=30)  # New, Contacted, Converted, Unconverted
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
