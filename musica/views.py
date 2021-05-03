from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . models import Artistas, Album, Cancion
from . serializers import ArtistasSerializer, AlbumsSerializer, CancionesSerializer
from base64 import b64encode
# Create your views here.


class ArtistasList(APIView):
    def get(self, request):
        artistas = Artistas.objects.all()
        serializer = ArtistasSerializer(artistas, many=True)
        return Response(serializer.data)

    def post(self, request):
        info = request.data
        id = b64encode(info['name'].encode()).decode('utf-8')
        albums = "https://tarea2pvlecaros.herokuapp.com/"+id+"/albums"
        tracks = "https://tarea2pvlecaros.herokuapp.com/"+id+"/tracks"
        yo = "https://tarea2pvlecaros.herokuapp.com/artists/"+id
        edad = int(info['age'])
        nuevo_artista = Artistas.objects.create(id=id, name=info['name'], age=edad, albums=albums, tracks=tracks)
        nuevo_artista.self = yo
        nuevo_artista.save()
        serializer = ArtistasSerializer(nuevo_artista)
        return Response(serializer.data)


class AlbumsList(APIView):
    def get(self, request):
        albums = Album.objects.all()
        serializer = AlbumsSerializer(albums, many=True)
        return Response(serializer.data)


class CancionesList(APIView):
    def get(self, request):
        canciones = Cancion.objects.all()
        serializer = CancionesSerializer(canciones, many=True)
        return Response(serializer.data)


class ArtistasUnico(APIView):
    def get(self, request, id):
        artista = Artistas.objects.get(id=id)
        serializer = ArtistasSerializer(artista)
        return Response(serializer.data)

    def delete(self, request, id):
        Artistas.objects.get(id=id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AlbumsUnico(APIView):
    def get(self, request, id):
        album = Album.objects.get(id=id)
        serializer = AlbumsSerializer(album)
        return Response(serializer.data)

    def delete(self, request, id):
        Album.objects.get(id=id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CancionesUnico(APIView):
    def get(self, request, id):
        cancion = Cancion.objects.get(id=id)
        serializer = CancionesSerializer(cancion)
        return Response(serializer.data)

    def delete(self, request, id):
        Cancion.objects.get(id=id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AlbumsArtista(APIView):
    def get(self, request, id):
        albums = Album.objects.all().filter(artist_id=id)
        serializer = AlbumsSerializer(albums, many=True)
        return Response(serializer.data)

    def post(self, request, id):
        info = request.data
        id1 = info['name']+":"+id
        id1 = b64encode(id1.encode()).decode('utf-8')
        artista = Artistas.objects.get(id=id)
        if len(id1) > 22:
            id1 = id1[0:22]
        artist = "https://tarea2pvlecaros.herokuapp.com/artists/"+id
        tracks = "https://tarea2pvlecaros.herokuapp.com/albums/"+id1+"/tracks"
        yo = "https://tarea2pvlecaros.herokuapp.com/albums/"+id1
        nuevo_album = Album.objects.create(id=id1, artist_id=id, name=info['name'], genre=info['genre'], artist=artist, tracks=tracks, padre=artista)
        nuevo_album.self = yo
        nuevo_album.save()
        serializer = AlbumsSerializer(nuevo_album)
        return Response(serializer.data)


class CancionesArtista(APIView):
    def get(self, request, id):
        albums = Album.objects.all().filter(artist_id=id)
        serializer = AlbumsSerializer(albums, many=True)
        lista = []
        for album in serializer.data:
            canciones = Cancion.objects.all().filter(album_id=album['id'])
            serializer1 = CancionesSerializer(canciones, many=True)
            for cancion in serializer1.data:
                lista.append(cancion)
        return Response(lista)


class CancionesAlbum(APIView):
    def get(self, request, id):
        canciones = Cancion.objects.all().filter(album_id=id)
        serializer = CancionesSerializer(canciones, many=True)
        return Response(serializer.data)

    def post(self, request, id):
        info = request.data
        id1 = info['name']+":"+id
        id1 = b64encode(id1.encode()).decode('utf-8')
        padre = Album.objects.get(id=id)
        if len(id1) > 22:
            id1 = id1[0:22]
        id_artista = Album.objects.get(id=id)
        id_artista = id_artista.artist_id
        artist= "https://tarea2pvlecaros.herokuapp.com/artists/"+id_artista
        album= "https://tarea2pvlecaros.herokuapp.com/albums/"+id
        yo = "https://tarea2pvlecaros.herokuapp.com/tracks/"+id1
        nueva_cancion = Cancion.objects.create(id=id1, album_id=id, name=info['name'], duration=float(info['duration']), times_played=0, artist=artist , album=album, padre=padre)
        nueva_cancion.self = yo
        nueva_cancion.save()
        serializer = CancionesSerializer(nueva_cancion)
        return Response(serializer.data)


class CancionPlay(APIView):
    def put(self, request, id):
        cancion = Cancion.objects.get(id=id)
        cancion.times_played += 1
        cancion.save()
        return Response(status=status.HTTP_200_OK)


class AlbumPlay(APIView):
    def put(self, request, id):
        canciones = Cancion.objects.all().filter(album_id=id)
        for cancion in canciones:
            cancion.times_played += 1
            cancion.save()
        return Response(status=status.HTTP_200_OK)


class ArtistaPlay(APIView):
    def put(self, request, id):
        albums = Album.objects.all().filter(artist_id=id)
        for album in albums:
            canciones = Cancion.objects.all().filter(album_id=album.id)
            for cancion in canciones:
                cancion.times_played += 1
                cancion.save()
        return Response(status=status.HTTP_200_OK)


