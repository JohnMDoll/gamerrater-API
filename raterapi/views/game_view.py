"""View module for handling requests about games"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from gamerraterapi.models import Game, GameCategory, Category


class GameView(ViewSet):
    """Gamerrater game view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game

        Returns:
            Response -- JSON serialized game
        """
        game = Game.objects.get(pk=pk)
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
        new_game.save()

        # categories_selected = request.data['categories']

        # for category in categories_selected:
        #     monkey = GameCategory()
        #     monkey.game = new_game #   <--- this is an object instance of a game
        #     monkey.category = Category.objects.get(pk = category)#   <--- this is an object instance of a category
        #     monkey.save()

        serializer = GameSerializer(new_game)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class GameCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ( 'label', )


class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for game"""
    categories = GameCategorySerializer(many=True)

    class Meta:
        model = Game
        fields = (
            'id', 'title', 'description', 'designer', 'year_released',
            'min_number_of_players', 'max_number_of_players', 'est_play_time', 'min_age',
            'categories'
        )