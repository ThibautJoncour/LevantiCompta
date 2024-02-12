# Dans serializers.py
from rest_framework import serializers
from .models import VotreModele

class VotreModeleSerializer(serializers.ModelSerializer):
    class Meta:
        model = VotreModele
        fields = '__all__'
