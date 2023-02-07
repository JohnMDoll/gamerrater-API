from django.db import models


class GameCategory(models.Model):

    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='category_games')
    game = models.ForeignKey('Game', on_delete=models.CASCADE, related_name='game_categories')