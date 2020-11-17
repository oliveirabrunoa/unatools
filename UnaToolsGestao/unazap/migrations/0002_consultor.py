# Generated by Django 2.2.13 on 2020-10-09 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unazap', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Consultor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nome_consultor', models.CharField(max_length=50, null=True)),
                ('num_whatsapp_consultor', models.CharField(max_length=200, null=True)),
            ],
            options={
                'verbose_name_plural': 'Consultora',
                'verbose_name': 'Consultor',
            },
        ),
    ]
