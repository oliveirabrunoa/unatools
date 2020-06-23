from django.shortcuts import render
import json
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
import requests
from django.shortcuts import render
from django.views import View
from .forms import ContratoFormAdmin


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
        print('************************************entrou')
        return render(request, self.template_name, { 'form' : form})


    def post(self, request, *args, **kwargs):
        initial_data=dict(nome=request.POST['nome'], email=request.POST['email'],
                           placa=formatar_campo(request.POST['placa']),
                           ddd_telefone_celular=int(formatar_campo(request.POST['telefone'])[:2]),
                           telefone_celular=formatar_campo(request.POST['telefone'])[2:])
        form = ClienteForm(initial_data)
        if form.is_valid():
            post = form.save(commit=False)
            cliente= get_cliente_by_email(post.email)
            cliente.nome = post.nome
            cotacao.save()

            request.session['cotacao_id']= str(cotacao.id)
            return HttpResponseRedirect('escolher_veiculo')
        return render(request, 'erro.html',{'raise_error':'Formulário inicial possui dados inválidos!'})
