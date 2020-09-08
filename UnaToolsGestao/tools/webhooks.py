from .models import Tag, Transaction, Contrato, Turma
from django.utils import timezone
import datetime
import json
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
import requests
from urllib import parse
from .choices import ESTADOS, ESTADO_CIVIL
from django.core.mail import send_mail
from django.conf import settings

#### Recebimento de Cadastro LL ####
# 1|Formação Completa em Coaching com PNL
# 2|Formação Oratória Magnética com técnicas de Coaching e PNL
# 3|Formação Liderança 4.0 com técnicas de Coaching e PNL
# 4|Formação NevEX  com técnicas de Coaching e PNL


@require_POST
@csrf_exempt
def ac_webhook_cadastro_klick(request):
    body_unicode = request.body.decode('utf-8')
    post_args=request.POST
    print(post_args)
    if post_args:
        params=dict(post_args.lists())
        nome = params.get("contact[first_name]")[0]
        email = params.get("contact[email]")[0]
        turma_tag = params.get("contact[fields][codturmainterno]")[0]

        turma = Turma.objects.all().filter(cod_turma__icontains=turma_tag).first()
        if turma:
            print(turma)
            try:
                payload = json.dumps({  "name":'{0}'.format(nome),
                        "email":'{0}'.format(email),
                        "transaction": '{0}'.format("FromAC"),
                        "token":'{0}'.format(turma.token_klickmembers),
                        "status":'{0}'.format("approved")
                    })
                response = requests.post(turma.url_klickmembers, data=payload, headers={'content-type': "application/json"})

                if response.status_code =="200":
                    send_mail('Acesso criado com sucesso!', 'Por favor, verifique o acesso de: \n  {0} | {1} | {2}'.format(nome,email,turma_tag),
                               settings.EMAIL_HOST_USER, ['brunooliveira@unacoaching.com.br','tauanbaqueiro@unacoaching.com.br'])
                    return HttpResponse(status=200)
            except:
                print("Não foi possível criar o usuário")
                send_mail('Ocorreu um erro ao criar usuário no Portal do Aluno', 'Por favor, verifique o acesso de: \n  {0} | {1} | {2}'.format(nome,email,turma_tag),
                           settings.EMAIL_HOST_USER, ['brunooliveira@unacoaching.com.br','tauanbaqueiro@unacoaching.com.br'])

        return HttpResponse(status=200)


@require_POST
@csrf_exempt
def ac_webhook_cadastro_klick_degust(request):
    body_unicode = request.body.decode('utf-8')
    post_args=request.POST
    print(post_args)
    if post_args:
        params=dict(post_args.lists())
        nome = params.get("contact[first_name]")[0]
        email = params.get("contact[email]")[0]

        turma = Turma.objects.all().filter(cod_turma__icontains="DEGUST01").first()
        if turma:
            print(turma)
            try:
                payload = json.dumps({  "name":'{0}'.format(nome),
                        "email":'{0}'.format(email),
                        "transaction": '{0}'.format("FromAC"),
                        "token":'{0}'.format(turma.token_klickmembers),
                        "status":'{0}'.format("approved")
                    })
                response = requests.post(turma.url_klickmembers, data=payload, headers={'content-type': "application/json"})

                if response.status_code =="200":
                    send_mail('Acesso criado com sucesso!', 'Por favor, verifique o acesso de: \n  {0} | {1} | {2}'.format(nome,email,turma_tag),
                               settings.EMAIL_HOST_USER, ['brunooliveira@unacoaching.com.br','tauanbaqueiro@unacoaching.com.br'])
                    return HttpResponse(status=200)
            except:
                print("Não foi possível criar o usuário")
                send_mail('Ocorreu um erro ao criar usuário no Portal do Aluno', 'Por favor, verifique o acesso de: \n  {0} | {1} | {2}'.format(nome,email,turma_tag),
                           settings.EMAIL_HOST_USER, ['brunooliveira@unacoaching.com.br','tauanbaqueiro@unacoaching.com.br'])

        return HttpResponse(status=200)

    
