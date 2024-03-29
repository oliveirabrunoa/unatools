# Generated by Django 2.2.10 on 2020-06-19 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0004_usersmoskit_principal'),
    ]

    operations = [
        migrations.CreateModel(
            name='UsersCRM',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.CharField(max_length=80, null=True)),
                ('nome', models.CharField(max_length=200, null=True)),
            ],
            options={
                'verbose_name_plural': 'UsersCRM',
                'verbose_name': 'UsersCRM',
            },
        ),
        migrations.DeleteModel(
            name='UsersMoskit',
        ),
        migrations.AlterField(
            model_name='transaction',
            name='lead',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.DeleteModel(
            name='Lead',
        ),
    ]
