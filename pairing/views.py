from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from pairing.models import Player, Result, Standing
from pairing.serializers import PlayerSerializer, ResultSerializer,\
    StandingSerializer 
from pairing import utils
from rest_framework.decorators import list_route

class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    
    def retrieve(self, request, pk):
        player = self.queryset.select_related('results').get(pk)
        return Response(self.serializer_class(player))
    
class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    
    def list(self, request):
        rnd = utils.get_current_round()
        serializer = self.serializer_class(self.queryset.filter(game=rnd),many=True)
        
        return Response(serializer.data)
    
class RoundViewSet(viewsets.ViewSet):
    '''
    Isn't backed by a model. Rounds do not have a model
    '''
    def create(self, request):
        if not utils.validate_players():
            return Response({'error': 'Odd number of players','code': 1}, status.HTTP_412_PRECONDITION_FAILED)
        if not utils.validate_results():
            return Response({'error': 'Results incomplete','code': 2}, status.HTTP_412_PRECONDITION_FAILED)

        rnd = utils.get_current_round()
            
        utils.make_pairing(rnd+1)
        
        return Response({'status': 'OK'})
    
    def retrieve(self, request, pk=None):
        serializer = ResultSerializer(Result.objects.filter(game=pk), many=True)
        return Response({'id': pk , 'results': serializer.data})
                                      
    def list(self, request):
        rnd = utils.get_current_round()+1
        
        return Response([{'id': i} for i in range(1, rnd)])
    
    
class StandingViewSet(viewsets.ModelViewSet):
    queryset = Standing.objects.all()
    serializer_class = StandingSerializer
