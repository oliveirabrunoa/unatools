from django.shortcuts import render
from .moskit import MoskitObj
import json
# Create your views here.


def meutest():
    a = MoskitObj()
    a.criar_contato()

    # print(b)
    # app_json = json.dumps(b)
    # print(b)

meutest()
