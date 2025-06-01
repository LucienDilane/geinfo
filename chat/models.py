from django.db import models
from Etudiants.models import Etudiant
from forum.models import Forum

# Create your models here.


class Message(models.Model):
    sender = models.ForeignKey(Etudiant, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(Etudiant, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('timestamp',)

    def __str__(self):
        return f"De {self.sender.nom} à {self.receiver.nom} : {self.content[:20]}"

class MessageForum(models.Model):
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name='messages')
    auteur = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    contenu = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date_envoi']  # Afficher les messages du plus ancien au plus récent

    def __str__(self):
        return f"Message de {self.auteur.username} dans {self.groupe.nom}"