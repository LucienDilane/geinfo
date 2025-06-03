# ressources_app/models.py
from django.db import models
from Etudiants.models import Etudiant

class CategorieRessource(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    extensions_associees = models.CharField(max_length=200, blank=True, help_text="Extensions de fichiers associées (séparées par des virgules, ex: pdf,docx,odt)")


    class Meta:
        verbose_name_plural = "Catégories de Ressources"

    def __str__(self):
        return self.nom
    
    def get_extensions_list(self):
        """Retourne la liste des extensions sous forme de liste Python."""
        return [ext.strip().lower() for ext in self.extensions_associees.split(',') if ext.strip()]

class Ressource(models.Model):
    titre = models.CharField(max_length=255)
    fichier = models.FileField(upload_to='resources/') # Le fichier sera stocké dans media/resources/
    categorie = models.ForeignKey(CategorieRessource, on_delete=models.SET_NULL, null=True, blank=True)
    auteur = models.ForeignKey(Etudiant, on_delete=models.CASCADE, related_name='ressources_partagees')
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_creation']
        verbose_name = "Ressource"
        verbose_name_plural = "Ressources"

    def __str__(self):
        return self.titre

    def get_file_extension(self):
        # Pour déterminer le type de fichier et le mettre dans la bonne catégorie
        name, extension = self.fichier.name.rsplit('.', 1)
        return extension.lower()