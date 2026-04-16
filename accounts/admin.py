from django.contrib import admin
from .models import User, RegisterableEmail

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # Les colonnes qui vont s'afficher dans la liste pour s'y retrouver
    list_display = ('id', 'username', 'email', 'last_login', 'points', 'current_level_label')
    
    # Pour pouvoir cliquer sur le nom et modifier
    list_display_links = ('username',)
    
    # Pour ajouter une barre de recherche dans l'admin
    search_fields = ('username', 'email')
    
    # Champ dérivé accessible en lecture seule dans le formulaire d'édition
    readonly_fields = ('current_level_label',)

    def current_level_label(self, obj):
        return obj.get_level_label()
    current_level_label.short_description = 'Niveau'

admin.site.register(RegisterableEmail)