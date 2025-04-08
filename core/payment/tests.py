from django.test import TestCase
from appointment.models import Patient
from payment.models import Debts, AppointmentCost, PaymentHistory


# Create your tests here.


class PaymentTestCase(TestCase):

    def setUp(self):
        Patient.objects.create(name='John Doe', phone_number='09123456789')
        Debts.objects.create(patient=Patient.objects.get(name='John Doe'))
        AppointmentCost.objects.create(price=5000)

    def test_payment(self):
        p = Patient.objects.create(name='Jane Doe', phone_number='09876543210')
        obj = Debts.objects.get(patient=p)
        self.assertEqual(obj.amount, 0)

# test payment history
class PaymentHistoryTestCase(TestCase):
    def setUp(self):
        Patient.objects.create(name='Jane Doe', phone_number='0987654321')
        PaymentHistory.objects.create(amount=5000,patient=Patient.objects.get(name='Jane Doe'))
    def test_payment_history(self):
        p = Patient.objects.get(name='Jane Doe')
        obj = PaymentHistory.objects.get(patient=p)
        self.assertEqual(obj.amount, 5000)