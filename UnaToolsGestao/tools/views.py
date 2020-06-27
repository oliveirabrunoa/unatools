from django.shortcuts import render
import json
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
import requests
from django.shortcuts import render
from django.views import View
from .models import Contrato
from .forms import ContratoFormAdmin, ContratoFormAdmin2


def visualizar_contrato(request, param):
    try:
        return FileResponse(open('{0}contrato_{1}'.format(settings.DIRETORIO_CONTRATOS,param), 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        raise Http404()


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


def index(request):
    return render(request, 'Modelo-de-Contrato-PPC-ONLINE html version.html',{'contratante':'Bruno Araújo de Oliveira'})

from django.contrib import messages
class consultar_cliente(View):
    template_name = 'index_base.html'
    form_class = ContratoFormAdmin

    def get(self, request,*args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, { 'form' : form})

    def post(self, request, *args, **kwargs):
        param = request.POST['email']
        if param:
            if Contrato.objects.filter(email=param).first():
                request.session['contrato_id']= str(Contrato.objects.filter(email=param).first().id)
                return HttpResponseRedirect('confirmar_dados')
            else:
                return render(request, self.template_name, {'messages' : 'messages', 'email':param})
        return render(request, self.template_name, { 'form' : self.form_class()})


class confirmar_dados(View):
    template_name = 'dados-contrato.html'
    form_class = ContratoFormAdmin

    def get(self, request,*args, **kwargs):
        contrato=Contrato.objects.filter(id=request.session.get('contrato_id')).first()

        if not contrato:
            return HttpResponseRedirect('consultar_cliente')

        initial_data = {'contratante': contrato.contratante, 'email': contrato.email,
                        'rg': contrato.rg, 'cpf': contrato.cpf,'endereco': contrato.endereco,
                        'cidade_estado': contrato.cidade_estado, 'cep': contrato.cep,
                        'telefone': contrato.telefone, 'data_nascimento': contrato.data_nascimento}

        form = self.form_class(initial= initial_data)
        return render(request, self.template_name, { 'form' : form, 'contratante': contrato.contratante, 'email': contrato.email,
                        'rg': contrato.rg, 'cpf': contrato.cpf,'endereco': contrato.endereco,
                        'cidade_estado': contrato.cidade_estado, 'cep': contrato.cep,
                        'telefone': contrato.telefone, 'data_nascimento': contrato.data_nascimento})


    #PARA REFATORAR - BASE
    def post(self, request, *args, **kwargs):
        print(request.POST)
        initial_data=dict(email=request.POST['email'])
        form = ContratoFormAdmin2(initial_data)
        print(form)
        if form.is_valid():
            print('passou validação')
            return HttpResponseRedirect('confirmar_servico')
        return render(request, 'index.html')


class confirmar_servico(View):
    def get(self, request,*args, **kwargs):
        return render(request, 'dados-servico.html')

    #PARA REFATORAR - BASE
    def post(self, request, *args, **kwargs):
        print(request.POST)
        initial_data=dict(email=request.POST['email'])
        form = ContratoFormAdmin2(initial_data)
        print(form)
        if form.is_valid():
            print('passou validação')
            return HttpResponseRedirect('confirmar_servico')
        return render(request, 'index.html')
