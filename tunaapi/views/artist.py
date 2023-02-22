from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Song, Artist

def join_songs(view_func):
    def wrapper(*args, **kwargs):
        # Call the actual view function
        response = view_func(*args, **kwargs)

        # Add songs to artist data
        if isinstance(response.data, list):
            for artist_data in response.data:
                artist_id = artist_data['id']
                songs = Song.objects.filter(artist_id=artist_id)
                songs_data = SongSerializer(songs, many=True).data
                artist_data['songs'] = songs_data
        else:
            artist_id = response.data['id']
            songs = Song.objects.filter(artist_id=artist_id)
            songs_data = SongSerializer(songs, many=True).data
            response.data['songs'] = songs_data

        return response
    return wrapper

class ArtistView(ViewSet):

    @join_songs
    def retrieve(self, request, pk):
        artist = Artist.objects.get(pk=pk)
        serializer = ArtistSerializer(artist)
        return Response(serializer.data)

    @join_songs
    def list(self, request):
        artists = Artist.objects.all()
        serializer = ArtistSerializer(artists, many=True)
        return Response(serializer.data)

    @join_songs
    def create(self, request):
        artist = Artist.objects.create(
            name=request.data["name"],
            age=request.data["age"],
            bio=request.data["bio"]
        )

        serializer = ArtistSerializer(artist)
        return Response(serializer.data)

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ('id', 'title', 'album')

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ('id', 'name', 'age', 'bio')
