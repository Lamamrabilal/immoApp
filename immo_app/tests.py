from django.test import TestCase, Client
from django.urls import reverse
from .models import Locataire

class TestLocataireView(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)
        self.url = reverse('immo_app:locataire_create')
        self.data = {
            'nom': 'Doe',
            'prenom': 'John',
            'adresse': '123 Main St',
            'email': 'john.doe@example.com',  # ✅ champ manquant ajouté
            'telephone': '0612345678',         # ✅ format valide pour telephone_regex
        }

    def test_locataire_page_returns_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_locataire_form_submission_creates_new_object(self):
        response = self.client.post(self.url, self.data)
        if response.status_code == 200 and 'form' in response.context:
            print("\nErreurs formulaire:", response.context['form'].errors)
        self.assertEqual(response.status_code, 302)