from django.contrib import admin
from .models import Tag, Transaction, UsersCRM, Turma, Contrato,ModeloContrato
from .forms import ContratoFormAdmin
from django.utils.html import format_html


# class ContratoFormAdmin(admin.ModelAdmin):
#    form = ContratoFormAdmin
#    list_display = ('get_url_contrato',)
#
#    def get_url_contrato(self, obj):
#         # if int(obj.status_assinatura) != 3:
#         #     return 'Visualização não disponivel'
#
#         return format_html("<a href='{url}' target='_blank'>Visualizar Contrato</a>", url='www.google.com.br')
#     # get_url_contrato.short_description = "Url"

# admin.site.register(Lead)
admin.site.register(Tag)
admin.site.register(Transaction)
admin.site.register(UsersCRM)
admin.site.register(Turma)
admin.site.register(Contrato)
admin.site.register(ModeloContrato)
