from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Conversation, Message, User


class ConversationTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create(user_id=1, user_name='User1', user_image='http://example.com/user1.jpg')
        self.user2 = User.objects.create(user_id=2, user_name='User2', user_image='http://example.com/user2.jpg')
        self.conversation = Conversation.objects.create(first_user=self.user1, second_user=self.user2)
        self.message1 = Message.objects.create(conversation=self.conversation, sender=self.user1, message='Hello')
        self.message2 = Message.objects.create(conversation=self.conversation, sender=self.user2, message='Hi')

    def test_add_conversation(self):
        url = reverse('add_conversation')
        data = {
            'firstUser': {
                'id': 6,
                'first_name': 'first user',
                'last_name': 'first user',
                'image_url': 'https://example.com/image.jpg'
            },
            'secondUser': {
                'id': 7,
                'first_name': 'second user',
                'last_name': 'second user',
                'image_url': 'https://example.com/image.jpg'
            }
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_all_conversations(self):
        user_id = self.user1.user_id
        url = reverse('all_conversations', args=[user_id])

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_all_messages(self):
        conversation_id = self.conversation.id
        user_id = self.user1.id
        url = reverse('all_messages', args=[conversation_id, user_id])

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_conversation(self):
        conversation_id = self.conversation.id
        url = reverse('get_conversation', args=[conversation_id])

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
