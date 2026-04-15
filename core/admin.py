from django.contrib import admin
from .models import ObjetConnecte

@admin.register(ObjetConnecte)
class ObjetConnecteAdmin(admin.ModelAdmin):
    # Les colonnes qui vont s'afficher dans la liste pour s'y retrouver
    list_display = ('nom', 'id_unique', 'categorie', 'animal_concerne', 'est_actif')
    
    # Pour pouvoir cliquer sur le nom et modifier
    list_display_links = ('nom',)
    
    # Pour ajouter une barre de recherche dans l'admin
    search_fields = ('nom', 'id_unique')