from django.shortcuts import render
from .models import Lead
from .moskit import MoskitObj
import json
# Create your views here.


def criar_lead_moskit(lead):
    moskit = MoskitObj()
    result = moskit.criar_contato(lead)
    if result == '200':
        print("cadastro de cliente concluido")


def gerar_contrato(nome_cliente):
    data={}
    template_contrato = "template_ss.html"

    data = {
        "imagem_contrato": "{0}{1}".format(settings.BASE_DIR,"/vendas/templates/images/doisminutos_logo.png"),
        "nome": '{0}'.format(cliente.nome),
        "cpf": '{0}'.format(cliente.cpf),
    }

    url_arquivo= gerador_pdf.run(template_contrato, data, cod_pagamento)
    if url_arquivo:
        return url_arquivo
    return False
