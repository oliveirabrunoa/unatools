# Generated by Django 2.2.13 on 2020-06-25 03:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0009_auto_20200622_0206'),
    ]

    operations = [
        migrations.AddField(
            model_name='turma',
            name='status_turma',
            field=models.BooleanField(default=False, verbose_name='Turma Concluída?'),
        ),
    ]
