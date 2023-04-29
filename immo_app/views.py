from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Button
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import FormView, TemplateView, CreateView, DeleteView, ListView, UpdateView
from django.urls import reverse_lazy
from .models import Locataire
from django.shortcuts import render, redirect, get_object_or_404
from .forms import LocataireForm
from django.contrib import messages


class ListeLocatairesView(TemplateView):
    model = Locataire
    template_name = 'accounts/locataire.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['locataires'] = Locataire.objects.all()
        return context

def LocataireCreateView(request):
    if request.method == 'POST':
        form = LocataireForm(request.POST)
        if form.is_valid():
            form.save()

            # Ajouter le nouveau locataire à la liste des locataires
            nouveau_locataire = form.instance
            locataires = Locataire.objects.all()
            context = {'locataires': locataires, 'nouveau_locataire': nouveau_locataire}
            return render(request, 'accounts/locataire.html', context)
    else:
        form = LocataireForm()
    return render(request, 'home/locataire_create.html', {'form': form})

class LocataireUpdateView(UpdateView):

    model = Locataire
    fields = ['nom', 'prenom', 'adresse', 'telephone']
    template_name = 'home/locataire_update.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["submit_text"] = "Modifier le locataire"

class LocataireDeleteView(DeleteView):
    model = Locataire
    template_name = 'home/locataire_delete.html'
    context_object_name = 'locataire'
    success_url = reverse_lazy('immo_app:locataire')

    def get_object(self, queryset=None):
        # Récupère l'objet Locataire à supprimer en utilisant le slug de l'URL
        slug = self.kwargs.get('slug')
        return self.model.objects.get(slug=slug)

    def get_success_url(self):
        return reverse_lazy('immo_app:locataire')

class immo_appHome(ListView):
    model = Locataire
    context_object_name = 'locataire'
    template_name = 'home/immo_app.html'
    queryset = Locataire.objects.all()