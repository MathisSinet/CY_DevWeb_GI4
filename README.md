# CY_DevWeb_GI4

Pour installer l'environnement de développement :
- Créer un environnement virtuel python (sur Linux)
- `pip install django`

Pour réinitialiser la base de données et la remplir avec des données de base :
- `python manage.py resetdb`

Pour mettre à jour la base de données si les tables ont été mises à jour :
- `python manage.py migrate`

Pour lancer le serveur en mode développement :
- `python manage.py runserver`