from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from decimal import Decimal


class Cliente(models.Model):
    id = models.AutoField(primary_key=True, blank=False, null=False)
    nome_cliente = models.CharField(max_length=50,blank=False, null=True)
    num_whatsapp = models.CharField(max_length=200,blank=False, null=True)

    def __str__(self):
        return '{0} - {1}'.format(self.nome_cliente, self.num_whatsapp)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'


class Consultor(models.Model):
    id = models.AutoField(primary_key=True, blank=False, null=False)
    nome_consultor = models.CharField(max_length=50,blank=False, null=True)
    num_whatsapp_consultor = models.CharField(max_length=200,blank=False, null=True)

    def __str__(self):
        return '{0} - {1}'.format(self.nome_consultor, self.num_whatsapp_consultor)

    class Meta:
        verbose_name = 'Consultor'
        verbose_name_plural = 'Consultores'
