



from django.contrib.auth.decorators import login_required
from django.http import request, HttpResponse
from django.template.loader import get_template
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import FormView, TemplateView, CreateView, DeleteView, ListView, UpdateView, DetailView
from django.urls import reverse_lazy
from reportlab.lib.pagesizes import A4


from .models import Locataire, Appartement, ContratLocataire, EtatLieux, Paiement
from django.shortcuts import render, redirect, get_object_or_404
from .forms import LocataireForm, AppartementForm, ContratLocataireForm, PaiementForm, Etat_lieuxForm
from reportlab.pdfgen import canvas
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


class immo_appHome(TemplateView):

    template_name = 'home/immo_app.html'

## Locataire

class ListeLocatairesView(ListView):
    model = Locataire
    template_name = 'accounts/locataire.html'
    paginate_by =3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        locataires = self.get_queryset()
        paginator = Paginator(locataires, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['locataires'] = page_obj
        context['paginator'] = paginator
        context['is_paginated'] = page_obj.has_other_pages()
        return context

class LocataireCreateView(CreateView):

    model = Locataire
    form_class = LocataireForm
    template_name = 'home/locataire_create.html'

    def form_valid(self, form):
        super().form_valid(form)
        nouveau_locataire= form.instance
        locataires = Locataire.objects.all()
        context = {'locataires': locataires, 'nouveau_locataire': nouveau_locataire}
        return render(self.request, 'accounts/locataire.html', context)


class LocataireUpdateView(UpdateView):
    model = Locataire
    form_class = LocataireForm
    template_name = 'home/locataire_update.html'
    success_url = reverse_lazy('immo_app:locataire')

    def get_object(self, queryset=None):
        # Récupère l'objet à modifier
        return get_object_or_404(Locataire, pk=self.kwargs['pk'])

class LocataireDeleteView(DeleteView):
    model = Locataire
    template_name = 'home/locataire_delete.html'
    context_object_name = 'locataire'
    success_url = reverse_lazy('immo_app:locataire')




# Appartement
class AppartementListView(ListView):
    model = Appartement
    template_name = 'accounts/appartement.html'
    paginate_by =2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        appartements = self.get_queryset()
        paginator = Paginator(appartements, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['appartements'] = page_obj
        context['paginator'] = paginator
        context['is_paginated'] = page_obj.has_other_pages()
        return context

class AppartementCreateView(CreateView):

    model = Appartement
    form_class = AppartementForm
    template_name = 'home/appartement_create.html'

    def form_valid(self, form):
        super().form_valid(form)
        nouveau_appartement = form.instance
        appartements = Appartement.objects.all()
        context = {'appartements': appartements, 'nouveau_appartement': nouveau_appartement}
        return render(self.request, 'accounts/appartement.html', context)


class AppartementUpdateView(UpdateView):

    model = Appartement
    form_class = AppartementForm
    template_name = 'home/appartement_update.html'
    success_url = reverse_lazy('immo_app:appartement')

    def get_object(self, queryset=None):
        # Récupère l'objet à modifier
        return get_object_or_404(Appartement, pk=self.kwargs['pk'])

class AppartementDetailView(DetailView):

    model = Appartement
    template_name = 'accounts/appartement.html'
    fields = '__all__'
    context_object_name = 'appartement'

class AppartementDeleteView(DeleteView):

        model = Appartement
        template_name = 'home/appartement_delete.html'
        success_url = reverse_lazy('immo_app:appartement')
        context_object_name = 'appartement'



class ContratLocataireListView(ListView):

    model = ContratLocataire
    template_name = 'accounts/contrat_locataire.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contrat_locataire = self.get_queryset()
        paginator = Paginator(contrat_locataire, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['contrat_locataire'] = page_obj
        context['paginator'] = paginator
        context['is_paginated'] = page_obj.has_other_pages()
        return context

class ContratLocataireCreateView(CreateView):

    model = ContratLocataire
    form_class = ContratLocataireForm
    template_name = 'home/contrat_locataire_create.html'

    def form_valid(self, form):
        super().form_valid(form)
        nouveau_contrat_locataire = form.instance
        contrat_locataire = ContratLocataire.objects.all()

        context = {'contrat_locataire':contrat_locataire, 'nouveau_contrat_locataire': nouveau_contrat_locataire}
        return render(self.request, 'accounts/contrat_locataire.html', context)


class ContratLocataireUpdateView(UpdateView):

    model = ContratLocataire
    form_class = ContratLocataireForm
    template_name = 'home/contrat_locataire_update.html'
    success_url = reverse_lazy('immo_app:contrat_locataire')

    def get_object(self, queryset=None):
        # Récupère l'objet à modifier
        return get_object_or_404(ContratLocataire, pk=self.kwargs['pk'])


class ContratLocataireDeleteView(DeleteView):

    model = ContratLocataire
    context_object_name = 'contrat_locataire'
    template_name = 'home/contrat_locataire_delete.html'
    success_url = reverse_lazy('immo_app:contrat_locataire')

class Etat_lieuxListView(ListView):
    model = EtatLieux
    template_name = 'accounts/etat_lieux.html'
    paginate_by = 2

    def get_queryset(self):
        # Vérifiez si `super().get_queryset()` est utilisé correctement
        return super().get_queryset().order_by('id')

    def get_context_data(self, **kwargs):
        # Assurez-vous que vous n'appelez pas `get_queryset()` directement ici
        context = super().get_context_data(**kwargs)
        context['is_paginated'] = context['page_obj'].has_other_pages()
        return context


class EtatLieuxCreateView(CreateView):

    model = EtatLieux
    form_class = Etat_lieuxForm
    template_name = 'home/etat_lieux_create.html'

    def form_valid(self, form):
        super().form_valid(form)
        nouveau_etat_lieux = form.instance
        etat_lieux = EtatLieux.objects.all()
        context = {'etat_lieux': etat_lieux, 'nouveau_etat_lieux': nouveau_etat_lieux}
        return render(self.request, 'accounts/etat_lieux.html', context)


class EtatLieuxUpdateView(UpdateView):

    model = EtatLieux
    form_class = Etat_lieuxForm
    template_name = 'home/etat_lieux_update.html'
    success_url = reverse_lazy('immo_app:etat_lieux')

    def get_object(self, queryset=None):
        # Récupère l'objet à modifier
        return get_object_or_404(EtatLieux, pk=self.kwargs['pk'])



class EtatDeleteLieuxView(DeleteView):

    model = EtatLieux
    template_name = 'home/etat_lieux_delete.html'
    success_url = reverse_lazy('immo_app:etat_lieux')


class PaiementListView(ListView):
    model = Paiement
    template_name = 'accounts/paiement.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paiements = self.get_queryset()
        paginator = Paginator(paiements, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['paiements'] = page_obj
        context['paginator'] = paginator
        context['is_paginated'] = page_obj.has_other_pages()
        return context

class PaiementCreateView(CreateView):

    model = Paiement
    form_class = PaiementForm
    template_name = 'home/paiement_create.html'

    def form_valid(self, form):
        super().form_valid(form)
        nouveau_paiement = form.instance
        paiements = Paiement.objects.all()
        context = {'paiements': paiements, 'nouveau_paiement': nouveau_paiement}
        return render(self.request, 'accounts/paiement.html', context)



class PaiementUpdateView(UpdateView):

    model = Paiement
    form_class = PaiementForm
    template_name = 'home/paiement_update.html'
    success_url = reverse_lazy('immo_app:paiement')

    def get_object(self, queryset=None):
        # Récupère l'objet à modifier
        return get_object_or_404(Paiement, pk=self.kwargs['pk'])



class PaiementDeleteView(DeleteView):

        model = Paiement
        template_name = 'home/paiement_delete.html'
        success_url = reverse_lazy('immo_app:paiement')
        context_object_name = 'paiement'

class QuittanceLoyerView(View):
    model = Paiement
    template_name = 'home/quittance.html'
    context_object_name = 'quittance'

    def get(self, request, pk):
        try:
            paiement = Paiement.objects.get(pk=pk, montant_paiement__gt=0)
        except Paiement.DoesNotExist:
            # If the payment does not exist or has a zero amount, return a 404 error
            return HttpResponse(status=404)
        else:
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="quittance_loyer_{paiement.locataire}-{paiement.date_paiement}.pdf"'

            p = canvas.Canvas(response, pagesize=A4)

            # Add logo and header
            p.setFont("Helvetica-Bold", 20)
            p.drawString(80, 280, "Quittance de Loyer")

            # Add details of paiement
            p.setFont("Helvetica-Bold", 14)
            p.drawString(80, 220, f"Locataire: {paiement.locataire}")
            p.drawString(80, 200, f"Appartement: {paiement.appartement}")
            p.drawString(80, 180, f"Montant payé: {paiement.montant_paiement}")
            p.drawString(80, 160, f"Date de paiement: {paiement.date_paiement}")
            p.drawString(80, 140, f"Origine de paiement: {paiement.origine_paiement}")

            # Add footer and signature
            p.setFont("Helvetica", 10)
            p.drawString(80, 40, ("Merci pour votre paiement."))
            p.drawString(80, 20, ("Signature"))

            p.showPage()
            p.save()

            return response
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename="quittance_loyer.pdf")

@method_decorator(login_required, name='dispatch')
class QuittanceDetailView(DetailView):
    model = Paiement
    template_name = 'quittance_detail.html'
    context_object_name = 'paiement'






