from django.urls import path
from . import views

urlpatterns=[
    path('message',views.contact_list,name="etudiants"),
    path('chat/<int:receiver_id>/', views.chat_view, name='chat_view'),
    path('message/<int:receiver_id>/',views.chat,name="message")
]