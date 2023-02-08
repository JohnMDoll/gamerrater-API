"""View module for handling requests about games"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from raterapi.models import Game, GameReview, Player


class ReviewView(ViewSet):
    """Gamerrater review view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single review

        Returns:
            Response -- JSON serialized review
        """
        review = GameReview.objects.get(pk=pk)
        serializer = GameReviewSerializer(review)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all reviews

        Returns:
            Response -- JSON serialized list of reviews
        """
        reviews = GameReview.objects.all()
        serializer = GameReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST requests to create a new review

        Returns:
            Response -- None, 201 status
        """
        new_game_review = GameReview()
        new_game_review.player = Player.objects.get(user=request.auth.user)
        new_game_review.game = Game.objects.get(pk=request.data['gameId'])
        new_game_review.review = request.data['review']
        new_game_review.save()

        # reviews_selected = request.data['reviews']

        # for review in reviews_selected:
        #     monkey = GameReview()
        #     monkey.game = new_game #   <--- this is an object instance of a game
        #     monkey.review = GameReview.objects.get(pk = review)#   <--- this is an object instance of a review
        #     monkey.save()
        serializer = GameReviewSerializer(new_game_review)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# class GameGameReviewSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Review
#         fields = ( 'label', )

class GameReviewSerializer(serializers.ModelSerializer):
    """JSON serializer for review"""
    # reviews = GameGameReviewSerializer(many=True)

    class Meta:
        model = GameReview
        fields = ( 'id', 'review', 'player', 'game', 'date_reviewed' )