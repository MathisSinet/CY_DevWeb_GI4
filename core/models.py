from django.db import models

# Create your models here.

class ObjetConnecte(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    categorie = models.CharField(max_length=50) # iot, produit, service
    animal_concerne = models.CharField(max_length=50, blank=True) 
    prix = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    batterie = models.IntegerField(default=100)
    est_actif = models.BooleanField(default=True)

    def __str__(self):
        return self.nom