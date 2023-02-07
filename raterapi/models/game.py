from django.db import models

class Game(models.Model):

    title = models.CharField( max_length=100)
    designer = models.CharField( max_length=100)
    description = models.CharField( max_length=300)
    year_released = models.IntegerField()
    min_number_of_players = models.IntegerField()
    max_number_of_players = models.IntegerField(default= min_number_of_players)
    est_play_time = models.IntegerField()
    min_age = models.IntegerField()
    categories =  models.ManyToManyField('Category', through='GameCategory')