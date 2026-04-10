from django.shortcuts import render
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

def concept(request):
    return render(request,"concept.html")

def boutique(request):
    return render(request,"boutique.html")

def garderie(request):
    return render(request,"garderie.html")

@login_required
def cart(request):
    return render(request,"cart.html")

def search(request):
    objets = ObjetConnecte.objects.all()

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

    return render(request, "search.html", {'objets': objets})






