from django.db import models

from Etudiants.models import Etudiant
from Groupe.models import Group
# Create your models here.

class Message(models.Model):
    sender=models.ForeignKey(Etudiant, on_delete=models.DO_NOTHING,related_name="envoie")
    receiver=models.ForeignKey(Etudiant, on_delete=models.CASCADE, related_name="reception")
    corps=models.TextField(max_length="300", verbose_name="message")
    media=models.CharField(max_length=255,verbose_name="mediaIb")
    date_envoie=models.DateTimeField(auto_now_add=True, editable=False, verbose_name="dateEnvoie")
    lu=models.BooleanField(default=False)

    def __str__(self):
        return {
                "corps": self.corps,
                "media": self.media,
                "datetime": self.date_envoie
                }




class Publication(models.Model):
    auteur=models.ForeignKey(Etudiant,on_delete=models.DO_NOTHING, related_name="auteur" )
    group=models.ForeignKey(Group, on_delete=models.CASCADE,related_name="pubGroup")
    content=models.TextField(max_length=300,verbose_name="contenu")
    media=models.CharField(max_length=255,verbose_name="mediaGroup")
    date_pub=models.DateTimeField(auto_now_add=True, editable=False,verbose_name="datePub")

    def __str__(self):
        return {
            "pub": self.content,
            "media": self.media,
            "datetime":self.date_pub
                }


class Commentaire(models.Model):
    publication=models.ForeignKey(Publication,on_delete=models.CASCADE)
    auteur= models.ForeignKey(Etudiant,on_delete=models.DO_NOTHING)
    content=models.TextField(max_length=300,verbose_name="commentaire")
    media=models.CharField(max_length=255,verbose_name="mediaComm")
    date_com=models.DateTimeField(auto_now_add=True, editable=False, verbose_name="dateComm")

    def __str__(self):
        return {
                "contenu":self.content,
                "media":self.media

                }