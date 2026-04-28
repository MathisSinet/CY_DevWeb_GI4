from django.db import models

class ObjetConnecte(models.Model):
    # --- Infos de base ---
    nom = models.CharField(max_length=100)
    id_unique = models.CharField(max_length=50, unique=True, default="ID-TEMP") # Obligatoire dans la consigne
    description = models.TextField(blank=True)
    categorie = models.CharField(max_length=50) # iot, produit, service
    animal_concerne = models.CharField(max_length=50, blank=True) 
    image = models.ImageField(upload_to='objets/', blank=True, null=True) # Pour pas avoir d'image cassée
    
    # --- 1. Attributs Énergie (Consigne) ---
    batterie = models.IntegerField(default=100) # En %
    alimentation = models.CharField(max_length=50, default="Secteur") # Batterie ou Secteur
    conso_energie = models.CharField(max_length=50, default="5W/h")

    # --- 2. Attributs Connectivité (Consigne) ---
    signal_wifi = models.CharField(max_length=50, default="Fort") # Fort, Moyen, Faible
    adresse_ip = models.GenericIPAddressField(null=True, blank=True)

    # --- 3. Attributs Capteurs & Usage (Consigne) ---
    capteurs_liste = models.CharField(max_length=200, default="Température, Humidité")
    valeur_actuelle = models.CharField(max_length=50, blank=True) # Ex: "21°C" ou "1.2L"
    derniere_interaction = models.DateTimeField(auto_now=True) # Se met à jour seul
    
    # --- État du système ---
    est_actif = models.BooleanField(default=True)
    mode = models.CharField(max_length=50, default="Automatique") # Automatique, Manuel, Eco

    def __str__(self):
        return self.nom
    

class Statistiques(models.Model):
    # On lie la stat à l'objet. Si l'objet est supprimé, ses stats aussi (on_delete=CASCADE)
    objet = models.ForeignKey(ObjetConnecte, on_delete=models.CASCADE, related_name='stats')
    jour = models.DateField()
    consommation = models.FloatField()

    def __str__(self):
        return f"{self.objet.id_unique} - {self.jour} : {self.consommation}W"
