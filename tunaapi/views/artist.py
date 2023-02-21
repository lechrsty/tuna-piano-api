"""View module for handling requests about artist types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Song, Genre, Artist


class ArtistView(ViewSet):

    def retrieve(self, request, pk):

        artist = Artist.objects.get(pk=pk)
        serializer = ArtistSerializer(artist)
        return Response(serializer.data)


    def list(self, request):

        artists = Artist.objects.all()
        serializer = ArtistSerializer(artists, many=True)
        return Response(serializer.data)

    # def create(self, request):
    #     """Handle POST operations

    #     Returns
    #         Response -- JSON serialized artist instance
    #     """
    #     artist = Artist.objects.get(user=request.auth.user)
    #     genre = Genre.objects.get(pk=request.data["genre"])

    #     artist = Artist.objects.create(
    #         artist=artist,
    #         name=request.data["name"],
    #         age=request.data["age"],
    #         bio=request.data["bio"]
    #     )
    #     serializer = ArtistSerializer(artist)
    #     return Response(serializer.data)

class SongsArtistSerializer(serializers.ModelSerializer):

    class Meta:
        model = Song
        fields = ('id', 'title', 'album' )

class ArtistSerializer(serializers.ModelSerializer):

    songs = SongsArtistSerializer(many=False)

    class Meta:
        model = Artist
        fields = ('id', 'name', 'age', 'bio', 'songs')
        depth = 1
