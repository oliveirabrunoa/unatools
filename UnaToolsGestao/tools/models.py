from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from decimal import Decimal


# class Cliente(models.Model):
#     id = models.AutoField(primary_key=True, blank=False, null=False)
#     email = models.CharField(max_length=100,blank=False, null=True)
#     cpf = models.CharField(max_length=14,blank=False, null=True)
#     rg = models.CharField(max_length=11,blank=False, null=True)
#     tipo_cliente = models.IntegerField(default=1,blank=False, null=True)
#     nome = models.CharField(max_length=250,blank=False, null=True)
#     sexo = models.CharField(max_length=1,choices=SEXO,blank=False, null=True)
#     data_nascimento = models.DateField(blank=False, null=True)
#     estado_civil = models.CharField(max_length=1,choices=ESTADO_CIVIL,blank=False, null=True)
#     nacionalidade = models.CharField(max_length=100,blank=False, null=True)
#     ramo_atividade_id = models.IntegerField(blank=True, null=True)
#     ocupacao_id = models.IntegerField(blank=False, null=True)
#     senha = models.CharField(max_length=50,blank=False, null=True)
#
#     def __str__(self):
#         return '{0} - {1}'.format(self.nome, self.cpf)
#
#     class Meta:
#         verbose_name = 'Cliente'
#         verbose_name_plural = 'Clientes'


# class Lead(models.Model):
#     id = models.AutoField(primary_key=True, blank=False, null=False)
#     email = models.CharField(max_length=80,blank=False, null=True)
#     nome = models.CharField(max_length=200,blank=False, null=True)
#     telefone = models.CharField(max_length=20,blank=False, null=True)
#     area_atuacao = models.CharField(max_length=100,blank=False, null=True)
#
#     def __str__(self):
#         return '{0} - {1}'.format(self.nome, self.email)
#
#     class Meta:
#         verbose_name = 'Lead'
#         verbose_name_plural = 'Leads'

class Tag(models.Model):
    id = models.AutoField(primary_key=True, blank=False, null=False)
    categoria = models.CharField(max_length=200,blank=False, null=True)

    def __str__(self):
        return '{0}'.format(self.categoria)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

class Transaction(models.Model):
    id = models.AutoField(primary_key=True, blank=False, null=False)
    data_cadastro = models.DateTimeField(default=timezone.now)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    lead = models.CharField(max_length=200,blank=False, null=True)

    def __str__(self):
        return '{0} - {1}'.format(self.id, self.data_cadastro)

    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'


class UsersCRM(models.Model):
    id = models.AutoField(primary_key=True, blank=False, null=False)
    email = models.CharField(max_length=80,blank=False, null=True)
    nome = models.CharField(max_length=200,blank=False, null=True)


    def __str__(self):
        return '{0} - {1}'.format(self.nome, self.email)

    class Meta:
        verbose_name = 'UsersCRM'
        verbose_name_plural = 'UsersCRM'
