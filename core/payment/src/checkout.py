#TODO: Implement the checkout class
class Checkout:
    """
    This class represents a checkout process for an appointment.
    """

    def __init__(self, appointment, user):
        """
        Initializes a new instance of the checkout class.

        Args:
            appointment (Appointment): number of The appointments to be checked out.
            user (User): The user who is checking out the appointment.
        """
        self._appointment = appointment
        self._user = user

    def calculate_total(self):
        """Calculates the total cost of the appointments."""
        pass
    def calculate_discount(self):
        """Calculates the discount for the appointments."""
        pass

    def calculate_tax(self):
        """Calculates the tax for the appointments."""
        pass
