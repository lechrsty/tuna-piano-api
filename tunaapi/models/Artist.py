from django.db import models

class Artist(models.Model):
    
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    bio = models.CharField(max_length=50)
    songs = models.ForeignKey("Song", on_delete=models.CASCADE, related_name="ArtistSong")