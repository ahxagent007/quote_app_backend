from .models import *
from rest_framework import serializers

class ChatSerializer(serializers.ModelSerializer):

    class Meta:
        model = chat
        fields = '__all__'


class VerficationSerializer(serializers.ModelSerializer):

    class Meta:
        model = verification
        fields = '__all__'