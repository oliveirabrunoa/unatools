import requests
import json
# import string
# import random
# from django.conf import settings
# import base64
# import os.path
# from django.utils import timezone


class MoskitObj(object):

    def __init__(self):#adicionar instancia lead
        self.apikey = 'c8e53183-f582-40be-8b5d-497871dee436'
        self.base_url= 'https://api.moskitcrm.com/v1/'

    def criar_contato(self):
        url = 'https://api.moskitcrm.com/v1/contacts'
        headers = {'content-type': 'application/json', 'apikey': 'c8e53183-f582-40be-8b5d-497871dee436'}

        dados =  {
                    "name":"aaaaaaaaaaaaaaaBruno Teste Intesdsdsdgração",
                    "notes":"Teste",
                    "createdBy":{
                          "id":"24453"
                       },
                    "responsible":{
                          "id":"24453"
                       },
                    "emails":[
                          {
                             "address":"bbbbbbbstring@gmail.com",
                          }
                       ],
                    "phones":
                          {
                             "number":"888888888",
                          }
                    }

        response = requests.post(url, json = json.dumps(dados), headers=headers, verify = False)
        print('Moskit criar_contato',response.text)
        return response.text


    # def check_arquivo(self, path_contrato):
    #     return os.path.exists(path_contrato)
    #
    #
    # def gerar_doc_base64(self, path_contrato):
    #     if self.check_arquivo(path_contrato):
    #         try:
    #             with open(path_contrato, "rb") as pdf_file:
    #                 encoded_string = base64.b64encode(pdf_file.read())
    #                 return encoded_string.decode('utf-8')
    #         except Exception as e:
    #             print(e.message, e.args)
    #     return False
    #
    #
    # def get_prazo_assinatura(self, dias):
    #     now = timezone.now()
    #     prazo = now + timezone.timedelta(days=dias)
    #     prazo_utc = prazo.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]
    #     return '{0}{1}'.format(prazo_utc,'Z')
