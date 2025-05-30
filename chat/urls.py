from django.urls import path
from . import views

urlpatterns=[
    path('message',views.contact_list,name="etudiants"),
    path('chat/<int:receiver_id>/', views.chat_view, name='chat_view'),  # L'URL existante pour la vue de chat
]