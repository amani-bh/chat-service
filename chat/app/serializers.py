from rest_framework import serializers
from .models import Message, Conversation

from rest_framework import serializers
from .models import User, Message


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer( read_only=True)
    receiver = UserSerializer( read_only=True)

    class Meta:
        model = Message
        fields = '__all__'


class ConversationSerializer(serializers.ModelSerializer):
    first_user = UserSerializer( read_only=True)
    second_user = UserSerializer( read_only=True)

    class Meta:
        model = Conversation
        fields = '__all__'
