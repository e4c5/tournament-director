from django.db.models import Q
from pairing.models import Player, Result , Standing
from rest_framework import serializers
from django.core.exceptions import ValidationError

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'
        read_only_fields = ('id',)
        

class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = '__all__'
        read_only_fields = ('id',)
        depth = 1
        
class ResultUpdateSerializer(serializers.Serializer):
    player1 = serializers.CharField()
    player2 = serializers.CharField()
    score1 = serializers.IntegerField()
    score2 = serializers.IntegerField()
    game = serializers.IntegerField()
    
    def validate(self, data):
        if Result.objects.filter( Q(game=data['game']) 
                                & Q(player1__name=data['player1']) 
                                & Q(player2__name=data['player2'])).count() != 1:
            raise ValidationError("Invalid pairing")
    
        return data
    
    
class StandingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Standing
        fields = '__all__'
        read_only_fields = ('id',)
        