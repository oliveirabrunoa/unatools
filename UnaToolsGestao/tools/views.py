from django.shortcuts import render
import json
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
import requests
from django.shortcuts import render
from django.views import View
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


class consultar_cliente(View):
    template_name = 'index_base.html'
    form_class = ContratoFormAdmin

    def get(self, request,*args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, { 'form' : form})

    def post(self, request, *args, **kwargs):
        print(request.POST)
        initial_data=dict(email=request.POST['email'])
        form = ContratoFormAdmin2(initial_data)
        print(form)
        if form.is_valid():
            print('passou validação')
        #     post = form.save(commit=False)
        #     cliente= get_cliente_by_email(post.email)
        #     cliente.nome = post.nome
        #     cotacao.save()
        #
        #     request.session['cotacao_id']= str(cotacao.id)
            return HttpResponseRedirect('confirmar_dados')
        return render(request, 'index.html')

class confirmar_dados(View):
    def get(self, request,*args, **kwargs):
        return render(request, 'dados-contrato.html')

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
