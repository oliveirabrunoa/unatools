# Generated by Django 2.2.10 on 2020-02-29 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0003_usersmoskit'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersmoskit',
            name='principal',
            field=models.BooleanField(default=False),
        ),
    ]
