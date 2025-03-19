from django import forms
from .models import Debts



class PayDebtsForm(forms.ModelForm):
    amount = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Debts
        fields = ['amount',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['amount'].widget.attrs.update({'readonly': 'readonly'})
