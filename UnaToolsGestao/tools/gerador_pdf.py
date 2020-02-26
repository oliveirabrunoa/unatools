import io
import pdfrw
from reportlab.pdfgen import canvas
from django.conf import settings
from ..choices import ESTADOS
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import string
import random


def run(template_contrato, data, cod_pagamento):
    filename=nome_arquivo(data['nome'],data['cpf'],cod_pagamento)
    pdf = render_to_pdf(template_contrato, data)
    save(pdf, filename)
    return filename

def nome_arquivo(cliente,cpf,cod_pagamento):
    return '{0}contrato_{1}_{2}_{3}_{4}.pdf'.format(settings.DIRETORIO_CONTRATOS, cliente.replace(' ',''), cpf, cod_pagamento, gerar_codigo())

def gerar_codigo(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def render_to_pdf(template_src, data):
     template = get_template(template_src)
     html  = template.render(data)
     result = BytesIO()
     pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
     if not pdf.err:
         return HttpResponse(result.getvalue(), content_type='application/pdf')
     return Nonesa

def save(pdf, filename):
    try:
        with open(filename, 'wb') as f:
            f.write(pdf.content)
    except:
        print('erro')
