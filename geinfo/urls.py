from django.urls import path
from . import views

urlpatterns=[
    path('',views.connexion,name='connexion'),
    path('infos',views.infos,name='propos'),
    path('accueil',views.accueil,name="accueil")
]