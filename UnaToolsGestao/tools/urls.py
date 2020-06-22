from django.conf.urls import url
from . import views
from . import webhooks

app_name = 'tools'

urlpatterns = [

    #Weebhooks
    # url(r'^leadlovers_webhook_cadastro_ppc$', webhooks.leadlovers_webhook_cadastro_ppc, name='leadlovers_webhook_cadastro_ppc'),
    url(r'^ac_webhook_cadastro_klick$', webhooks.ac_webhook_cadastro_klick, name='ac_webhook_cadastro_klick'),
    url(r'^ac_webhook_contrato$', webhooks.ac_webhook_contrato, name='ac_webhook_contrato'),

    url(r'^$', views.index, name='index'),
]
