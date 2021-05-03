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
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        info = request.data
        if "name" not in info.keys() or "age" not in info.keys():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if type(info['name']) != str or type(info['age']) != int:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        id = b64encode(info['name'].encode()).decode('utf-8')
        if len(id) > 22:
            id = id[0:22]
        artista = Artistas.objects.all().filter(id=id)
        if artista:
            serializer = ArtistasSerializer(artista, many=True)
            return Response(serializer.data[0], status=status.HTTP_409_CONFLICT)
        albums = "https://tarea2pvlecaros.herokuapp.com/artists/"+id+"/albums"
        tracks = "https://tarea2pvlecaros.herokuapp.com/artists/"+id+"/tracks"
        yo = "https://tarea2pvlecaros.herokuapp.com/artists/"+id
        edad = info['age']
        nuevo_artista = Artistas.objects.create(id=id, name=info['name'], age=edad, albums=albums, tracks=tracks)
        nuevo_artista.self = yo
        nuevo_artista.save()
        serializer = ArtistasSerializer(nuevo_artista)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AlbumsList(APIView):
    def get(self, request):
        albums = Album.objects.all()
        serializer = AlbumsSerializer(albums, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CancionesList(APIView):
    def get(self, request):
        canciones = Cancion.objects.all()
        serializer = CancionesSerializer(canciones, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ArtistasUnico(APIView):
    def get(self, request, id):
        artista = Artistas.objects.all().filter(id=id)
        if artista:
            serializer = ArtistasSerializer(artista, many=True)
            return Response(serializer.data[0], status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        artista = Artistas.objects.all().filter(id=id)
        if artista:
            Artistas.objects.get(id=id).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)


class AlbumsUnico(APIView):
    def get(self, request, id):
        album = Album.objects.all().filter(id=id)
        if album:
            serializer = AlbumsSerializer(album, many=True)
            return Response(serializer.data[0], status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        album = Album.objects.all().filter(id=id)
        if album:
            Album.objects.get(id=id).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)


class CancionesUnico(APIView):
    def get(self, request, id):
        cancion = Cancion.objects.all().filter(id=id)
        if cancion:
            serializer = CancionesSerializer(cancion, many=True)
            return Response(serializer.data[0], status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        cancion = Cancion.objects.all().filter(id=id)
        if cancion:
            Cancion.objects.get(id=id).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)


class AlbumsArtista(APIView):
    def get(self, request, id):
        artista = Artistas.objects.all().filter(id=id)
        if not artista:
            return Response(status=status.HTTP_404_NOT_FOUND)
        albums = Album.objects.all().filter(artist_id=id)
        if albums:
            serializer = AlbumsSerializer(albums, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, id):
        info = request.data
        if "name" not in info.keys() or "genre" not in info.keys():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if type(info['name']) != str or type(info['genre']) != str:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        artista = Artistas.objects.all().filter(id=id)
        if not artista:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        id1 = info['name']+":"+id
        id1 = b64encode(id1.encode()).decode('utf-8')
        if len(id1) > 22:
            id1 = id1[0:22]
        album = Album.objects.all().filter(id=id1)
        if album:
            serializer = AlbumsSerializer(album, many=True)
            return Response(serializer.data[0], status=status.HTTP_409_CONFLICT)
        artista = Artistas.objects.get(id=id)
        artist = "https://tarea2pvlecaros.herokuapp.com/artists/"+id
        tracks = "https://tarea2pvlecaros.herokuapp.com/albums/"+id1+"/tracks"
        yo = "https://tarea2pvlecaros.herokuapp.com/albums/"+id1
        nuevo_album = Album.objects.create(id=id1, artist_id=id, name=info['name'], genre=info['genre'], artist=artist, tracks=tracks, padre=artista)
        nuevo_album.self = yo
        nuevo_album.save()
        serializer = AlbumsSerializer(nuevo_album)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CancionesArtista(APIView):
    def get(self, request, id):
        artista = Artistas.objects.all().filter(id=id)
        if not artista:
            return Response(status=status.HTTP_404_NOT_FOUND)
        albums = Album.objects.all().filter(artist_id=id)
        serializer = AlbumsSerializer(albums, many=True)
        lista = []
        for album in serializer.data:
            canciones = Cancion.objects.all().filter(album_id=album['id'])
            serializer1 = CancionesSerializer(canciones, many=True)
            for cancion in serializer1.data:
                lista.append(cancion)
        return Response(lista, status=status.HTTP_200_OK)


class CancionesAlbum(APIView):
    def get(self, request, id):
        album = Album.objects.all().filter(id=id)
        if not album:
            return Response(status=status.HTTP_404_NOT_FOUND)
        canciones = Cancion.objects.all().filter(album_id=id)
        serializer = CancionesSerializer(canciones, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, id):
        album = Album.objects.all().filter(id=id)
        if not album:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        info = request.data
        if "name" not in info.keys() or "duration" not in info.keys():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if type(info['name']) != str or type(info['duration']) != float:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        id1 = info['name']+":"+id
        id1 = b64encode(id1.encode()).decode('utf-8')
        if len(id1) > 22:
            id1 = id1[0:22]
        cancion = Cancion.objects.all().filter(id=id1)
        if cancion:
            serializer = CancionesSerializer(cancion, many=True)
            return Response(serializer.data[0], status=status.HTTP_409_CONFLICT)
        padre = Album.objects.get(id=id)
        id_artista = Album.objects.get(id=id)
        id_artista = id_artista.artist_id
        artist= "https://tarea2pvlecaros.herokuapp.com/artists/"+id_artista
        album= "https://tarea2pvlecaros.herokuapp.com/albums/"+id
        yo = "https://tarea2pvlecaros.herokuapp.com/tracks/"+id1
        nueva_cancion = Cancion.objects.create(id=id1, album_id=id, name=info['name'], duration=float(info['duration']), times_played=0, artist=artist , album=album, padre=padre)
        nueva_cancion.self = yo
        nueva_cancion.save()
        serializer = CancionesSerializer(nueva_cancion)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CancionPlay(APIView):
    def put(self, request, id):
        cancion = Cancion.objects.all().filter(id=id)
        if not cancion:
            return Response(status=status.HTTP_404_NOT_FOUND)
        cancion = Cancion.objects.get(id=id)
        cancion.times_played += 1
        cancion.save()
        return Response(status=status.HTTP_200_OK)


class AlbumPlay(APIView):
    def put(self, request, id):
        album = Album.objects.all().filter(id=id)
        if not album:
            return Response(status=status.HTTP_404_NOT_FOUND)
        canciones = Cancion.objects.all().filter(album_id=id)
        for cancion in canciones:
            cancion.times_played += 1
            cancion.save()
        return Response(status=status.HTTP_200_OK)


class ArtistaPlay(APIView):
    def put(self, request, id):
        artista = Artistas.objects.all().filter(id=id)
        if not artista:
            return Response(status=status.HTTP_404_NOT_FOUND)
        albums = Album.objects.all().filter(artist_id=id)
        for album in albums:
            canciones = Cancion.objects.all().filter(album_id=album.id)
            for cancion in canciones:
                cancion.times_played += 1
                cancion.save()
        return Response(status=status.HTTP_200_OK)


