import io
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
import string
import random
from weasyprint import HTML, CSS
import tempfile
import os
import shutil
from .models import Contrato

def gerar_codigo(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class ContratoAPI(object):

    def __init__(self):
        self.base_url = 'http://127.0.0.1:8000'+'/internal_url'
        self.template_name = 'Modelo-de-Contrato-PPC-ONLINE.html'

    def nome_arquivo(self, contrato):
        return '{0}Contrato_{1}_{2}_{3}.pdf'.format(settings.DIRETORIO_CONTRATOS, contrato.contratante, contrato.cpf, gerar_codigo())

    def gerar_temp_file(self, template_name):
        template_src = obter_template(template_name)
        novo=shutil.copy(template_src, '{0}/{1}{2}'.format(settings.DIRETORIO_TEMP,gerar_codigo(),'.html'))
        return novo

    def obter_template(self,template_name):
        for root, dirs, files in os.walk(settings.BASE_DIR+'/tools/templates/'):
            if template_name in files:
                return os.path.join(root, template_name)
            else:
                print('Template não encontrado')

    def gerar_contrato(self):
        contrato= Contrato.objects.all().first()
        src = self.gerar_temp_file(template_name)
        file_name = nome_arquivo(contrato)
    # return render(request, 'Modelo-de-Contrato-PPC-ONLINE.html',{'contratante':'Bruno Araújo de Oliveira'})
        if file_name and src:
            HTML(base_url).write_pdf(file_name, stylesheets=[CSS(string=("@page { size: A3 }"))])

        return HttpResponse("okok")


def internal_url(request):
    return render(request, 'Modelo-de-Contrato-PPC-ONLINE.html',{'contratante':'Bruno Araújo de Oliveira'})
