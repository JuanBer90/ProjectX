from django.test import TestCase
from django.contrib.auth.models import User





class Testing(TestCase):

    def setUp(self):
        self.user=User.objects.create_user("juanber", "juanber@juanber.com")

    def test_url(self):
        """
        test url ingresar
        """

        resp=self.client.get('/ingresar/')
        self.assertEqual(resp.status_code, 200)

    def testUsuarioComparacion(self):
        """
        Testing de comparacion de usuario
        """
        user1 = User.objects.get(username="juanber")
        self.assertEquals(self.user.email, user1.email)

    def tearDown(self):
        self.user.delete()
