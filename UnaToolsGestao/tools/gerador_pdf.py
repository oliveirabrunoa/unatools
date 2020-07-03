import io
import pdfrw
from reportlab.pdfgen import canvas
from django.conf import settings
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import string
import random


def run(template_contrato, data):
    # filename=nome_arquivo(data['contratante'],data['cpf'])
    print('chegou RUN')
    filename='meuteste.pdf'
    pdf = render_to_pdf(template_contrato, data)
    print('PASSOU RENDER')
    save(pdf, filename)
    print('PASSOU SAVE')
    return filename

def nome_arquivo(contratante,cpf):
    return '{0}Contrato_{1}_{2}_{3}.pdf'.format(settings.DIRETORIO_CONTRATOS, contratante, cpf, gerar_codigo())

def gerar_codigo(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def render_to_pdf(template_src, data):
     print('chegou ENTROU RENDER')
     template = get_template(template_src)
     html  = template.render(data)
     result = BytesIO()
     pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1",'ignore')), result)
     print('passou pisa')
     if not pdf.err:
         print('sem erro')
         return HttpResponse(result.getvalue(), content_type='application/pdf')
     return None

def save(pdf, filename):
    try:
        with open(filename, 'wb') as f:
            f.write(pdf.content)
            print('try do save')
    except:
        print('TRY DO ERRO SAVE')
