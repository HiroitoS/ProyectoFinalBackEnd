from rest_framework import serializers
from .models import Calificacion,Curso,Horario,Usuario


class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso

        fields = '__all__'


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario

        fields = '__all__'

class CalificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calificacion

        fields = '__all__'

class HorarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Horario

        fields = '__all__'            