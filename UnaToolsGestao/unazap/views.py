 # -*- coding: utf-8 -*-
 #Python Imports
import json
import os
from datetime import date
import datetime
import requests
import time
#Django Imports
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse,Http404
from django.conf import settings
from django.views import View
from django.utils import timezone
from django.template.loader import get_template
from .models import Cliente
from .forms import ClienteFormAdmin


class testevalidatenew(View):
    template_name = 'lista_contatos.html'
    form_class = ClienteFormAdmin

    def get(self, request,*args, **kwargs):
        return render(request, self.template_name, {'clientes': Cliente.objects.all()})

    def post(self, request, *args, **kwargs):
        clientes= Cliente.objects.all()

        with open('lista_formatada.csv', 'w', newline='') as csvfile:
            fieldnames = ['whatsapp','nome']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for cliente in clientes:
                writer.writerow({'whatsapp': cliente.num_whatsapp, 'nome': cliente.nome_cliente})

        return render(request, self.template_name, {'clientes': Cliente.objects.all()})

#-----------------
def formatar_nomes(nome):
    if nome:
        nome = formatar_simbolos(nome)
        primeiro_nome = nome.split()[0].capitalize()
        return primeiro_nome
    return 'Verificar nome: {0}'.format(nome)

def validar_ddi(numero):
    ctx_number = 0
    if numero.startswith('0'):
        ctx_number = numero[1:]
    else:
        ctx_number = numero


    if ctx_number.startswith('55') and len(ctx_number) == 13:
        return ctx_number[2:]
    else:
        return ctx_number

def validar_nono_digito(numero):
    print('entrou no 9 digitos assim>>>> ', numero)
    if len(numero) >= 10:
        temp_ddd = numero[:2]
        temp_completo = numero[2:]
        print(' DDD e Completo >>>> ', temp_ddd, '  ', temp_completo)
# 71992457753
        if numero.startswith('2') or numero.startswith('1'):
            print('começar com 1 ou 2>>>> ', numero)
            if len(numero) == 11:
                print('tem 11 digitos completos>>>> ', numero)
                return '{0}{1}'.format('55',numero)
            if len(numero) == 10:
                print('tem 10... inclusao do 9>>>> ', numero)
                return '{0}{1}{2}{3}'.format('55',temp_ddd,'9',temp_completo)
        else:
            if len(numero) == 11:
                print('tem 11 digitos, mas ddd n é 1 ou 2>>>> ', numero)
                return '{0}{1}{2}'.format('55',temp_ddd,temp_completo[1:])
            if len(numero) == 10:
                print('tem 10 digitos, mas ddd n é 1 ou 2>>>> ', numero)
                return '{0}{1}{2}'.format('55',temp_ddd,temp_completo)

    else:
        print('else do 9 digito>>>> ', numero)
        return '{0}{1}'.format(numero, ' REVISAO MANUAL - DDD INICIADO EM 1 OU 2')


def formatar_numeros(numero):
    return validar_nono_digito(validar_ddi(formatar_simbolos(numero)))

def formatar_simbolos(item):
    return item.replace('+','').replace('-','').replace(' ','').replace('(','').replace(')','').replace('"','')

import csv
def loadlista():
    index = 0

    with open('Export Lista PH.csv', newline='') as csvfile:
        spamreader = csv.DictReader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            index +=1
            print(formatar_nomes(row['Nome']), formatar_numeros(row['Telefone']))
            cliente = Cliente.objects.create(nome_cliente=formatar_nomes(row['Nome']),num_whatsapp=formatar_numeros(row['Telefone']))
            cliente.save()

            # if index == 15:
            #     break;


# loadlista()
