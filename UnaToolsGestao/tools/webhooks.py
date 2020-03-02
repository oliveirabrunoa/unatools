from .models import Tag, Transaction, Lead
from django.utils import timezone
import json
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
import requests
from urllib import parse
from .views import criar_lead_moskit

#### Recebimento de Cadastro LL ####
# 1|Formação Completa em Coaching com PNL
# 2|Formação Oratória Magnética com técnicas de Coaching e PNL
# 3|Formação Liderança 4.0 com técnicas de Coaching e PNL
# 4|Formação NevEX  com técnicas de Coaching e PNL


@require_POST
@csrf_exempt
def leadlovers_webhook_cadastro_ppc(request):
    body_unicode = request.body.decode('utf-8')
    params = dict(parse.parse_qsl(parse.urlsplit(body_unicode).path))
    print(params)
    if params:
        lead = Lead()
        lead.nome = params['Nome']
        lead.email = params['Email']
        lead.telefone = params['Telefone']
        lead.area_atuacao = params['AreadeAtuacao']
        lead.save()

        tag = Tag.objects.filter(id=params['maquina_origem']).first()

        transaction = Transaction()
        transaction.lead = lead
        transaction.tag = tag
        transaction.save()

        criar_lead_moskit(lead)

    return HttpResponse(status=200)
