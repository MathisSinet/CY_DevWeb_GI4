from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import ObjetConnecte

# Create your views here.
def test(request):
    return render(request, "test.html")

def index(request):
    return render(request, "index.html")

def login(request):
    return render(request,"login.html")

def signup(request):
    return render(request,"signup.html")

def concept(request, id_unique):
    # On récupère l'objet grâce à son ID unique (ex: FONT-001)
    objet = get_object_or_404(ObjetConnecte, id_unique=id_unique)
    
    # On définit qui est expert : ici, n'importe quel utilisateur connecté
    # (Tu pourras affiner plus tard avec les groupes si besoin)
    est_expert = request.user.is_authenticated 
    
    return render(request, "concept.html", {
        'objet': objet,
        'est_expert': est_expert
    })

# Nouvelle vue pour gérer les modifications (Boutons Expert)
def modifier_objet(request, id_unique):
    if request.method == "POST" and request.user.is_authenticated:
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

def garderie(request):
    return render(request,"garderie.html")

@login_required
def cart(request):
    return render(request,"cart.html")

def search(request):
    objets = ObjetConnecte.objects.all()

    # --- 1. Ta recherche par filtres (déjà faite) ---
    animal = request.GET.get('animal')
    categorie = request.GET.get('type')
    statut = request.GET.get('statut')

    if animal:
        objets = objets.filter(animal_concerne=animal)
    
    if categorie:
        objets = objets.filter(categorie=categorie)

    if statut:
        est_actif = (statut == 'disponible')
        objets = objets.filter(est_actif=est_actif)

    # --- 2. AJOUT : La recherche par mots-clés (Consigne !) ---
    # Ça permet de taper "Thermostat" ou "température" dans la barre
    q = request.GET.get('q')
    if q:
        # On cherche dans le nom OU dans la description
        objets = objets.filter(nom__icontains=q) | objets.filter(description__icontains=q)

    return render(request, "search.html", {'objets': objets})






