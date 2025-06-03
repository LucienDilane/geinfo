from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
import Etudiants.views as etudiant
import adminginfo.views as ginfo
import forum.views as groupe
import ressources.views as res

urlpatterns=[
    ## Liens Admin
    path('admin',views.admin,name="admin"),
    path('delete/<int:id>/', views.delete, name='delete'),

    path('update/<int:id>/',views.update,name='update'),
    path('administration',ginfo.login_admin,name='administration'),
    path('interface',views.administration,name='interface'),
    path('api/etudiants/', views.etudiants_list_api, name='etudiants_list_api'),
    path('api/etudiants/<int:id>/', views.etudiant_detail_api, name='etudiant_detail_api'),
    path('api/etudiants/<int:id>/', views.etudiant_detail_update_delete_api, name='etudiant_detail_update_delete_api'),


    # Forum
    path('allforums',groupe.allforums, name='forums'),
    

    ## Liens Etudiants

    path('',views.accueil,name="accueil"),
    path('connexion',views.connexion,name='connexion'),
    path('connect',etudiant.connexion_etudiant,name='connect'),
    path('allstudents',etudiant.contact_list,name="etudiants"),
    path('profil',etudiant.profil,name="profil"),
    path('admin-register',views.register,name='register'),
    path('register',views.enregistrement_etudiant,name='register'),
    path('logout/', auth_views.LogoutView.as_view(next_page='connexion'), name='logout'),
    path('changerphoto',etudiant.modifier_photo_profil,name='changerphoto'),
    path('changepassword',etudiant.changer_mot_de_passe,name='changepassword'),

    ##Ressources
    path('ressources',res.ressources,name="ressources")

    #path('admin', auth_views.LoginView.as_view(template_name='geinfo/login.html'), name='admin'),
    #path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'), # Redirige vers la racine après la déconnexion
]