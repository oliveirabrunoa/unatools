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
#Aplications Imports
from .models import Contrato, Turma, Tag, Transaction
from .forms import ContratoFormAdmin
from django.contrib.auth import authenticate, login
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView


class allcontracts(ListView):
    template_name = 'contracts_list.html'
    model = Contrato
    queryset = Contrato.objects.all()

class index(View):
    template_name = 'login.html'

    def get(self, request,*args, **kwargs):
        return render(request, self.template_name, {})

    def post(self, request, *args, **kwargs):
        print(request.POST)
        if request.POST:
            email = request.POST['email']
            pwd = request.POST['senha']
            user = authenticate(request, username=email, password=pwd)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('contracts')
            else:
                return render(request, self.template_name, {'messages' : 'messages', 'email':email})
        return render(request, self.template_name, {})

#opcao com consulta de cliente por email
class consultar_cliente(View):
    template_name = 'index_base.html'
    form_class = ContratoFormAdmin

    def get(self, request,*args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/?next=%s' % request.path)

        form = self.form_class()
        return render(request, self.template_name, { 'form' : form})

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/?next=%s' % request.path)

        param = request.POST['email']
        if param:
            if Contrato.objects.filter(email=param).first():
                request.session['contrato_id']= str(Contrato.objects.filter(email=param).first().id)
                transaction = Transaction.objects.create(contrato=Contrato.objects.filter(email=param).first())
                return HttpResponseRedirect('confirmar_dados')
            else:
                return render(request, self.template_name, {'messages' : 'messages', 'email':param})
        return render(request, self.template_name, { 'form' : self.form_class()})

class confirmar_dados(View):
    template_name = 'dados-contrato.html'
    form_class = ContratoFormAdmin

    def get(self, request,*args, **kwargs):

        contrato=Contrato.objects.filter(id=self.kwargs.get('pk')).first()

        if not contrato:
            return HttpResponseRedirect('consultar_cliente')

        request.session['contrato_id']= str(contrato.id)
        return render(request, self.template_name, { 'form' : self.form_class(), 'contratante': contrato.contratante, 'email': contrato.email,
                        'rg': contrato.rg, 'cpf': contrato.cpf,'endereco': contrato.endereco,
                        'cidade_estado': contrato.cidade_estado, 'cep': contrato.cep,
                        'telefone': contrato.telefone, 'data_nascimento': contrato.data_nascimento})

    def post(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return HttpResponseRedirect('/?next=%s' % request.path)

        contrato=Contrato.objects.filter(id=request.session.get('contrato_id')).first()

        if request.POST:
            contrato_atualizado=Contrato.objects.filter(id=request.session.get('contrato_id')).update(email=contrato.email,
                              contratante = request.POST['contratante'],
                              rg=request.POST['rg'], cpf=request.POST['cpf'],
                              endereco=request.POST['endereco'],
                              cidade_estado=request.POST['cidade-estado'],
                              cep=request.POST['cep'], telefone=request.POST['telefone'],
                              data_nascimento=data_nasc_format(request.POST['data_nascimento'])) #VERIFICAR VALIDAÇÃO

            return HttpResponseRedirect('confirmar_servico')
        return HttpResponseRedirect('consultar_cliente')


class confirmar_servico(View):
    template_name = 'dados-servico.html'
    form_class = ContratoFormAdmin

    def get_turmas_abertas(self):
        turmas_ativas = Turma.objects.filter(status_turma=False)
        lista_turmas = [('','Selecione a Turma')]
        for turma in turmas_ativas:
            lista_turmas.append((int(turma.id), turma))
        return lista_turmas

    def querydict_to_string(self, query_dict, filter_name):
        result=' '
        for key in query_dict.keys():
            if key == filter_name:
                v = query_dict.getlist(key)
                if len(v)==1:
                    return v[0]
                result = ', '.join(v)
                return result
        return result

    def get_cursos(self):
        cursos = Tag.objects.all()
        # lista_cursos = [('','Selecione o Curso')]
        lista_cursos = []
        for c in cursos:
            lista_cursos.append((int(c.id), c))
        return lista_cursos

    def get(self, request,*args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/?next=%s' % request.path)

        contrato=Contrato.objects.filter(id=request.session.get('contrato_id')).first()

        if not contrato:
            return HttpResponseRedirect('consultar_cliente')

        data_atual=date.today()
        return render(request, self.template_name, { 'form' : self.form_class(), 'email': contrato.email, 'lista_turmas': self.get_turmas_abertas(), 'lista_cursos': self.get_cursos(),
                        'consultor': request.user, 'data_local_assinatura': '{0}, {1} de {2} de {3}'.format('Salvador/BA', data_atual.day, desc_mes(data_atual.month), data_atual.year)})

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/?next=%s' % request.path)

        contrato=Contrato.objects.filter(id=request.session.get('contrato_id')).first()

        if not contrato:
            return HttpResponseRedirect('consultar_cliente')

        if request.POST:
            contrato_atualizado=Contrato.objects.filter(id=request.session.get('contrato_id')).update(
                              turma=Turma.objects.filter(id=request.POST['turmas']).first(),
                              forma_pagamento =  self.querydict_to_string(request.POST, 'forma-pagamento'),
                              condicoes_pagamento=request.POST['condicoes-pagamento'],
                              consultor='{0}'.format(request.user))

            return HttpResponseRedirect('generate_pdf')

        return render(request, self.template_name)


class generate_pdf(View):
    template_name = 'generate-wait.html'

    def get(self, request,*args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/?next=%s' % request.path)

        contrato=Contrato.objects.filter(id=request.session.get('contrato_id')).first()

        if not contrato:
            return HttpResponseRedirect('consultar_cliente')

        data_atual=date.today()
        contrato.data_criacao = '{0}, {1} de {2} de {3}'.format('Salvador/BA', data_atual.day, desc_mes(data_atual.month), data_atual.year)
        contrato.save()
        return render(request, self.template_name)

class concluido(View):
    template_name = 'generated.html'

    def get(self, request,*args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/?next=%s' % request.path)

        return render(request, self.template_name)


class visualizar_contrato(View):

    def get(self, request,*args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/?next=%s' % request.path)

        contrato=Contrato.objects.filter(id=request.session.get('contrato_id')).first()

        if not contrato:
            return HttpResponseRedirect('consultar_cliente')

        file_path = contrato.url_contrato
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/pdf")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response
        raise Http404


class download_contrato(View):

    def get(self, request,*args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/?next=%s' % request.path)

        contrato=Contrato.objects.filter(id=request.session.get('contrato_id')).first()

        if not contrato:
            return HttpResponseRedirect('consultar_cliente')

        file_path = contrato.url_contrato
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/force-download")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response
        raise Http404


def desc_mes(mes_atual):
    meses = [(1,'Janeiro'),(2,'Fevereiro'),(3,'Março'),(4,'Abril'),(5,'Maio'),(6,'Junho'),(7,'Julho'),(8,'Agosto'),(9,'Setembro'),(10,'Outubro'),(11,'Novembro'),(12,'Dezembro')]
    for mes in meses:
        if mes[0]==mes_atual:
            return mes[1]

def data_nasc_format(data_nasc):
    data_nasc_cliente = data_nasc
    if data_nasc_cliente.find('/')  > 0:
        return datetime.datetime.strptime(data_nasc_cliente,"%d/%m/%Y").strftime("%Y-%m-%d")
    elif data_nasc_cliente.find('-')  > 0:
        return datetime.datetime.strptime(data_nasc_cliente,"%d-%m-%Y").strftime("%Y-%m-%d")
    return None
