"""tarea2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from musica import views

urlpatterns = [
    path('admin', admin.site.urls),
    path('artists', views.ArtistasList.as_view()),
    path('albums', views.AlbumsList.as_view()),
    path('tracks', views.CancionesList.as_view()),
    path('artists/<str:id>', views.ArtistasUnico.as_view()),
    path('albums/<str:id>', views.AlbumsUnico.as_view()),
    path('tracks/<str:id>', views.CancionesUnico.as_view()),
    path('artists/<str:id>/albums', views.AlbumsArtista.as_view()),
    path('artists/<str:id>/tracks', views.CancionesArtista.as_view()),
    path('albums/<str:id>/tracks', views.CancionesAlbum.as_view()),
    path('albums/<str:id>/tracks/play', views.AlbumPlay.as_view()),
    path('artists/<str:id>/albums/play', views.ArtistaPlay.as_view()),
    path('tracks/<str:id>/play', views.CancionPlay.as_view()),
]
