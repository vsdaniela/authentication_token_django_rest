# Generated by Django 3.2.4 on 2021-07-06 08:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_persona_telefono'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='persona',
            name='telefono',
        ),
    ]
