from django.db.models import Q
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from pairing.models import Player, Result, Standing
from pairing import serializers
     
from pairing import utils
from rest_framework.decorators import list_route
from django.db.models.deletion import ProtectedError
from rest_framework.exceptions import APIException

class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'retrieve': return serializers.PlayerDetailSerializer
        else : return serializers.PlayerSerializer
    
    def retrieve(self, request, pk):
        player = self.queryset.get(pk=pk)
        Serial = self.get_serializer_class()
        
        return Response(Serial(player).data)
    
    def update(self, request, pk):
        Serial = self.get_serializer_class();
        s = Serial(self.queryset.get(pk=pk), data=request.data)
        if s.is_valid():
            s.save()
            
        return Response({'status':'OK'})

    def destroy(self, request, pk):
        try :
            return super(PlayerViewSet, self).destroy(request, pk)
        except ProtectedError:
            raise APIException(detail='Player has been paired and cannot be deleted')
        
class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.all()
    serializer_class = serializers.ResultSerializer
    
    def list(self, request):
        '''
        Returns results for the latest rounds.
        
        If results have not yet been entered, the scores will be null. And 
        that gives you the draw for the next round!
        '''
        
        rnd = utils.get_current_round()
        qs = self.queryset.filter(game=rnd)
        serializer = self.serializer_class(qs,many=True)
        
        return Response(serializer.data)
    
    def create(self, request):
        '''
        Note that we use a different serializer here
        '''
        s = serializers.ResultUpdateSerializer(data=request.data)
        if s.is_valid():
            Result.objects.filter( Q(player1__name=s.validated_data['player1']) & 
                                   Q(player2__name=s.validated_data['player2']) &
                                   Q(game=s.validated_data['game'])
                                   ).update(score1=s.validated_data['score1'], score2=s.validated_data['score2'])
            return Response({'status': 'OK'})
        else:
            return Response({'error': 'Players mismatched'}, status=status.HTTP_412_PRECONDITION_FAILED)
    
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
        serializer = serializers.ResultSerializer(Result.objects.filter(game=pk), many=True)
        return Response({'id': pk , 'results': serializer.data})
                                      
    def list(self, request):
        rnd = utils.get_current_round()+1
        
        return Response([{'id': i} for i in range(1, rnd)])
    
    
class StandingViewSet(viewsets.ModelViewSet):
    queryset = Standing.objects.all()
    serializer_class = serializers.StandingSerializer
