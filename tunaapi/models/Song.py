from django.db import models

class Song(models.Model):

    title = models.CharField(max_length=55)
    album = models.CharField(max_length=500)
    length = models.IntegerField()
    genre = models.ForeignKey("Genre", on_delete=models.SET_NULL, null=True)
    artist = models.ForeignKey("Artist", on_delete=models.CASCADE, related_name="SongArtist")