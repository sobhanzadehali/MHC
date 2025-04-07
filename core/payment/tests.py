from django.test import TestCase
from appointment.models import Patient
from payment.models import Debts


# Create your tests here.


class PaymentTestCase(TestCase):

    def setUp(self):
       Patient.objects.create(name='John Doe',phone_number='09123456789')
       Debts.objects.create(patient=Patient.objects.get(name='John Doe'))

    def test_payment(self):
        p = Patient.objects.create(name='Jane Doe',phone_number='09876543210')
        obj = Debts.objects.get(patient= p)
        self.assertEqual(obj.amount , 0)
