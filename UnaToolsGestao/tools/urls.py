from django.conf.urls import url
from . import views
from . import webhooks
from . import gerador_contrato

app_name = 'tools'

urlpatterns = [

    #Weebhooks
    url(r'^ac_webhook_cadastro_klick$', webhooks.ac_webhook_cadastro_klick, name='ac_webhook_cadastro_klick'),
    url(r'^ac_webhook_contrato$', webhooks.ac_webhook_contrato, name='ac_webhook_contrato'),
    #Internal
    url(r'^visualizar_contrato/(?P<param>[\w{}.-]{0,200})/$', views.visualizar_contrato, name='visualizar_contrato'),
    url(r'^consultar_cliente$', views.consultar_cliente.as_view(), name='consultar_cliente'),
    url(r'^confirmar_dados$', views.confirmar_dados.as_view(), name='confirmar_dados'),
    url(r'^confirmar_servico$', views.confirmar_servico.as_view(), name='confirmar_servico'),
    url(r'^generate_pdf$', views.generate_pdf.as_view(), name='generate_pdf'),
    url(r'^concluido$', views.concluido.as_view(), name='concluido'),
    url(r'^visualizar_contrato$', views.visualizar_contrato.as_view(), name='visualizar_contrato'),
    url(r'^download_contrato$', views.download_contrato.as_view(), name='download_contrato'),
    #Index
    # url(r'^$', views.index, name='index'),
    url(r'^entrada$', views.entrada, name='entrada'),
]
