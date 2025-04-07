from abc import ABC, abstractmethod

class Bank(ABC):

    def __init__(self,name) -> None:
        self.name = name

    def get_payment_link(self,amount: float, currency: str):
        pass
