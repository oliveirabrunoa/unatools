import requests
import json
from .models import UsersMoskit

class MoskitObj(object):

    def __init__(self):#adicionar instancia lead
        self.apikey = 'c8e53183-f582-40be-8b5d-497871dee436'
        self.base_url= 'https://api.moskitcrm.com/v1/'
        self.headers = {'content-type': "application/json",'apikey': "c8e53183-f582-40be-8b5d-497871dee436",'cache-control': "no-cache",}

    def criar_contato(self, lead):
        url = self.base_url + "contacts"
        payload = json.dumps({
                                "name":'{0}'.format(lead.nome),
                                "notes":"Criado by UnaTools",
                                "createdBy":{"id":"24453"}, #Id da Conta Principal - Atualmente Comercial
                                "responsible":{"id": '{0}'.format(self.get_responsible().id_moskit)},
                                "emails":[{"address": '{0}'.format(lead.email),}],
                                "phones": [{"number": "992457753"}],
                            })
        
        response = requests.post(url, data=payload, headers=self.headers)
        return response.status_code

    def get_responsible(self):
        user_moskit_principal = UsersMoskit.objects.filter(principal=True).first()
        return user_moskit_principal
