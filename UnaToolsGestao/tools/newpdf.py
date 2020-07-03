from io import StringIO
import six
from django.http import HttpResponse
from django.template.loader import get_template
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
import pdfkit

# from django.conf import settings
# settings.configure()

from weasyprint import HTML, CSS



def render_to_pdf():
    print('entroy')
    context_dict={
        'contratante': "Bruno oli",
        'cpf': "000000"
    }
    HTML('http://weasyprint.org/').write_pdf('/tmp/weasyprint-website.pdf',
        stylesheets=[CSS(string='body { font-family: serif !important }')])


    # template = get_template("template_ppc_novo_contrato.html")
    # # html  = template.render(context_dict)
    # # result = six.StringIO()
    # # pdf = pisa.pisaDocument(six.StringIO(html), result)
    # # /usr/bin/wkhtmltopdf
    # # config = pdfkit.configuration(wkhtmltopdf="/usr/bin/wkhtmltopdf")
    # # pdf = pdfkit.from_file(html, 'MyPDF.pdf', configuration=config)
    # # pdfkit.from_url('http://google.com', 'out.pdf')
    # with open('/home/linuxlite/Documentos/unatools/UnaToolsGestao/tools/templates/template_ppc_novo_contrato.html') as f:
    #     pdfkit.from_file(f, 'out.pdf')
    #     print('FUNFOU')
    #
    # # if pdf:
    # #     print('sem erro')
    # #     return HttpResponse(result.getvalue(), content_type='application/pdf')
    # return 'OKOK'
