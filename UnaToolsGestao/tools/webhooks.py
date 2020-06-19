from .models import Tag, Transaction
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


# @require_POST
# @csrf_exempt
# def leadlovers_webhook_cadastro_ppc(request):
#     body_unicode = request.body.decode('utf-8')
#     params = dict(parse.parse_qsl(parse.urlsplit(body_unicode).path))
#     print(params)
#     if params:
#         lead = Lead()
#         lead.nome = params['Nome']
#         lead.email = params['Email']
#         lead.telefone = params['Telefone']
#         lead.area_atuacao = params['AreadeAtuacao']
#         lead.save()
#
#         tag = Tag.objects.filter(id=params['maquina_origem']).first()
#
#         transaction = Transaction()
#         transaction.lead = lead
#         transaction.tag = tag
#         transaction.save()
#
#         criar_lead_moskit(lead)
#
#     return HttpResponse(status=200)

# parsed = urlparse('http://user:pass@NetLoc:80/path;parameters?query=argument#fragment')

@require_POST
@csrf_exempt
def ac_webhook_cadastro_klick(request):
    body_unicode = request.body.decode('utf-8')
    post_args=request.POST
    if post_args:
        params=dict(post_args.lists())
        nome = params.get("contact[first_name]")[0]
        email = params.get("contact[email]")[0]
        transaction = '{0}'.format("FromAC")
        token = '{0}'.format("c8f64ca00902401400674529e36f9b26")
        status = '{0}'.format("approved")
        url = "https://api.klickmembers.com.br/webhook/advanced/NTAwOQ==/NjM2OA=="
        headers = {'content-type': "application/json"}

        try:
            payload = json.dumps({  "name":'{0}'.format(nome),
                    "email":'{0}'.format(email),
                    "transaction": '{0}'.format(transaction),
                    "token":'{0}'.format(token),
                    "status":'{0}'.format(status)
                })
            response = requests.post(url, data=payload, headers=headers)
            if response.status_code =="200":
                return HttpResponse(status=200)
        except:
            print("Não foi possível criar o usuário")
        return HttpResponse(status=200)
