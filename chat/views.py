from django.shortcuts import render, get_object_or_404,redirect
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
    return render(request, 'chat/list_etudiants.html', {'contacts': contacts})

@login_required
def chat_view(request, receiver_id):
    receiver = get_object_or_404(Etudiant, id=receiver_id)
    messages = Message.objects.filter(
        (Q(sender_id=request.user.id, receiver_id=receiver.id) | Q(sender_id=receiver, receiver_id=request.user.id))
    ).order_by('timestamp')
    return render(request, 'chat/chat.html', {'receiver': receiver, 'messages': messages,'sender':request.user})

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
