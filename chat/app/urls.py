from django.urls import path, include

from . import views
#from .views import MessageListCreateView, ConversationListCreateView

urlpatterns = [

   #path('conversations/', ConversationListCreateView.as_view(), name='conversation-list'),
   #path('conversations/<int:pk>/messages/', MessageListCreateView.as_view(), name='message-list'),
   path('add_conversation', views.add_conversation),
   path('all_conversations/<int:user_id>', views.all_conversations),
   path('all_messages/<int:id>/<int:idUser>', views.all_messages),
   path('get_conversation/<int:id>', views.get_conversation),

]
