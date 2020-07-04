 # -*- coding: utf-8 -*-
from django.shortcuts import render
import json
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
import requests
from django.shortcuts import render
from django.views import View
from .models import Contrato, Turma, Tag
from .forms import ContratoFormAdmin, ContratoFormAdmin2
from django.utils import timezone
from datetime import date
import datetime
from . import gerador_pdf

from django.template.loader import get_template
from .newpdf import render_to_pdf
from weasyprint import HTML, CSS


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
    return render(request, 'Modelo-de-Contrato-PPC-ONLINE.html',{'contratante':'Bruno Araújo de Oliveira'})

class consultar_cliente(View):
    template_name = 'index_base.html'
    form_class = ContratoFormAdmin

    def get(self, request,*args, **kwargs):
        # if not request.user.is_authenticated:
        #     return HttpResponseRedirect('/login/?next=%s' % request.path)

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
        print(contrato.data_nascimento)
        return render(request, self.template_name, { 'form' : self.form_class(), 'contratante': contrato.contratante, 'email': contrato.email,
                        'rg': contrato.rg, 'cpf': contrato.cpf,'endereco': contrato.endereco,
                        'cidade_estado': contrato.cidade_estado, 'cep': contrato.cep,
                        'telefone': contrato.telefone, 'data_nascimento': contrato.data_nascimento})

    def post(self, request, *args, **kwargs):
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

    def get_cursos(self):
        cursos = Tag.objects.all()
        # lista_cursos = [('','Selecione o Curso')]
        lista_cursos = []
        for c in cursos:
            lista_cursos.append((int(c.id), c))
        return lista_cursos

    def get(self, request,*args, **kwargs):
        contrato=Contrato.objects.filter(id=request.session.get('contrato_id')).first()

        if not contrato:
            return HttpResponseRedirect('consultar_cliente')

        data_atual=date.today()

        return render(request, self.template_name, { 'form' : self.form_class(), 'email': contrato.email, 'lista_turmas': self.get_turmas_abertas(), 'lista_cursos': self.get_cursos(),
                        'consultor': request.user, 'data_local_assinatura': '{0}, {1} de {2} de {3}'.format('Salvador/BA', data_atual.day, desc_mes(data_atual.month), data_atual.year)})

    def post(self, request, *args, **kwargs):
        print(request.POST)
        contrato=Contrato.objects.filter(id=request.session.get('contrato_id')).first()

        if not contrato:
            return HttpResponseRedirect('consultar_cliente')

        if request.POST:
            contrato_atualizado=Contrato.objects.filter(id=request.session.get('contrato_id')).update(
                              turma=Turma.objects.filter(id=request.POST['turmas']).first(),
                              forma_pagamento =  ''.join(list(request.POST['forma-pagamento']))  ,
                              condicoes_pagamento=request.POST['condicoes-pagamento'])

            data = gerar_contrato(contrato_atualizado)
            print(data)
        return render(request, self.template_name)


def gerar_contrato(contrato_id):
    contrato=Contrato.objects.filter(id=contrato_id).first()
    template_contrato = 'template_csbckp.html'
    data={
        'contratante': contrato.contratante,
        'cpf': contrato.cpf
    }
    url_arquivo= gerador_pdf.run(template_contrato, data)
    return data
    # url_arquivo= gerador_pdf.run(template_contrato, data)
    # if url_arquivo:
    #     return url_arquivo
    # return None

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

# def meu_teste_pdf(request):
#
#     template = get_template('template_csbckp.html')
#
#     HTML('http://127.0.0.1:8000').write_pdf('./una-contrato.pdf', stylesheets=[CSS(string=("@page { size: A3 }" ))])
#
#     return HttpResponse("okok")
    # html = template.render(context)
    # pdf = render_to_pdf()
    # if pdf:
    #     response = HttpResponse(pdf, content_type='application/pdf')
    #     filename = "Invoice_%s.pdf" %("12341231")
    #     content = "inline; filename='%s'" %(filename)
    #     download = request.GET.get("download")
    #     if download:
    #         content = "attachment; filename='%s'" %(filename)
    #     response['Content-Disposition'] = content
    #     return response
    # return HttpResponse("Not found")





from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile

def generate_pdf(request):
# render(request, 'Modelo-de-Contrato-PPC-ONLINE html version.html',{'contratante':'Bruno Araújo de Oliveira'})
    # Rendered
    html_string = render_to_string('template_ppc_novo_contrato.html', {'contratante':'Bruno Araújo de Oliveira'})
    html = HTML(string=html_string.replace("\\/", "/").encode().decode('utf-8'))
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=list_people.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'r')
        response.write(output.read())

    return response
