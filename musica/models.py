from django.db import models

# Create your models here.


class Artistas(models.Model):
    id = models.CharField(primary_key=True, max_length=22)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    albums = models.CharField(max_length=200)
    tracks = models.CharField(max_length=200)
    self = models.CharField(max_length=200)


class Album(models.Model):
    id = models.CharField(primary_key=True, max_length=22)
    artist_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    artist = models.CharField(max_length=200)
    tracks = models.CharField(max_length=200)
    self = models.CharField(max_length=200)
    padre = models.ForeignKey(Artistas, on_delete=models.CASCADE)


class Cancion(models.Model):
    id = models.CharField(primary_key=True, max_length=22)
    album_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    duration = models.FloatField()
    times_played = models.IntegerField()
    artist = models.CharField(max_length=200)
    album = models.CharField(max_length=200)
    self = models.CharField(max_length=200)
    padre = models.ForeignKey(Album, on_delete=models.CASCADE)