# @require_POST
# @csrf_exempt
# def ac_webhook_cadastro_klick_ppc(request):
#     body_unicode = request.body.decode('utf-8')
#     post_args=request.POST
#     if post_args:
#         params=dict(post_args.lists())
#         nome = params.get("contact[first_name]")[0]
#         email = params.get("contact[email]")[0]
#         transaction = '{0}'.format("FromAC")
#         token = '{0}'.format("c8f64ca00902401400674529e36f9b26")
#         status = '{0}'.format("approved")
#         url = "https://api.klickmembers.com.br/webhook/advanced/NTAwOQ==/NjM2OA=="
#         headers = {'content-type': "application/json"}
#
#         try:
#             payload = json.dumps({  "name":'{0}'.format(nome),
#                     "email":'{0}'.format(email),
#                     "transaction": '{0}'.format(transaction),
#                     "token":'{0}'.format(token),
#                     "status":'{0}'.format(status)
#                 })
#             response = requests.post(url, data=payload, headers=headers)
#             if response.status_code =="200":
#                 return HttpResponse(status=200)
#         except:
#             print("Não foi possível criar o usuário")
#         return HttpResponse(status=200)


@require_POST
@csrf_exempt
def ac_webhook_contrato(request):
    body_unicode = request.body.decode('utf-8')
    post_args=request.POST
    # print(post_args)
    if post_args:
        params=dict(post_args.lists())
        nome_completo = '{0} {1}'.format(params.get("contact[first_name]")[0], params.get("contact[last_name]")[0])
        email = '{0}'.format(params.get("contact[email]")[0])
        telefone = '{0}'.format(params.get("contact[phone]")[0])
        cpf = '{0}'.format(params.get("contact[fields][cpf]")[0])
        rg = '{0}'.format(params.get("contact[fields][rg]")[0])
        data_nasc = '{0}'.format(params.get("contact[fields][nascimento]")[0])
        endereco_cidade = '{0}'.format(params.get("contact[fields][cidade]")[0])
        endereco_cliente = '{0}'.format(params.get("contact[fields][enderecocompleto]")[0])
        endereco_numero = '{0}'.format(params.get("contact[fields][endereconumero]")[0])
        endereco_bairro = '{0}'.format(params.get("contact[fields][bairro]")[0])
        endereco_estado = '{0}'.format(params.get("contact[fields][estado]")[0])
        cep = '{0}'.format(params.get("contact[fields][cep]")[0])
        profissao = '{0}'.format(params.get("contact[fields][profissao]")[0])
        estado_civil = '{0}'.format(params.get("contact[fields][estado_civil]")[0])

        print(params)

        #Criação de Instância do Tipo Contrato
        contrato = Contrato()
        contrato.contratante = nome_completo
        contrato.rg=rg
        contrato.cpf=cpf
        contrato.endereco= '{0}'.format(endereco_cliente )
        contrato.endereco_bairro = '{0}'.format(endereco_bairro)
        contrato.endereco_cidade = endereco_cidade
        contrato.numero_endereco = endereco_numero
        contrato.profissao = profissao
        contrato.estado_civil = '{0}'.format(get_estado_civil(estado_civil ))
        contrato.endereco_uf = '{0}'.format(get_sigla_codigo(endereco_estado))
        contrato.cep = cep
        contrato.complemento_endereco =' '
        contrato.telefone = telefone
        contrato.data_nascimento=data_nasc_format(data_nasc)
        contrato.email = email
        contrato.save()

    return HttpResponse(status=200)

def get_estado_civil(estado_civil_web):
    if estado_civil_web:
        for ec in ESTADO_CIVIL:
            if ec[1] in estado_civil_web:
                return ec[0]
    return ""

def get_sigla_codigo(endereco_estado):
    if endereco_estado:
        for estado in ESTADOS:
            if estado[1] in endereco_estado:
                return estado[0]
    return ""

def data_nasc_format(data_nasc):
    data_nasc_cliente = data_nasc
    if data_nasc_cliente.find('/')  > 0:
        return datetime.datetime.strptime(data_nasc_cliente,"%d/%m/%Y").strftime("%Y-%m-%d")
    elif data_nasc_cliente.find('-')  > 0:
        return datetime.datetime.strptime(data_nasc_cliente,"%d-%m-%Y").strftime("%Y-%m-%d")
    return None
