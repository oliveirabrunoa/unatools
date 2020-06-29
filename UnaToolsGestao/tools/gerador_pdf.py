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
    filename=nome_arquivo(data['contratante'],data['cpf'])
    pdf = render_to_pdf(template_contrato, data)
    save(pdf, filename)
    return filename

def nome_arquivo(contratante,cpf):
    return '{0}Contrato_{1}_{2}_{3}.pdf'.format(settings.DIRETORIO_CONTRATOS, contratante, cpf, gerar_codigo())

def gerar_codigo(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def render_to_pdf(template_src, data):
     template = get_template(template_src)
     html  = template.render(data)
     result = BytesIO()
     pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1",'ignore')), result)
     if not pdf.err:
         return HttpResponse(result.getvalue(), content_type='application/pdf')
     return Nonesa

def save(pdf, filename):
    try:
        with open(filename, 'wb') as f:
            f.write(pdf.content)
    except:
        print('erro')
