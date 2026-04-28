from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string 
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse

from .models import ObjetConnecte, Statistiques
from accounts.models import User, UserLevel

from django.db.models import Avg

def is_expert(user):
    try:
        return user.current_level == UserLevel.EXPERT
    except:
        return False

# Create your views here.
def test(request):
    return render(request, "test.html")

def index(request):
    return render(request, "index.html")

def concept(request, id_unique):
    # On récupère l'objet grâce à son ID unique (ex: FONT-001)
    objet = get_object_or_404(ObjetConnecte, id_unique=id_unique)
    
    return render(request, "concept.html", {
        'objet': objet,
        'est_expert': is_expert(request.user)
    })

# Nouvelle vue pour gérer les modifications (Boutons Expert)
@login_required
def modifier_objet(request, id_unique):
    if request.method == "POST" and request.user.is_authenticated and is_expert(request.user):
        
        objet = get_object_or_404(ObjetConnecte, id_unique=id_unique)
        
        # Action : Recharger la batterie
        if 'recharger' in request.POST:
            objet.batterie = 100
            
        # Action : Changer le mode (Auto/Manuel/Eco)
        nouveau_mode = request.POST.get('mode')
        if nouveau_mode:
            objet.mode = nouveau_mode
            
        # Action : Switch ON/OFF
        if 'toggle_actif' in request.POST:
            objet.est_actif = not objet.est_actif
            
        objet.save() # On enregistre les modifs dans db.sqlite3
        
    return redirect('concept', id_unique=id_unique)

def search(request):
    objets = ObjetConnecte.objects.all()

    # --- 1. Ta recherche par filtres (déjà faite) ---
    animal = request.GET.get('animal')
    categorie = request.GET.get('type')
    statut = request.GET.get('statut')

    if animal:
        objets = objets.filter(animal_concerne__icontains=animal)
    
    if categorie:
        objets = objets.filter(categorie=categorie)

    if statut:
        est_actif = (statut == 'disponible')
        objets = objets.filter(est_actif=est_actif)

    # --- 2. AJOUT : La recherche par mots-clés (Consigne !) ---
    # Ça permet de taper "Thermostat" ou "température" dans la barre
    
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # On calcule uniquement le HTML des résultats
        html = render_to_string("search.html", {'objets': objets}, request=request)
        # On découpe le HTML pour ne prendre que ce qui est dans le bloc search_results
        # Mais plus simple : on renvoie tout et le JS fera le tri, 
        # ou on utilise une astuce de template.
        return render(request, "search.html", {'objets': objets})
    
    return render(request, "search.html", {'objets': objets})

def information(request):
    actualites = [
        {
            "titre": "Anniversaire Coconimal", 
            "date": "15 Avril 2026", 
            "image": "actus/anniversaire.png", 
            "desc": "AUJOURD'HUI ! Déjà un an que notre pensionnat détente accueille vos compagnons avec amour et technologie !"
        },
        {
            "titre": "Foire Internationale des Animaux", 
            "date": "20 Mai 2026", 
            "image": "actus/foire.png", 
            "desc": "BIENTÔT - Venez nous rencontrer au stand 12 pour découvrir nos nouveaux box connectés !"
        },
        {
            "titre": "Journée Internationale du Chat", 
            "date": "8 Août 2026", 
            "image": "actus/chat.png", 
            "desc": "BIENTÔT - Distribution de friandises bio gratuite pour tous nos pensionnaires félins."
        },
        {
            "titre": "Fête Nationale du Chien", 
            "date": "26 Août 2026", 
            "image": "actus/chien.png", 
            "desc": "BIENTÔT - Grande promenade collective organisée dans le parc de notre magnifique pensionnat."
        },
        {
            "titre": "Repti-Day : La Fête du Reptile", 
            "date": "12 Octobre 2026", 
            "image": "actus/reptile.png", 
            "desc": "BIENTÔT - Atelier découverte : comprendre le cycle UV et la mue de nos amis à écailles."
        },
        {
            "titre": "Nouvel An Chinois - Année du Cheval", 
            "date": "17 Février 2026", 
            "image": "actus/cheval.jpg", 
            "desc": "ÉVÉNEMENT PASSÉ - Une année de dynamisme ! Merci d'être venus nombreux pour le soin des sabots."
        },
    ]
    return render(request, 'information.html', {'actualites': actualites})

@login_required
def stats_view(request, id_unique):
    if not is_expert(request.user):
        return redirect('concept', id_unique=id_unique)
    
    objet = get_object_or_404(ObjetConnecte, id_unique=id_unique)
    
    # On calcule la moyenne des consommations liées à cet objet
    moyenne_data = objet.stats.aggregate(Avg('consommation'))
    # On récupère la valeur ou 0 si c'est vide
    moyenne = moyenne_data['consommation__avg'] or 0
    
    return render(request, 'stats.html', {
        'objet': objet,
        'moyenne': round(moyenne, 1) 
    })

def social(request):
    # Récupérer les paramètres de recherche et filtrage
    search_query = request.GET.get('search', '')
    type_filter = request.GET.get('type', '')
    
    # Base queryset
    users = User.objects.all().order_by('-date_joined')
    
    # Appliquer le filtre de recherche (pseudo insensible à la casse)
    if search_query:
        users = users.filter(username__icontains=search_query)
    
    # Appliquer le filtre par type (niveau d'utilisateur)
    if type_filter:
        # Mapper les valeurs du filtre aux niveaux
        level_mapping = {
            'BEGINNER': UserLevel.BEGINNER,
            'INTERMEDIATE': UserLevel.INTERMEDIATE,
            'ADVANCED': UserLevel.ADVANCED,
            'EXPERT': UserLevel.EXPERT,
        }
        if type_filter in level_mapping:
            # Filtrer par niveau en utilisant les points
            level = level_mapping[type_filter]
            if type_filter == 'BEGINNER':
                users = users.filter(points__lt=100)
            elif type_filter == 'INTERMEDIATE':
                users = users.filter(points__gte=100, points__lt=500)
            elif type_filter == 'ADVANCED':
                users = users.filter(points__gte=500, points__lt=1000)
            elif type_filter == 'EXPERT':
                users = users.filter(points__gte=1000)
    
    # Pagination - 20 utilisateurs par page
    paginator = Paginator(users, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Préparer les types pour le filtre dropdown
    user_types = [
        {'value': 'BEGINNER', 'label': 'Débutant'},
        {'value': 'INTERMEDIATE', 'label': 'Intermédiaire'},
        {'value': 'ADVANCED', 'label': 'Avancé'},
        {'value': 'EXPERT', 'label': 'Expert'},
    ]
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'type_filter': type_filter,
        'user_types': user_types,
    }
    
    return render(request, 'social.html', context)
