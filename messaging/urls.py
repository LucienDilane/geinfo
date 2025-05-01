from django.urls import path
from . import views

urlpatterns=[
    path('message',views.contact_list,name="etudiants"),
]