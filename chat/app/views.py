from django.db.models import Q
from rest_framework.decorators import api_view
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer, UserSerializer
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


@api_view(['POST'])
def add_conversation(request):
    first_user_data = request.data.get('firstUser', {})
    second_user_data = request.data.get('secondUser', {})

    first_user_id = first_user_data.get('id')
    first_user = User.objects.filter(user_id=first_user_id).first()
    if not first_user:
        first_user = User.objects.create(
            user_id=first_user_id,
            user_name=first_user_data.get('first_name') + " " + first_user_data.get('last_name'),
            user_image=first_user_data.get('image_url')
        )

    second_user_id = second_user_data.get('id')
    second_user = User.objects.filter(user_id=second_user_id).first()
    if not second_user:
        second_user = User.objects.create(
            user_id=second_user_id,
            user_name=second_user_data.get('first_name') + " " + second_user_data.get('last_name'),
            user_image=second_user_data.get('image_url')
        )

    conversation = Conversation.objects.create(
        first_user=first_user,
        second_user=second_user,
    )

    conversation_serializer = ConversationSerializer(conversation)
    return Response(conversation_serializer.data, status=status.HTTP_201_CREATED)



@api_view(['GET'])
def all_conversations(request, user_id):
    conversations = Conversation.objects.filter(Q(first_user__user_id=user_id) | Q(second_user__user_id=user_id))
    if conversations:
        conversations_data = []
        for conversation in conversations:
            last_message = conversation.messages.last()  # Retrieve the last message of the conversation
            unread_message_count = conversation.messages.exclude(sender_id=user_id).filter(is_read=False).count()
            if last_message:
                conversation_data = {
                    'id': conversation.id,
                    'first_user': {
                        "user_id": conversation.first_user.user_id,
                        "user_name": conversation.first_user.user_name,
                        "user_image": conversation.first_user.user_image
                    },
                    'second_user': {
                        "user_id": conversation.second_user.user_id,
                        "user_name": conversation.second_user.user_name,
                        "user_image": conversation.second_user.user_image
                    },
                    'last_message': last_message.message,
                    'last_message_sender': last_message.sender.user_id,
                    'last_message_timestamp': last_message.created_at,
                    'unread_message_count': unread_message_count
                }
                conversations_data.append(conversation_data)
        return Response(conversations_data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def all_messages(request, id,idUser):
    try:
        conversation = Conversation.objects.get(id=id)
        messages = conversation.messages.all()
        for message in messages:
            if message.sender_id!=idUser:
                message.is_read=True
                message.save()

        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
    except Conversation.DoesNotExist:
        return Response([])


@api_view(['GET'])
def get_conversation(request, id):
    try:
        conversation = Conversation.objects.get(pk=id)
        serializer = ConversationSerializer(conversation)
        return Response(serializer.data)
    except Conversation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

###################################################################
###################################################################
class StartCallSerializer(serializers.Serializer):
    receiver = serializers.SlugField()
    sender = serializers.SlugField()
    peer_id = serializers.CharField()


class StartCall(APIView):

    def post(self, request, format=None):
        serializer = StartCallSerializer(data=request.data)
        if serializer.is_valid():
            sender_user = User.objects.get(user_id=serializer.validated_data['sender'])
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'chat_%s' % serializer.validated_data['receiver'], {
                    'type': 'new_call',
                    'message': {
                        'data': serializer.validated_data,
                        'display': UserSerializer(sender_user, context={'request': request}).data
                    }
                }
            )
            print('all good')
            return Response({'hello': 'world'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JoinCallSerializer(serializers.Serializer):
    peer_js = serializers.CharField()


class EndCall(APIView):

    def post(self, request, format=None):
        serializer = JoinCallSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'chat_%s' % serializer.validated_data['peer_js'], {  # Use 'peer_js' instead of 'peer_id'
                    'type': 'end_call',
                    'message': {
                        'data': serializer.validated_data,
                    }
                }
            )
            return Response({'hello': 'world'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
