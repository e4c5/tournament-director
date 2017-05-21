import random
import sys, os

if __name__ == '__main__': #pragma nocover
    # Setup environ
    sys.path.append(os.getcwd())
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pairing.settings")
    import django
    django.setup()

from pairing.models import Result, Player
from django.db.models import Q

def validate_results():
    if Result.objects.filter( Q(score1=None) | Q(score2=None) ).count() > 0:
        return False
    return True

def validate_players():
    
    if Player.objects.count() % 2 == 0:  return True
    else:  return False


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
    
    
def simulate(player1, player2):
    '''
    Simulate a result using probability and the rating difference.
    
    According to the Australian scrabble rating system, the probability 
    of a higher rated player winning the game is 50% + rating difference/12
    
    So we get two random numbers starting from (zero, win probability). The
    player who gets a higher random number is the winner. 
    
    Each player then gets a score of 1000*random number drawn rounded to the
    nearest int.
    
    To avoid outliers, we also do a random min, max 
    If the rounding results in the numbers being equal then 
    the result is considered to be a tie.
    

    '''
    
    p = 0.50 + abs(1.0*(player1.rating - player2.rating)/1200)

    if player1.rating > player2.rating:
        p1 = random.random()*p
        p2 = random.random()*(1.0 - p)
    else :
        p1 = random.random()*(1.0 - p)
        p2 = random.random()*p
        
    
    s1, s2 = 1000*p1, 1000*p2    
    lower = random.randint(100,200)
    upper = random.randint(500,750)
    
    s1 = max(lower, min(upper, s1))
    s2 = max(lower, min(upper, s2))
    
    return int(s1), int(s2)

if __name__ == '__main__': #pragma nocover
    player1 = Player(rating=1250)
    player2 = Player(rating=1400)
    print (simulate(player1, player2))
