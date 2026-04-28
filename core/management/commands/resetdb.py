import random
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth import get_user_model
from accounts.models import RegisterableEmail
from core.models import ObjetConnecte, Statistiques

User = get_user_model()

class Command(BaseCommand):
    help = "Réinitialise la base de données et la remplit avec des données de test"

    def handle(self, *args, **kwargs):
        self.stdout.write("Réinitialisation de la base de données...")

        call_command("flush", "--no-input")

        call_command("migrate")

        self.stdout.write(self.style.SUCCESS("Base de données réinitialisée !"))

        self.stdout.write("Ecriture des données de test")

        # Exemple : créer un admin
        User.objects.create_superuser(
            username="admin",
            email="admin@cocomail.com",
            password="admin",
            first_name = "Admin",
            last_name = "Root",
            birthdate = "1990-01-01",
            points = 2000,
            verified = True
        )
        User.objects.create_user(
            username="alice",
            email="alice@cocomail.com",
            password="alice",
            first_name = "Alice",
            last_name = "Coco",
            birthdate = "2005-02-08",
            points = 300,
            verified = True
        )
        User.objects.create_user(
            username="bob",
            email="bob@cocomail.com",
            password="bob",
            first_name = "Bob",
            last_name = "Coco",
            birthdate = "2000-10-10",
            verified = True
        )

        EMAILS = [
            "admin@cocomail.com",
            "alice@cocomail.com",
            "bob@cocomail.com",
            "cindy@cocomail.com",
            "david@cocomail.com",
            "elena@cocomail.com",
            "fabien@cocomail.com",
        ]
        RegisterableEmail.objects.bulk_create(list(map(lambda email:RegisterableEmail(email=email), EMAILS)))

        self.stdout.write("Création des objets connectés...")
        
        objets_data = [
            {
                "nom": "Fontaine Smart Flow",
                "id_unique": "FONT-001",
                "description": "Fontaine connectée avec filtration triple action. Surveille l'hydratation en temps réel.",
                "categorie": "iot",
                "animal_concerne": "chien_chat",
                "image": "objets/fontaine.png",
                "batterie": 83,
                "alimentation": "Secteur",
                "conso_energie": "5W/h",
                "signal_wifi": "Fort",
                "adresse_ip": "192.168.1.50",
                "capteurs_liste": "Niveau d'eau, Débit de pompe",
                "valeur_actuelle": "2.5 Litres",
                "mode": "Automatique"
            },
            {
                "nom": "Litière Pure-Box",
                "id_unique": "LIT-001",
                "description": "Station d'hygiène auto-nettoyante avec analyse du poids et neutralisation des odeurs.",
                "categorie": "iot",
                "animal_concerne": "chat",
                "image": "objets/litiere.png",
                "batterie": 100,
                "alimentation": "Secteur",
                "conso_energie": "12W/h",
                "signal_wifi": "Stable",
                "adresse_ip": "192.168.1.51",
                "capteurs_liste": "Balance, Capteur de présence",
                "valeur_actuelle": "4.2 kg (Dernière pesée)",
                "mode": "Automatique"
            },
            {
                "nom": "TerraControl Pro",
                "id_unique": "TERRA-001",
                "description": "Centrale de gestion intelligente pour terrariums. Régule UV et chaleur.",
                "categorie": "iot",
                "animal_concerne": "reptile",
                "image": "objets/terrarium.png",
                "batterie": 92,
                "alimentation": "Secteur",
                "conso_energie": "45W/h",
                "signal_wifi": "Moyen",
                "adresse_ip": "192.168.1.60",
                "capteurs_liste": "Sonde UV, Thermostat, Hygromètre",
                "valeur_actuelle": "31°C / 65% Humidité",
                "mode": "Eco"
            },
            {
                "nom": "Clim-IA Multi-Espèce",
                "id_unique": "CLIM-001",
                "description": "Unité de régulation thermique intelligente pour tout l'espace de garde.",
                "categorie": "service",
                "animal_concerne": "tous",
                "image": "objets/climatisation.png",
                "batterie": 100,
                "alimentation": "Secteur",
                "conso_energie": "120W/h",
                "signal_wifi": "Excellent",
                "adresse_ip": "192.168.1.100",
                "capteurs_liste": "Thermomètre ambiant, Capteur de CO2",
                "valeur_actuelle": "22.5°C / Air Pur",
                "mode": "Automatique"
            },
            {
                "nom": "Fontaine Smart Flow - Secteur B",
                "id_unique": "FONT-002",
                "description": "Deuxième unité d'hydratation située dans l'aile Est.",
                "categorie": "iot",
                "animal_concerne": "chien_chat",
                "image": "objets/fontaine.png",
                "batterie": 15,
                "alimentation": "Secteur",
                "conso_energie": "5W/h",
                "signal_wifi": "Faible",
                "adresse_ip": "192.168.1.52",
                "capteurs_liste": "Niveau de cuve, Débit d'eau",
                "valeur_actuelle": "0.4 Litre (Niveau Bas)",
                "mode": "Eco"
            },
            {
                "nom": "Clim-IA - Zone Reptiles",
                "id_unique": "CLIM-002",
                "description": "Unité de régulation thermique dédiée aux terrariums.",
                "categorie": "service",
                "animal_concerne": "reptile",
                "image": "objets/climatisation.png",
                "batterie": 100,
                "alimentation": "Secteur",
                "conso_energie": "90W/h",
                "signal_wifi": "Excellent",
                "adresse_ip": "192.168.1.102",
                "capteurs_liste": "Hygromètre, Thermomètre",
                "valeur_actuelle": "28°C / 70% Humidité",
                "mode": "Automatique"
            },
        ]


        for data in objets_data:
            ObjetConnecte.objects.create(**data)

        self.stdout.write(self.style.SUCCESS("Base de données créée avec 6 objets !"))

        # --- 3. STATISTIQUES SUR 7 JOURS (AJOUTÉ ICI) ---
        self.stdout.write("Génération des statistiques sur 7 jours...")
        tous_les_objets = ObjetConnecte.objects.all()
        aujourdhui = date.today()

        for obj in tous_les_objets:
            # On définit une consommation de base différente selon l'ID pour le réalisme
            if "FONT" in obj.id_unique: base_conso = 120 
            elif "LIT" in obj.id_unique: base_conso = 280
            elif "TERRA" in obj.id_unique: base_conso = 950
            else: base_conso = 2200 # Les Climatisations

            for i in range(7):
                jour_cible = aujourdhui - timedelta(days=i)
                # Variation aléatoire de +/- 15% pour que le graphique ne soit pas plat
                conso_finale = round(base_conso * random.uniform(0.85, 1.15), 1)
                
                Statistiques.objects.create(
                    objet=obj,
                    jour=jour_cible,
                    consommation=conso_finale
                )
        
        self.stdout.write(self.style.SUCCESS("Base de données créée !"))