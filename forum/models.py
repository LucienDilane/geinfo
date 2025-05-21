from django.db import models



# Create your models here.
class Forum(models.Model):
    nom = models.CharField(max_length=15, unique=True, verbose_name="nom_forum")
    description = models.TextField(max_length=200, verbose_name="description_forum")
    profil = models.CharField(max_length=100, verbose_name="profil_forum")
    createur = models.ForeignKey(
        'Etudiants.Etudiant',
        on_delete=models.SET_NULL,
        related_name="forums_crees",
        null=True,
        blank=True,
        verbose_name="createur_forum"
    )

    class Meta:
        verbose_name = "Forum"
        verbose_name_plural = "Forums"
        ordering = ['nom']

    def __str__(self):
        creator_name = self.createur.get_full_name() if self.createur else "Inconnu"
        return f"{self.nom} (Créé par: {creator_name})"