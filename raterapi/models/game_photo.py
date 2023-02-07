from django.db import models


class GamePhoto(models.Model):

    image = models.ImageField(null=False)
    player = models.ForeignKey('Player', related_name='player_photos', on_delete=models.CASCADE)
    game = models.ForeignKey('Game', on_delete=models.CASCADE, related_name='game_photos')
    date_added = models.DateTimeField(auto_now=True)