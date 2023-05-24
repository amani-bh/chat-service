from django.urls import path, include

from . import views
from .views import StartCall, EndCall

urlpatterns = [

   path('add_conversation', views.add_conversation),
   path('all_conversations/<int:user_id>', views.all_conversations),
   path('all_messages/<int:id>/<int:idUser>', views.all_messages),
   path('get_conversation/<int:id>', views.get_conversation),
   path('start-call/', StartCall.as_view()),
   path('end-call/', EndCall.as_view()),

]
