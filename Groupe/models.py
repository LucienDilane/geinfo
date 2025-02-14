from django.db import models
from Etudiants.models import Etudiant

# Create your models here.

class Group(models.Model):
    nom= models.CharField(max_length=50,verbose_name="nom_group",unique=True)
    description= models.TextField(max_length=300,verbose_name="description")
    profil=models.CharField(max_length=255, verbose_name="profilGroup")
    createur=models.ForeignKey(Etudiant, on_delete=models.SET_NULL,related_name="createur",null=True,blank=True)
    date_creation= models.DateTimeField(auto_now_add=True, editable=False,verbose_name="creationGroup")
    members= models.ManyToManyField(Etudiant, related_name="membres")

    def __str__(self):
        return {"nom":self.nom,
                "description":self.description,
                "datecreate":self.date_creation}


