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
    creator = models.ForeignKey('Player', default=1, null=True, on_delete=models.DO_NOTHING, related_name="player_games")

    @property
    def can_edit(self):
        return self.__can_edit

    @can_edit.setter
    def can_edit(self, value):
        self.__can_edit = value