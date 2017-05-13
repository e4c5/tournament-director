from django.db import models

class Player(models.Model):
    name = models.CharField(max_length=126)
    rating = models.IntegerField()

class Round(models.Model):
    number = models.IntegerField()
    
class Result(models.Model):
    ''' There will be a result object for each participant in a given round '''

    player1 = models.ForeignKey(Player, related_name='player1', on_delete=models.CASCADE)
    player2 = models.ForeignKey(Player, related_name='player2', on_delete = models.CASCADE)
    game  = models.ForeignKey(Round)

    score1 = models.IntegerField(null = True) # scored in this round
    score2 = models.IntegerField(null = True) # scored by opponent

    score1_adjusted = models.IntegerField(null = True) # scored in this round after applying penalties
    score2_adjusted = models.IntegerField(null = True) # scored by opponent after applying penalties
    
class Standing(models.Model):
    player = models.ForeignKey(Player)
    game = models.ForeignKey(Round)
    wins = models.IntegerField() # 0 loss, 1 draw, 2 win
    margin = models.IntegerField()
    