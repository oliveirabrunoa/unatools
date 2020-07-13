import io
from django.conf import settings
from django.template.loader import get_template
import string
import random
from weasyprint import HTML, CSS
import os
from django.shortcuts import render
from django.template.loader import render_to_string
from .models import Turma, Tag


class ContratoAPI(object):

    def __init__(self):
        self.base_url = 'http://127.0.0.1:8000'+'/internal_url'
        self.template_name = 'Modelo-de-Contrato-PPC-ONLINE.html'
        self.cod_transacao = self.gerar_codigo()

    def gerar_codigo(self, size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def nome_arquivo(self, contrato):
        return '{0}Contrato_{1}_{2}_{3}.pdf'.format(settings.DIRETORIO_CONTRATOS, str(contrato.contratante).replace(' ', '-'), contrato.cpf, self.cod_transacao)

    def gerar_contrato(self, contrato):
        file_name = self.nome_arquivo(contrato)
        if file_name:
            html_string = render_to_string(self.template_name,self.formatar_dados(contrato))
            html = HTML(string=html_string)
            result = html.write_pdf(file_name, stylesheets=[CSS(string=("@page { size: A3 }"))])
            contrato.url_contrato=file_name
            contrato.save()
            return True
        return False

    def formatar_dados(self,contrato):
        turma = Turma.objects.filter(id=contrato.turma.id).first()
        curso = Tag.objects.filter(id=turma.curso.id).first()
        return {'contratante': contrato.contratante,
                'rg_cliente': contrato.rg,
                'cpf_cliente': contrato.cpf,
                'endereco_cliente': contrato.endereco,
                'cidade_estado_cliente': contrato.cidade_estado,
                'cep_cliente': contrato.cep,
                'telefone_cliente': contrato.telefone,
                'nasc_cliente': contrato.data_nascimento,
                'email_cliente': contrato.email,
                'curso_info': curso.categoria,
                'curso_desc': contrato.extra_bonus if contrato.extra_bonus else '  ',
                'curso_period': turma.periodo,
                'forma_pagamento': contrato.forma_pagamento,
                'cond_pagamento': '{0}{1}'.format(' - ', contrato.condicoes_pagamento),
                'turma_cliente': contrato.turma,
                'consultor_nome': contrato.consultor,
                'cidade_data_contrato': contrato.data_criacao}