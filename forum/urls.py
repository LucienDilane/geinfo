from django.urls import path
from . import views

urlpatterns = [
    # Vue principale du chat pour un forum donné
    path('chat/<int:forum_id>/', views.chat_room_view, name='chat_room'),
    
    # URL pour envoyer un message (via POST AJAX)
    #path('chat/<int:forum_id>', views.send_message_view, name='send_message'),
    
    # URL pour récupérer les messages (via GET AJAX polling)
    #path('chat/<int:forum_id>/messages/', views.get_messages_view, name='get_messages'),
]