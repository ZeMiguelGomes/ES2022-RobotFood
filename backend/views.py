from django.shortcuts import render
# import view sets from the REST framework
from rest_framework import viewsets
 
# import the Serializer from the serializer file
from .serializers import UtilizadorSerializer
 
# import the Todo model from the models file
from .models import Utilizador

class UtilizadorView(viewsets.ModelViewSet):
    serializer_class = UtilizadorSerializer
    queryset = Utilizador.objects.all()