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

def nome_arquivo(contrato):
    return '{0}Contrato_{1}_{2}_{3}.pdf'.format(settings.DIRETORIO_CONTRATOS, contrato.contratante, contrato.cpf, gerar_codigo())

def gerar_codigo(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def gerar_temp_file(template_name):
    template_src = obter_template(template_name)
    novo=shutil.copy(template_src, '{0}/{1}{2}'.format(settings.DIRETORIO_TEMP,gerar_codigo(),'.html'))
    return novo

def obter_template(template_name):
    for root, dirs, files in os.walk(settings.BASE_DIR+'/tools/templates/'):
        if template_name in files:
            return os.path.join(root, template_name)
        else:
            print('Template não encontrado')

def meu_teste_pdf(request):
    contrato= Contrato.objects.all().first()
    base_url = 'http://127.0.0.1:8000'
    template_name = 'Modelo-de-Contrato-PPC-ONLINE.html'
    src = gerar_temp_file(template_name)
    file_name = nome_arquivo(contrato)
# return render(request, 'Modelo-de-Contrato-PPC-ONLINE.html',{'contratante':'Bruno Araújo de Oliveira'})
    if file_name and src:
        HTML(base_url).write_pdf(file_name, stylesheets=[CSS(string=("@page { size: A3 }"))])


    return HttpResponse("okok")

def save(pdf, filename):
    try:
        with open(filename, 'wb') as f:
            f.write(pdf.content)
            print('try do save')
    except:
        print('TRY DO ERRO SAVE')
