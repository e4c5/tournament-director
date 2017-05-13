from pairing.models import Player, Result , Standing
from rest_framework.serializers import ModelSerializer

class PlayerSerializer(ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'
        read_only_fields = ('id',)
        

class ResultSerializer(ModelSerializer):
    class Meta:
        model = Result
        fields = '__all__'
        read_only_fields = ('id',)
        depth = 1
        
class StandingSerializer(ModelSerializer):
    class Meta:
        model = Standing
        fields = '__all__'
        read_only_fields = ('id',)
        