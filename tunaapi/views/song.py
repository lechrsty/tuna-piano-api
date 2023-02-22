"""View module for handling requests about song types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Song, Genre, Artist


class SongView(ViewSet):

    def retrieve(self, request, pk):

        song = Song.objects.get(pk=pk)
        serializer = SongSerializer(song)
        return Response(serializer.data)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = SongSerializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        queryset = Song.objects.all()

        genre_id = self.request.query_params.get('genre_id')
        if genre_id is not None:
            queryset = queryset.filter(genre_id=genre_id)

        artist_id = self.request.query_params.get('artist_id')
        if artist_id is not None:
            queryset = queryset.filter(artist_id=artist_id)

        return queryset

    def create(self, request):

        artist = Artist.objects.get(pk=request.data["artist"])
        genre = Genre.objects.get(pk=request.data["genre"])

        song = Song.objects.create(
            title=request.data["title"],
            album=request.data["album"],
            length=request.data["length"],
            genre=genre,
            artist=artist
        )
        serializer = SongSerializer(song)
        return Response(serializer.data)

class ArtistSongSerializer(serializers.ModelSerializer):

    class Meta:
        model = Artist
        fields = ('name',)

class GenreSongSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('description', )

class SongSerializer(serializers.ModelSerializer):

    artist = ArtistSongSerializer(many=False)
    genre = GenreSongSerializer(many=False)

    class Meta:
        model = Song
        fields = ('id', 'title', 'album', 'length', 'genre', 'artist')
        depth = 1
