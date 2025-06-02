from django.urls import path
from . import views

urlpatterns=[
    path('chat/<int:receiver_id>/', views.chat_view, name='chat_view'),  # L'URL existante pour la vue de chat

]