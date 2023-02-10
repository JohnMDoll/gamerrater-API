"""View module for handling requests about games"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from raterapi.models import Game, GameRating, Player


class RatingView(ViewSet):
    """Gamerrater rating view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single rating

        Returns:
            Response -- JSON serialized rating
        """
        rating = GameRating.objects.get(pk=pk)
        serializer = GameRatingSerializer(rating)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all ratings

        Returns:
            Response -- JSON serialized list of ratings
        """
        game = Game.objects.get(pk=request.data['gameId'])
        ratings = GameRating.objects.filter(game)
        serializer = GameRatingSerializer(ratings, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST requests to create a new rating

        Returns:
            Response -- None, 201 status
        """
        new_game_rating = GameRating()
        new_game_rating.player = Player.objects.get(user=request.auth.user)
        new_game_rating.game = Game.objects.get(pk=request.data['gameId'])
        new_game_rating.rating = request.data['rating']
        new_game_rating.save()

        serializer = GameRatingSerializer(new_game_rating)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class GameRatingSerializer(serializers.ModelSerializer):
    """JSON serializer for rating"""

    class Meta:
        model = GameRating
        fields = ( 'id', 'rating', 'player', 'game', 'date_rated' )