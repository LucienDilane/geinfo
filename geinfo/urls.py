from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns=[
    path('',views.accueil,name="accueil"),
    path('connexion',views.connexion,name='connexion'),
    path('login',views.connexion_user,name='login'),
    path('infos',views.infos,name='propos'),
    path('profil',views.profil,name="profil"),
    path('admin',views.admin,name='admin'),
    path('register',views.enregistrement_etudiant,name='register'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='connexion'), name='logout'),
    path('changerphoto',views.modifier_photo_profil,name='changerphoto'),
    #path('admin', auth_views.LoginView.as_view(template_name='geinfo/login.html'), name='admin'),
    #path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'), # Redirige vers la racine après la déconnexion
]