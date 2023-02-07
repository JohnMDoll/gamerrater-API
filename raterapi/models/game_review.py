from django.db import models


class GameReview(models.Model):

    review = models.CharField( max_length=500)
    player = models.ForeignKey('Player', related_name='player_reviews', on_delete=models.CASCADE)
    game = models.ForeignKey('Game', on_delete=models.CASCADE, related_name='game_reviews')
    date_reviewed = models.DateTimeField(auto_now_add=True)