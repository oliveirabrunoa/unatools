from django.conf.urls import url
from . import views
from . import webhooks
from . import gerador_pdf

app_name = 'tools'

urlpatterns = [

    #Weebhooks
    # url(r'^leadlovers_webhook_cadastro_ppc$', webhooks.leadlovers_webhook_cadastro_ppc, name='leadlovers_webhook_cadastro_ppc'),
    url(r'^ac_webhook_cadastro_klick$', webhooks.ac_webhook_cadastro_klick, name='ac_webhook_cadastro_klick'),
    url(r'^ac_webhook_contrato$', webhooks.ac_webhook_contrato, name='ac_webhook_contrato'),
    url(r'^visualizar_contrato/(?P<param>[\w{}.-]{0,200})/$', views.visualizar_contrato, name='visualizar_contrato'),
    url(r'^consultar_cliente$', views.consultar_cliente.as_view(), name='consultar_cliente'),
    url(r'^confirmar_dados$', views.confirmar_dados.as_view(), name='confirmar_dados'),
    url(r'^confirmar_servico$', views.confirmar_servico.as_view(), name='confirmar_servico'),

    # url(r'^meu_teste_pdf$', views.meu_teste_pdf, name='meu_teste_pdf'),
    url(r'^$', views.index, name='index'),
    url(r'^generate_pdf$', gerador_pdf.meu_teste_pdf, name='gerador_pdf'),

]
