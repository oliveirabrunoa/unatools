from django.conf.urls import url
from . import views
from . import webhooks

app_name = 'tools'

urlpatterns = [

    #Weebhooks
    url(r'^leadlovers_webhook_cadastro_ppc$', webhooks.leadlovers_webhook_cadastro_ppc, name='leadlovers_webhook_cadastro_ppc'),
]
