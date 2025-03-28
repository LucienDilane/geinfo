from django.urls import path
from . import views


urlpatterns=[
    path('',views.accueil,name='accueil'),
    path('infos',views.infos,name='propos')
]