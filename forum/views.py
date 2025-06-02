from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q


from .models import Forum
from chat.models import MessageForum
from Etudiants.models import Etudiant  # Assurez-vous d'importer Etudiant



@login_required
def allforums(request):
    forums=Forum.objects.all()
    return render(request,'forum/allforums.html',{'forums':forums})


# Vue principale du chat pour un forum donné
@login_required
def chat_room_view(request, forum_id):
    # Récupérer l'instance du Forum. C'est correct !
    forum = get_object_or_404(Forum, id=forum_id)
    user = request.user

    # --- Création du message ---
    if request.method == "POST":
        message_content = request.POST.get("message") # Renommé pour plus de clarté

        if message_content:
            MessageForum.objects.create(
                forum=forum,
                auteur=user, # <-- CORRECTION MAJEURE ICI : Passe l'objet 'user' complet, pas 'user.id'
                contenu=message_content # Utilise le nom de variable corrigé
            )
            # Redirection pour éviter la re-soumission du formulaire
            return redirect("chat_room", forum_id=forum.id)

    # --- Récupération des messages ---
    # CORRECTION ICI : 'get' renvoie une erreur si plus d'un objet correspond.
    # Pour récupérer plusieurs messages, utilise 'filter'.
    # De plus, assure-toi que le nom du champ pour le forum dans MessageForum est bien 'forum'.
    # Si c'est 'forum_current', alors garde 'forum_current=forum'.
    # J'assume ici que le champ s'appelle 'forum' dans ton modèle MessageForum.
    messages = MessageForum.objects.filter(forum=forum).order_by('date_envoi')


    # --- Vérification d'appartenance de l'utilisateur au forum (optionnel mais utile) ---
    # Cette ligne est spécifique à comment tu as lié les utilisateurs aux forums.
    # Si `user.forums` est un ManyToManyField qui lie l'utilisateur à plusieurs forums,
    # alors `user.forums.filter(id=forum_id).exists()` est une bonne façon de vérifier.
    # Pour l'envoyer au template, tu peux juste envoyer une booléenne.
    user_forums=[]
    if user.forums.filter(id=forum_id).exists():
       user_forums.append(forum) # Renommé pour clarté

    context = {
        'forum': forum,
        'messages': messages,
        'current_user_id': request.user.id,
        'user_forums': user_forums # Renommé pour clarté
    }
    return render(request, 'chat/chatforum.html', context)
    
