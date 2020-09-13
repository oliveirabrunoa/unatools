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
from .choices import ESTADOS, ESTADO_CIVIL
from django.contrib.auth import authenticate, login
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout

class allcontracts(ListView):
    template_name = 'contracts_list.html'
    model = Contrato
    queryset = Contrato.objects.all().filter(assinado=False)

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


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')
    # Redirect to a success page.

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


class confirmar_dados_branco(View):
    template_name = 'dados-contrato-branco.html'
    form_class = ContratoFormAdmin

    def get(self, request,*args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/?next=%s' % request.path)

        return render(request, self.template_name, { 'form' : self.form_class(), 'estadolist': ESTADOS,'estadocivillist': ESTADO_CIVIL})

    def post(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return HttpResponseRedirect('/?next=%s' % request.path)

        if request.POST:
            contrato_novo=Contrato.objects.create(email=request.POST['email'],
                              contratante = request.POST['contratante'],
                              rg=request.POST['rg'], cpf=request.POST['cpf'],
                              endereco=request.POST['endereco'],
                              endereco_cidade=request.POST['cidade'],endereco_uf= request.POST['estado'],
                              cep=request.POST['cep'], telefone=request.POST['telefone'],profissao=request.POST['profissao'],
                              endereco_bairro=request.POST['bairro'], complemento_endereco=request.POST['complemento'],
                              numero_endereco=request.POST['numero'], estado_civil=request.POST['estadocivil'],
                              data_nascimento=data_nasc_format(request.POST['data_nascimento']))
            contrato_novo.save()

            request.session['contrato_id']= str(contrato_novo.id)
            transaction = Transaction.objects.create(contrato=Contrato.objects.filter(id=contrato_novo.id).first())
            return HttpResponseRedirect('escolher_servico')
        return render(request, self.template_name, {})


class confirmar_dados(View):
    template_name = 'dados-contrato.html'
    form_class = ContratoFormAdmin

    def get_sigla_codigo(self,contrato):
        if contrato.endereco_uf:
            for estado in ESTADOS:
                if estado[0]==contrato.endereco_uf:
                    return estado[0]
        return ""

    def get_estado_civil(self,contrato):
        if contrato.estado_civil:
            for estado_civil in ESTADO_CIVIL:
                if estado_civil[0]==contrato.estado_civil:
                    return estado_civil[0]
        return ""

    def get(self, request,*args, **kwargs):

        contrato=Contrato.objects.filter(id=self.kwargs.get('pk')).first()

        if not contrato:
            return HttpResponseRedirect('consultar_cliente')

        request.session['contrato_id']= str(contrato.id)
        transaction = Transaction.objects.create(contrato=contrato)
        return render(request, self.template_name, { 'form' : self.form_class(), 'contratante': contrato.contratante, 'email': contrato.email,
                        'rg': contrato.rg, 'cpf': contrato.cpf,'endereco': contrato.endereco,
                        'cidade': contrato.endereco_cidade,'estadolist': ESTADOS,
                        'bairro': contrato.endereco_bairro, 'cep': contrato.cep,'complemento': contrato.complemento_endereco,
                        'numero': contrato.numero_endereco,'estadocivillist': ESTADO_CIVIL,'profissao': contrato.profissao,
                        'telefone': contrato.telefone, 'data_nascimento': contrato.data_nascimento,
                        'selected_opc_est': self.get_sigla_codigo(contrato),
                        'selected_opc_est_civil': self.get_estado_civil(contrato)})

    def post(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return HttpResponseRedirect('/?next=%s' % request.path)

        contrato=Contrato.objects.filter(id=request.session.get('contrato_id')).first()

        if request.POST:
            contrato_atualizado=Contrato.objects.filter(id=request.session.get('contrato_id')).update(email=contrato.email,
                              contratante = request.POST['contratante'],
                              rg=request.POST['rg'], cpf=request.POST['cpf'],
                              endereco=request.POST['endereco'],
                              endereco_cidade=request.POST['cidade'],endereco_uf= request.POST['estado'],
                              cep=request.POST['cep'], telefone=request.POST['telefone'],profissao=request.POST['profissao'],
                              endereco_bairro=request.POST['bairro'], complemento_endereco=request.POST['complemento'],
                              numero_endereco=request.POST['numero'], estado_civil=request.POST['estadocivil'],
                              data_nascimento=data_nasc_format(request.POST['data_nascimento']))

            return HttpResponseRedirect('escolher_servico')
        return HttpResponseRedirect('consultar_cliente')


class escolher_servico(View):
    template_name = 'escolher-servico.html'
    form_class = ContratoFormAdmin

    def get_cursos(self):
        cursos = Tag.objects.all()
        lista_cursos = [('','Selecione o Curso')]
        # lista_cursos = []
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
        return render(request, self.template_name, { 'form' : self.form_class(), 'email': contrato.email, 'lista_cursos': self.get_cursos()})

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/?next=%s' % request.path)

        contrato=Contrato.objects.filter(id=request.session.get('contrato_id')).first()

        if not contrato:
            return HttpResponseRedirect('consultar_cliente')

        if request.POST:
            contrato_atualizado=Contrato.objects.filter(id=request.session.get('contrato_id')).update(
                              curso=Tag.objects.filter(id=request.POST['cursos']).first(),
                              extra_bonus = request.POST['curso_desc'])

            return HttpResponseRedirect('confirmar_servico')

        return render(request, self.template_name)


class confirmar_servico(View):
    template_name = 'dados-servico.html'
    form_class = ContratoFormAdmin

    def get_turmas_abertas(self, curso_id):
        turmas_ativas = Turma.objects.filter(status_turma=False, curso=curso_id)
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

    def get_consultor_info(self, user):
        nome_consultor = User.objects.filter(username=user).first()
        if nome_consultor:
            return '{0} {1}'.format(nome_consultor.first_name,nome_consultor.last_name)
        return ''

    def split_cond_pag(self,cond_pag):
        s = cond_pag
        n = 87
        linhas = []
        for start in range(0, len(s), n):
            yield s[start:start+n]

    def format_cond_pag(self, cond_pag):
        linhas = []
        for linha in self.split_cond_pag(cond_pag):
            linhas.append(linha)
            linhas.append('\n')
        return ''.join(linhas)

    def get(self, request,*args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/?next=%s' % request.path)

        contrato=Contrato.objects.filter(id=request.session.get('contrato_id')).first()

        if not contrato:
            return HttpResponseRedirect('consultar_cliente')

        data_atual=date.today()
        return render(request, self.template_name, { 'form' : self.form_class(), 'email': contrato.email, 'lista_turmas': self.get_turmas_abertas(contrato.curso.id), 'curso': contrato.curso.nome_curso,
                        'consultor': self.get_consultor_info(request.user), 'datalocalassinatura': '{0}, {1} de {2} de {3}'.format('Salvador/BA', data_atual.day, desc_mes(data_atual.month), data_atual.year)})

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/?next=%s' % request.path)

        contrato=Contrato.objects.filter(id=request.session.get('contrato_id')).first()

        if not contrato:
            return HttpResponseRedirect('consultar_cliente')

        if request.POST:
            contrato_atualizado=Contrato.objects.filter(id=request.session.get('contrato_id')).update(
                              turma=Turma.objects.filter(id=request.POST['turmas']).first(),
                              forma_pagamento =  self.querydict_to_string(request.POST, 'formapagamento'),
                              condicoes_pagamento=self.format_cond_pag(request.POST['condicoespagamento']),
                              consultor='{0}'.format(self.get_consultor_info(request.user)))

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


def testevalidate(request):
    return render(request, "testevalidation.html", {'contrato': Contrato.objects.filter(id=1).first()})
    # Redirect to a success page.
