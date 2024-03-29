from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from decimal import Decimal
from .choices import ESTADOS, ESTADO_CIVIL

class ModeloContrato(models.Model):
    id = models.AutoField(primary_key=True, blank=False, null=False)
    nome_modelo=models.CharField(max_length=250,blank=False, null=True)
    url_modelo=models.CharField(max_length=450,blank=False, null=True)
    cod_modelo = models.CharField(max_length=50,blank=False, null=True)
    modelo_provi = models.BooleanField(default=False, verbose_name="Contrato com Provi")


    def __str__(self):
        return '{0}'.format(self.nome_modelo)

    class Meta:
        verbose_name = 'Modelo de Contrato'
        verbose_name_plural = 'Modelos de Contratos'


class Tag(models.Model):
    id = models.AutoField(primary_key=True, blank=False, null=False)
    cod_curso = models.CharField(max_length=50,blank=False, null=True)
    nome_curso = models.CharField(max_length=200,blank=False, null=True)
    modelo_contrato = models.ForeignKey(ModeloContrato,blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return '{0}'.format(self.nome_curso)

    class Meta:
        verbose_name = 'Curso/Formação'
        verbose_name_plural = 'Cursos/Formações'

class Turma(models.Model):
    id = models.AutoField(primary_key=True, blank=False, null=False)
    cod_turma = models.CharField(max_length=50,blank=False, null=True)
    curso = models.ForeignKey(Tag, null=True, on_delete=models.SET_NULL)
    periodo = models.CharField(max_length=200,blank=False, null=True)
    qtd_encontros =  models.IntegerField()
    token_klickmembers = models.CharField(max_length=200,blank=False, null=True)
    url_klickmembers = models.CharField(max_length=300,blank=False, null=True)
    status_turma = models.BooleanField(default=False, verbose_name="Turma Concluída?")

    def __str__(self):
        return '{0} - {1}'.format(self.cod_turma, self.periodo)

    class Meta:
        verbose_name = 'Turma'
        verbose_name_plural = 'Turmas'



class Contrato(models.Model):
    id = models.AutoField(primary_key=True, blank=False, null=False)
    contratante = models.CharField(max_length=250,verbose_name="Contratante",blank=False, null=True)
    cod_provi =  models.CharField(max_length=50,blank=True, null=True)
    rg = models.CharField(max_length=25,verbose_name="RG",blank=False, null=True)
    cpf = models.CharField(max_length=14,verbose_name="CPF",blank=False, null=True)
    endereco = models.CharField(max_length=250,blank=False, null=True)
    endereco_cidade = models.CharField(max_length=100,verbose_name="Cidade",blank=False, null=True)
    endereco_uf = models.CharField(max_length=2,choices=ESTADOS,verbose_name="UF", blank=False, null=True)
    endereco_bairro = models.CharField(max_length=100,verbose_name="Bairro",blank=False, null=True)
    cep = models.CharField(max_length=100,verbose_name="CEP",blank=False, null=True)
    complemento_endereco = models.CharField(max_length=100,verbose_name="Complemento",blank=True, null=True)
    numero_endereco = models.CharField(max_length=100,verbose_name="Número do endereço",blank=False, null=True)
    telefone = models.CharField(max_length=100,blank=False, null=True)
    data_nascimento = models.DateField(verbose_name="Data de Nascimento",blank=False, null=True)
    email = models.CharField(max_length=100,blank=False, null=True)
    estado_civil = models.CharField(max_length=1,choices=ESTADO_CIVIL,blank=False, null=True)
    profissao = models.CharField(max_length=100,verbose_name="Profissão",blank=False, null=True)
    turma = models.ForeignKey(Turma, null=True, on_delete=models.SET_NULL)
    curso = models.ForeignKey(Tag, null=True, on_delete=models.SET_NULL)
    forma_pagamento=models.CharField(max_length=250,blank=False, null=True)
    condicoes_pagamento=models.TextField(blank=False, null=True)
    extra_bonus =  models.CharField(max_length=100,blank=True, null=True)
    data_criacao = models.CharField(max_length=100,blank=True, null=True)
    data_recebimento = models.DateTimeField(default=timezone.now)
    consultor = models.CharField(max_length=100,blank=True, null=True)
    url_contrato=models.CharField(max_length=250,blank=False, null=True)
    assinado = models.BooleanField(default=False, blank=True, null=True, verbose_name="Assinado?")

    def __str__(self):
        return '{0} - {1}'.format(self.contratante, self.cpf)

    class Meta:
        verbose_name = 'Contrato'
        verbose_name_plural = 'Contratos'

class Transaction(models.Model):
    id = models.AutoField(primary_key=True, blank=False, null=False)
    data_cadastro = models.DateTimeField(default=timezone.now)
    contrato = models.ForeignKey(Contrato, null=True, on_delete=models.SET_NULL)
    cod_transacao = models.CharField(max_length=200,blank=False, null=True)

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
        verbose_name = 'Consultor'
        verbose_name_plural = 'Consultores'
