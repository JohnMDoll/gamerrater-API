"""View module for handling requests about games"""
from django.http import HttpResponseServerError
from django.db.models import Count, Q, Case, When
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

        return Response(None, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for game categories

        Returns:
            Response -- Empty body with 204 status code
        """
        game = Game.objects.get(pk=request.data['gameId'])
        player = game.creator

        client_categories = set(request.data['categories'])

        all_relationships = GameCategory.objects.filter(game=game)
        game_categories = all_relationships.filter(game=game, category_id__in=request.data['categories'])
        good_categories = set(game_categories.values_list('category_id'))
        all_categories = set(all_relationships.values_list('category_id', flat=True))
        # create and delete
        overlap = all_categories.symmetric_difference(client_categories)
        #delete
        delete_categories = overlap.difference(client_categories)
        all_relationships.filter(category_id__in=list(delete_categories)).delete()
        #create
        create_categories = overlap.intersection(client_categories)

        for good_category in create_categories:
            
            # category_type = Category.objects.get(pk=request_category)
            new_game_cat = GameCategory()
            new_game_cat.game = game
            new_game_cat.player = player
            new_game_cat.category_id = good_category
            new_game_cat.save()
                # else:
                #     if cat.category_id not in request.data['categories']:

        # for category in game_categories:
        #     if category.category_id not in request.data['categories']:
        #         # print(f"delete category {category}")
        #         category.delete()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

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