from django.shortcuts import render

# Create your views here.
def test(request):
    return render(request, "test.html")

def index(request):
    return render(request, "index.html")

def login(request):
    return render(request,"login.html")

def concept(request):
    return render(request,"concept.html")

def boutique(request):
    return render(request,"boutique.html")

def garderie(request):
    return render(request,"garderie.html")

def cart(request):
    return render(request,"cart.html")

def search(request):
    return render(request,"search.html")








