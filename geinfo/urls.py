from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
import Etudiants.views as etudiant
import adminginfo.views as ginfo
import forum.views as groupe

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

    ##Forums
    # URLs pour les forums (maintenant dans forum/views.py)
    path('api/forums/', groupe.forums_list_api, name='forums_list_api'),
    path('api/forums/<int:pk>/', groupe.forum_detail_update_delete_api, name='forum_detail_update_delete_api'),
    path('api/forums/create/', groupe.create_forum_api, name='create_forum_api'),

    # NOUVELLES URLs pour la gestion des membres de forum
    path('allforums',groupe.allforums, name='forums'),
    #path('api/forums/<int:forum_pk>/members/', groupe.forum_members_api, name='forum_members_api'),
    #path('api/forums/<int:forum_pk>/members/<int:etudiant_pk>/remove/', groupe.forum_remove_member_api,name='forum_remove_member_api'),

    ## Liens Etudiants

    path('',views.accueil,name="accueil"),
    path('connexion',views.connexion,name='connexion'),
    path('connect',etudiant.connexion_etudiant,name='connect'),
    path('infos',views.infos,name='propos'),
    path('allstudents',etudiant.contact_list,name="etudiants"),
    path('profil',etudiant.profil,name="profil"),
    path('admin-register',views.register,name='register'),
    path('register',views.enregistrement_etudiant,name='register'),
    path('logout/', auth_views.LogoutView.as_view(next_page='connexion'), name='logout'),
    path('changerphoto',etudiant.modifier_photo_profil,name='changerphoto'),
    path('changepassword',etudiant.changer_mot_de_passe,name='changepassword'),

    #path('admin', auth_views.LoginView.as_view(template_name='geinfo/login.html'), name='admin'),
    #path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'), # Redirige vers la racine après la déconnexion
]