# Generated by Django 2.2.13 on 2020-07-07 02:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0013_contrato_url_contrato'),
    ]

    operations = [
        migrations.AddField(
            model_name='contrato',
            name='consultor',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='contrato',
            name='data_criacao',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]