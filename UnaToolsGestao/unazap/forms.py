from django import forms
from .models import Cliente


class ClienteFormAdmin(forms.ModelForm):

   class Meta:
       model = Cliente
       fields = '__all__'
