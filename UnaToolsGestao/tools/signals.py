from django.db.models.signals import post_save
from django.dispatch import receiver

from .gerador_contrato import ContratoAPI

from .models import Contrato, Transaction

@receiver(post_save, sender=Contrato, dispatch_uid="update_contrato")
def update_contrato(sender, instance, **kwargs):
    print('*****************************RECEBIDO!')
    print(instance.contratante)
    if instance.turma and instance.forma_pagamento and instance.consultor and instance.data_criacao:
        ultima_transacao = Transaction.objects.filter(contrato=instance).order_by('-data_cadastro').first()
        if ultima_transacao and ultima_transacao.cod_transacao is None:
            contrato_process=ContratoAPI()
            ultima_transacao.cod_transacao = contrato_process.cod_transacao
            ultima_transacao.save()
            result = contrato_process.gerar_contrato(instance)
