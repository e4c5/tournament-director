from pairing.models import Result, Player
from django.db.models import Q

def validate_results():
    if Result.objects.filter( Q(score1=None) | Q(score2=None) ).count() > 0:
        return False
    return True

def validate_players():
    bye = Player.objects.filter(name = 'Bye').count()
    
    if Player.objects.count() % 2 == 0:
        if bye: return False
    else:
        if not bye: return False
        
    return True


def make_pairing(rnd):
    players = list(Player.objects.order_by('-rating'))
    halfway = len(players) // 2
    for p in range(halfway):
        Result.objects.create(player1=players[p], player2=players[p+halfway],game=rnd)
        

def get_current_round():
    try :
        rnd = Result.objects.order_by('-game')[0]
        return rnd.game
    except IndexError:
        return 0 # tournament hasn't started'