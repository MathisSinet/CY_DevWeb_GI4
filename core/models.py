from django.db import models

class CategorieObjet(models.TextChoices):
    IOT = "iot", "IOT"
    PRODUIT = "produit", "Produit"
    SERVICE = "service", "Service"

class TypeAlimentation(models.TextChoices):
    BATTERIE = "batterie", "Batterie"
    SECTEUR = "secteur", "Secteur"

class PuissanceSignal(models.TextChoices):
    EXCELLENT = "excellent", "Excellent"
    FORT = "fort", "Fort"
    MOYEN = "moyen", "Moyen"
    FAIBLE = "faible", "Faible"

class ModeObjet(models.TextChoices):
    AUTO = "auto", "Automatique"
    MAN = "man", "Manuel"
    ECO = "eco", "Eco"

class ObjetConnecte(models.Model):
    # --- Infos de base ---
    nom = models.CharField(max_length=100)
    id_unique = models.CharField(max_length=50, unique=True, default="ID-TEMP")
    description = models.TextField(blank=True)
    categorie = models.CharField(max_length=10, choices=CategorieObjet)
    animal_concerne = models.CharField(max_length=50, blank=True) 
    image = models.ImageField(upload_to='objets/', blank=True, null=True) # Pour pas avoir d'image cassée
    
    # --- 1. Attributs Énergie ---
    batterie = models.IntegerField(default=100) # En %
    alimentation = models.CharField(max_length=10, default=TypeAlimentation.SECTEUR, choices=TypeAlimentation)
    conso_energie = models.FloatField(default="5") # En W/h

    # --- 2. Attributs Connectivité ---
    signal_wifi = models.CharField(max_length=10, default=PuissanceSignal.FORT, choices=PuissanceSignal)
    adresse_ip = models.GenericIPAddressField(null=True, blank=True)

    # --- 3. Attributs Capteurs & Usage ---
    capteurs_liste = models.CharField(max_length=200, default="Température, Humidité")
    valeur_actuelle = models.CharField(max_length=50, blank=True) # Ex: "21°C" ou "1.2L"
    derniere_interaction = models.DateTimeField(auto_now=True) # Se met à jour seul
    
    # --- État du système ---
    est_actif = models.BooleanField(default=True)
    mode = models.CharField(max_length=10, default=ModeObjet.AUTO, choices=ModeObjet)

    def __str__(self):
        return self.nom
    

class Statistiques(models.Model):
    # On lie la stat à l'objet. Si l'objet est supprimé, ses stats aussi (on_delete=CASCADE)
    objet = models.ForeignKey(ObjetConnecte, on_delete=models.CASCADE, related_name='stats')
    jour = models.DateField()
    consommation = models.FloatField()

    def __str__(self):
        return f"{self.objet.id_unique} - {self.jour} : {self.consommation}W"
