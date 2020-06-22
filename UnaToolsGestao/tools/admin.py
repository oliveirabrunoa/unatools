from django.contrib import admin
from .models import Tag, Transaction, UsersCRM, Turma, Contrato
from .forms import ContratoFormAdmin


class ContratoFormAdmin(admin.ModelAdmin):
   form = ContratoFormAdmin

# admin.site.register(Lead)
admin.site.register(Tag)
admin.site.register(Transaction)
admin.site.register(UsersCRM)
admin.site.register(Turma)
admin.site.register(Contrato,ContratoFormAdmin)
