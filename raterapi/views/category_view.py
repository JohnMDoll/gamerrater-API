"""View module for handling requests about games"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from raterapi.models import Game, GameCategory, Category


class CategoryView(ViewSet):
    """Gamerrater category view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single category

        Returns:
            Response -- JSON serialized category
        """
        category = Category.objects.get(pk=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all categories

        Returns:
            Response -- JSON serialized list of categories
        """
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST requests to create a new category

        Returns:
            Response -- None, 201 status
        """
        new_game_category = GameCategory()
        new_game_category.game = Game.objects.get(pk=request.data['gameId'])
        new_game_category.category = Category.objects.get(pk=request.data['categoryId'])
        new_game_category.save()

        # categories_selected = request.data['categories']

        # for category in categories_selected:
        #     monkey = GameCategory()
        #     monkey.game = new_game #   <--- this is an object instance of a game
        #     monkey.category = Category.objects.get(pk = category)#   <--- this is an object instance of a category
        #     monkey.save()

        return Response(None, status=status.HTTP_201_CREATED)

# class GameCategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = ( 'label', )

class CategorySerializer(serializers.ModelSerializer):
    """JSON serializer for category"""
    # categories = GameCategorySerializer(many=True)

    class Meta:
        model = Category
        fields = ( 'id', 'label' )