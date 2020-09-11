from django.conf.urls import url
from . import views
from . import webhooks
from . import gerador_contrato
from . import validacao_ajax
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy


app_name = 'tools'

urlpatterns = [

    #Weebhooks
    url(r'^ac_webhook_cadastro_klick$', webhooks.ac_webhook_cadastro_klick, name='ac_webhook_cadastro_klick'),
    url(r'^ac_webhook_cadastro_klick_degust$', webhooks.ac_webhook_cadastro_klick_degust, name='ac_webhook_cadastro_klick_degust'),

    url(r'^ac_webhook_contrato$', webhooks.ac_webhook_contrato, name='ac_webhook_contrato'),
    #Internal
    url(r'^visualizar_contrato/(?P<param>[\w{}.-]{0,200})/$', views.visualizar_contrato, name='visualizar_contrato'),
    url(r'^consultar_cliente$', views.consultar_cliente.as_view(), name='consultar_cliente'),
    url(r'^confirmar_dados$', views.confirmar_dados.as_view(), name='confirmar_dados'),
    url(r'^confirmar_dados_branco$', views.confirmar_dados_branco.as_view(), name='confirmar_dados_branco'),
    url(r'^confirmar_servico$', views.confirmar_servico.as_view(), name='confirmar_servico'),
    url(r'^escolher_servico$', views.escolher_servico.as_view(), name='escolher_servico'),
    url(r'^generate_pdf$', views.generate_pdf.as_view(), name='generate_pdf'),
    url(r'^concluido$', views.concluido.as_view(), name='concluido'),
    url(r'^visualizar_contrato$', views.visualizar_contrato.as_view(), name='visualizar_contrato'),
    url(r'^download_contrato$', views.download_contrato.as_view(), name='download_contrato'),
    #Index
    # url(r'^$', views.index, name='index'),
    url(r'^$', views.index.as_view(), name='index'),
    url(r'^login$', views.index.as_view(), name='index'),
    url(r'^logout$', views.logout_view, name='logout'),


    url(r'^contracts/$', login_required(views.allcontracts.as_view()), name='contracts'),
    url(r'^contracts/(?P<pk>\d+)/$', login_required(views.confirmar_dados.as_view()), name='contractdetails'),
    #Validações
    url(r'^testevalidate$', views.testevalidate, name='testevalidate'),
    url(r'^validar_cpf/$', validacao_ajax.validar_cpf, name='validar_cpf'),
    url(r'^validar_cep/$', validacao_ajax.validar_cep, name='validar_cep'),
    url(r'^validar_data_nascimento/$', validacao_ajax.validar_data_nascimento, name='validar_data_nascimento'),
]
