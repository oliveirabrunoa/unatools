from .models import Tag, Transaction, Lead
from django.utils import timezone
import json
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
import requests
from urllib import parse

#### Recebimento de Cadastro LL ####
@require_POST
@csrf_exempt
def leadlovers_webhook_cadastro_ppc(request):
    body_unicode = request.body.decode('utf-8')
    params = dict(parse.parse_qsl(parse.urlsplit(body_unicode).path))
    print(params)
    return HttpResponse(status=200)
    # pagamento_instalacao = ItemPagamentoMoip.objects.filter(codigo_pagamento_moip = body.get('resource').get('payment').get('id'), descricao_item__iexact='Instalação').first()
    # if pagamento_instalacao:
    #     pagamento_instalacao.atualizacao_status = body.get('resource').get('payment').get('updatedAt')
    #     pagamento_instalacao.save()
    #     if body.get('event') == "PAYMENT.AUTHORIZED":
    #         cliente=Cliente.objects.filter(id=pagamento_instalacao.pagamento_id.cliente_id.id).first()
    #         proposta = pagamento_instalacao.pagamento_id.proposta
    #         try:
    #             url_contrato = gerar_contrato(proposta,cliente, pagamento_instalacao.pagamento_id)
    #             contrato = Contrato()
    #             contrato.proposta = pagamento_instalacao.pagamento_id.proposta
    #             contrato.cliente_id = cliente
    #             if url_contrato:
    #                 contrato.url_contrato=url_contrato
    #                 assinatura_digital = assinar_digitalmente(cliente, contrato.url_contrato)
    #                 contrato.clicksign_doc_key = assinatura_digital.get('document').get('key')
    #                 contrato.status_assinatura=1
    #                 print('recebido webhook pagamento criado, status 1!')
    #                 contrato.save()
    #                 pagamento_contrato = pagamento_instalacao.pagamento_id
    #                 pagamento_contrato.contrato = contrato
    #                 pagamento_contrato.save()
    #                 pagamento_instalacao.save()
    #                 return HttpResponse(status=200)
    #         except ValueError:
    #             print ("Não foi possivel gerar o contrato! Aguardando novas tentativas")
    # return HttpResponse(status=302)

#
#
# ####################Metodos para recebimento de Webhooks ClickSign#######################
# ####Documento assinado####
# @require_POST
# @csrf_exempt
# def clicksign_webhook(request):
#     body_unicode = request.body.decode('utf-8')
#     body = json.loads(body_unicode)
#     print('web webhook contrato recebido!  ', body)
#
#     if body.get('event').get('name') == "upload":
#         contrato = Contrato.objects.all().filter(clicksign_doc_key=body.get('document').get('key')).first()
#         if contrato and int(contrato.status_assinatura) == 1:
#             contrato.status_assinatura = 2
#             contrato.save()
#             print('recebido webhook contrato upload ok, status 2!')
#
#     if body.get('event').get('name') == "sign":
#         contrato = Contrato.objects.all().filter(clicksign_doc_key=body.get('document').get('key')).first()
#         if contrato and int(contrato.status_assinatura) < 3:
#             url = body.get('document').get('downloads').get('signed_file_url')
#             path = '{0}contrato_{1}_{2}.pdf'.format(settings.DIRETORIO_CONTRATOS, contrato.cliente_id.cpf, contrato.clicksign_doc_key)
#             arquivo_baixado = False
#             try:
#                 response = requests.get(url)
#                 with open(path, 'wb') as f:
#                     f.write(response.content)
#                     arquivo_baixado=True
#                     print('baixou arquivo')
#             except:
#                 arquivo_baixado=False
#                 print('ocorreu um erro ao baixar o arquivo')
#
#
#             if arquivo_baixado:
#                 contrato.url_contrato=path
#                 contrato.status_assinatura=3
#                 contrato.concluido=body.get('event').get('occurred_at')
#                 contrato.save()
#                 # if contrato.proposta.codigo:
#                 #     result = usebens.formalizar_proposta(contrato.proposta.codigo)
#                 #     print('****Retorno usebens formalizar proposta:::',result)
#                 # print('recebido webhook contrato assinado ok, status 3!')
#                 return HttpResponse(status=200)
#             return HttpResponse(status=500)
#     return HttpResponse(status=200)
