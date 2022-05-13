# import serializers from the REST framework
from rest_framework import serializers
 
# import the data model
from .models import Utilizador
 
# create a serializer class
class UtilizadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilizador
        fields = ('email', 'name', 'password', 'isStaff', 'isWorking')