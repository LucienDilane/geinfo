from django.db import models
from Etudiants.models import Etudiant

# Create your models here.

class Group(models.Model):
    nom= models.CharField(max_length=50,verbose_name="nom_group",unique=True)
    description= models.TextField(max_length=300,verbose_name="description")
    createur=models.ForeignKey(Etudiant, on_delete=models.DO_NOTHING,related_name="createur")
    date_creation= models.DateTimeField(auto_now_add=True, editable=False,verbose_name="creationGroup")
    members= models.ManyToManyField(Etudiant, related_name="membres")

    def __str__(self):
        return {"nom":self.nom,
                "description":self.description,
                "datecreate":self.date_creation}


