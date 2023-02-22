from django.db import models
from .Song import Song

class Artist(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    bio = models.CharField(max_length=50)
