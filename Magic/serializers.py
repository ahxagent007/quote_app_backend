from .models import *
from rest_framework import serializers

class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = image
        fields = '__all__'

class ChatSerializer(serializers.ModelSerializer):
    #images = ImageSerializer(many=True)
    class Meta:
        model = chat
        fields = '__all__'


class VerficationSerializer(serializers.ModelSerializer):

    class Meta:
        model = verification
        fields = '__all__'

class LastSeenSerializer(serializers.ModelSerializer):

    class Meta:
        model = last_seen
        fields = '__all__'

