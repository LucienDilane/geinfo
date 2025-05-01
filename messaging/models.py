from django.db import models
from Etudiants.models import Etudiant

# Create your models here.


class Echange(models.Model):
    sender = models.ForeignKey(Etudiant, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(Etudiant, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('timestamp',)

    def __str__(self):
        return f"De {self.sender.nom} à {self.receiver.nom} : {self.content[:20]}"