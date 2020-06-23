from django.conf.urls import url
from . import views
from . import webhooks

app_name = 'tools'

urlpatterns = [

    #Weebhooks
    # url(r'^leadlovers_webhook_cadastro_ppc$', webhooks.leadlovers_webhook_cadastro_ppc, name='leadlovers_webhook_cadastro_ppc'),
    url(r'^ac_webhook_cadastro_klick$', webhooks.ac_webhook_cadastro_klick, name='ac_webhook_cadastro_klick'),
    url(r'^ac_webhook_contrato$', webhooks.ac_webhook_contrato, name='ac_webhook_contrato'),
    url(r'^visualizar_contrato/(?P<param>[\w{}.-]{0,200})/$', views.visualizar_contrato, name='visualizar_contrato'),
    url(r'^consultar_cliente$', views.consultar_cliente.as_view(), name='consultar_cliente'),

    # url(r'^$', views.consultar_cliente, name='consultar_cliente'),
]
