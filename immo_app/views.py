
from django.views.generic import ListView

from django.shortcuts import render
from .models import Locataire

def home(request):
    return render (request, 'base.html')

def locataire(request):
    return render (request, 'accounts/locataire.html')
def contrat_locataire(request):
    return render (request, 'accounts/contrat_locataire.html')

class immo_appHome(ListView):
    model =Locataire
    context_object_name = 'immo_app'




