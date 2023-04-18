

from django.test import TestCase, Client
from django.urls import reverse
from .models import Locataire

class TestLocataireView(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('create_locataire')
        self.data = {
            'nom': 'Doe',
            'prenom': 'John',
            'adresse': '123 Main St',
            'telephone': '555-1234'
        }

    def test_locataire_page_returns_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_locataire_form_submission_creates_new_object(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 302)
        locataires = Locataire.objects.all()
        self.assertEqual(locataires.count(), 1)
        locataire = locataires.first()
        self.assertEqual(locataire.nom, 'Doe')
        self.assertEqual(locataire.prenom, 'John')
        self.assertEqual(locataire.adresse, '123 Main St')
        self.assertEqual(locataire.telephone, '555-1234')
