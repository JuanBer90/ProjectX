from django.test import TestCase
from django.contrib.auth.models import User
from django.core import  mail

class Testing(TestCase):

    def setUp(self):

        self.user=User.objects.create_user("Rodrigo","rodrigo@gmail.com","12345")


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

        user1 = User.objects.get(username="Rodrigo")

        self.assertEquals(self.user.email, user1.email)

    def testLogin(self):
        """
        Testeo de Login
        """
        self.assertTrue(self.client.login(username='Rodrigo', password='12345'))

    def tearDown(self):
        self.user.delete()

    def test_enviar_email(self):
        # Envia mensaje.
        mail.send_mail('Saludo al Mundo', 'Hola Mundo',
            'rodrigo@gmail.com', ['marcelo@gmail.com'],
            fail_silently=False)

           # Prueba de que un mensaje ha sido enviado .
        self.assertEqual(len(mail.outbox), 1)
        """
        Verifique que el tema del primer mensaje es correcto.
        """
        self.assertEqual(mail.outbox[0].subject, 'Saludo al Mundo')
