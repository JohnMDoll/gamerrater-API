"""View module for handling requests about games"""
from django.http import HttpResponseServerError
from django.db.models import Count, Q, Case, When
from django.db.models.fields import BooleanField
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from raterapi.models import Game, GameCategory, Category, GameReview, Player


class GameView(ViewSet):
    """Gamerrater game view"""

    # def user_game_edit_check(self, request, creatorId):
    #     '''handles client request to check user against request'''
    #     current_user = Player.objects.get(user=request.auth.user)
    #     request_user = Player.objects.get(pk=creatorId)
    #     if current_user == request_user:
    #         data = {
    #             'can_edit': True,
    #         }
    #         return Response(data)
    #     else:
    #         # User isn't game creator, cannot edit game data
    #         data = {'can_edit': False}
    #         return Response(data)

    def retrieve(self, request, pk):
        """Handle GET requests for single game

        Returns:
            Response -- JSON serialized game
        """
        # game = Game.objects.get(pk=pk)
        game = Game.objects.annotate(can_edit=Case(
            When( 
                creator__user = request.auth.user, then=True
            ),
            default=False,
            output_field=BooleanField()
        )).get(pk=pk)
        serializer = GameSerializer(game)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all games

        Returns:
            Response -- JSON serialized list of games
        """
        games = Game.objects.all()

        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST requests to create a new game

        Returns:
            Response -- JSON serialized dictionary representation of the new game
        """
        new_game = Game()
        new_game.description = request.data['description']
        new_game.title = request.data['title']
        new_game.min_number_of_players = request.data['min_number_of_players']
        new_game.max_number_of_players = request.data['max_number_of_players']
        new_game.est_play_time = request.data['est_play_time']
        new_game.min_age = request.data['min_age']
        new_game.year_released = request.data['year_released']
        new_game.designer = request.data['designer']
        new_game.creator = Player.objects.get(user=request.auth.user)
        new_game.save()

        serializer = GameSerializer(new_game)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GameCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'label', )

# class GameReviewPlayerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Player
#         fields = ( 'full_name', )


class GameReviewSerializer(serializers.ModelSerializer):
    # player = GameReviewPlayerSerializer()
    # replaces commented code but returns fullname to client in .player instead of .player.fullname
    player = serializers.StringRelatedField(source='player.full_name')

    class Meta:
        model = GameReview
        fields = ('id', 'review', 'player', 'date_reviewed')


class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for game"""
    categories = GameCategorySerializer(many=True)
    game_reviews = GameReviewSerializer(many=True)

    class Meta:
        model = Game
        fields = (
            'id', 'title', 'description', 'designer', 'year_released',
            'min_number_of_players', 'max_number_of_players', 'est_play_time', 'min_age',
            'categories', 'game_reviews', 'creator', 'can_edit'
        )
