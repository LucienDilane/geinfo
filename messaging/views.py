from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from Etudiants.models import Etudiant
from .models import Message
# Create your views here.



@login_required
def contact_list(request):
    # Si tes contacts sont les autres utilisateurs :
    contacts = Etudiant.objects.exclude(id=request.user.id)
    # Si tu as un modèle Contact :
    # contacts = Contact.objects.filter(user=request.user)
    return render(request, 'messaging/list_etudiants.html', {'contacts': contacts})

@login_required
def chat_view(request, receiver_id):
    receiver = get_object_or_404(Etudiant, id=receiver_id)
    messages = Message.objects.filter(
        (Q(sender=request.user, receiver=receiver) | Q(sender=receiver, receiver=request.user))
    ).order_by('timestamp')
    return render(request, 'messaging/chat.html', {'receiver': receiver, 'messages': messages})