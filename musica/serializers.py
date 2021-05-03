from rest_framework import serializers
from . models import Artistas, Album, Cancion

class ArtistasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artistas
        fields = '__all__'

class AlbumsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ('id', 'artist_id', 'name', 'genre', 'artist', 'tracks', 'self')

class CancionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cancion
        fields = ('id', 'album_id', 'name', 'duration', 'times_played', 'artist', 'album', 'self')