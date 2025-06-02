from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q

import json
from django.http import JsonResponse, Http404

from Etudiants.models import Etudiant
from forum.models import Forum
from .models import Message, MessageForum
# Create your views here.


@login_required
def chat_view(request, receiver_id):
    # L'utilisateur connecté est une instance de User (django.contrib.auth.models.User)
    current_user_django = request.user

    # Trouver l'instance Etudiant correspondant à l'utilisateur connecté
    try:
        sender_etudiant = Etudiant.objects.get(id=current_user_django.id)
    except Etudiant.DoesNotExist:
        # Gérer le cas où l'utilisateur connecté n'a pas de profil Etudiant
        # Vous pouvez rediriger, afficher un message d'erreur, etc.
        # Pour l'instant, on va juste lever une erreur pour le débogage.
        # En production, vous pourriez faire un redirect('profil_creation_page')
        raise Http404("Profil Etudiant de l'expéditeur introuvable.")


    receiver_etudiant = get_object_or_404(Etudiant, id=receiver_id)

    if request.method == 'POST':
        content = request.POST.get('message')
        if content:
            # Créer le message en utilisant les instances Etudiant comme expéditeur et destinataire
            Message.objects.create(sender=sender_etudiant, receiver=receiver_etudiant, content=content)
            # Rediriger vers la même page pour afficher le nouveau message (et éviter la soumission multiple)
            return redirect('chat_view', receiver_id=receiver_etudiant.id)

    # Récupérer les messages entre les deux utilisateurs (instances d'Etudiant)
    messages = Message.objects.filter(
        (Q(sender=sender_etudiant, receiver=receiver_etudiant) | Q(sender=receiver_etudiant, receiver=sender_etudiant))
    ).order_by('timestamp') # Important pour avoir les messages dans l'ordre

    context = {
        'sender': sender_etudiant, # Passer l'instance Etudiant de l'expéditeur au template
        'receiver': receiver_etudiant,
        'messages': messages,
    }
    return render(request, 'chat/chat.html', context)

def chat(request,receiver_id):
    if request.method=='POST':
        content=request.POST.get("message")
        recepteur=get_object_or_404(Etudiant,id=receiver_id)
        chat=Message(
            sender=request.user,
            receiver=recepteur,
            content=content
        )

        chat.save()

        return redirect("chat_view",receiver_id=receiver_id)
    else:
        return redirect("chat_view",receiver_id=receiver_id)
