from django import forms
from .models import Locataire, Appartement, ContratLocataire, Paiement, EtatLieux,FraisAgence
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms


class LocataireForm(forms.ModelForm):
    class Meta:
        model = Locataire
        fields = ['nom', 'prenom', 'adresse', 'email', 'telephone']
        labels = {
            'nom': 'Nom',
            'prenom': 'Prénom',
            'adresse': 'Adresse',
            'email': 'Email',
            'telephone': 'Téléphone'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.add_input(Submit('submit', 'Enregistrer'))

class AppartementForm(forms.ModelForm):
    class Meta:
        model = Appartement
        fields = '__all__'


class ContratLocataireForm(forms.ModelForm):
    class Meta:
        model = ContratLocataire
        fields = '__all__'


class PaiementForm(forms.ModelForm):
    class Meta:
        model = Paiement
        fields = '__all__'




class Etat_lieuxForm(forms.ModelForm):
    class Meta:
        model = EtatLieux
        fields = '__all__'

class Frais_agenceForm(forms.ModelForm):
    class Meta:
         model = FraisAgence
         fields = '__all__'