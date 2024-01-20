from .models import *
from rest_framework import serializers

class QuoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = quote
        fields = '__all__'
