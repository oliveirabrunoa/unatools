import requests
import json

class MoskitObj(object):

    def __init__(self):#adicionar instancia lead
        self.apikey = 'c8e53183-f582-40be-8b5d-497871dee436'
        self.base_url= 'https://api.moskitcrm.com/v1/'
        self.headers = {'content-type': "application/json",'apikey': "c8e53183-f582-40be-8b5d-497871dee436",'cache-control': "no-cache",}

    def criar_contato(self):
        url = self.base_url + "contacts"
        payload = json.dumps({
                                "name":"aaaaaaaaaaaaaaaBruno Teste Intesdsdsdgração",
                                "notes":"Teste",
                                "createdBy":{"id":"24453"},
                                "responsible":{"id":"24453"},
                                "emails":[{"address":"bbbbbbbstring@gmail.com",}],
                                "phones": {"number":"888888888",}
                            })

        response = requests.post(url, data=payload, headers=self.headers)
        print(response.text)
