from django.db import models


class GameRating(models.Model):

    rating = models.IntegerField( )
    player = models.ForeignKey('Player', related_name='player_ratings', on_delete=models.CASCADE)
    game = models.ForeignKey('Game', on_delete=models.CASCADE, related_name='game_ratings')
    date_rated = models.DateTimeField(auto_now_add=True)