from core.payment.src.bank import Bank
from core.payment.src.checkout import Checkout


class PaymentService:
    def __init__(self, bank:Bank, checkout:Checkout) -> None:
        self._bank = bank
        self._checkout = checkout
    def pay(self):
        """
        pays checkout with given bank
        """
        pass
