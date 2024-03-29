
from django import forms
from localflavor.br.forms import BRCPFField, BRZipCodeField
from .models import Contrato


class ContratoFormAdmin(forms.ModelForm):
   cpf = BRCPFField(label="cpf")
   cep = BRZipCodeField(label="cep")

   class Meta:
       model = Contrato
       fields = '__all__'
