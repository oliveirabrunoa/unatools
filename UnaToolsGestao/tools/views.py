from django.shortcuts import render
from .models import Lead
from .moskit import MoskitObj
import json
# Create your views here.


def criar_lead_moskit(lead):
    moskit = MoskitObj()
    result = moskit.criar_contato(lead)

    if result == '200':
        print("cadastro efetuado")
