# Generated by Django 4.1 on 2023-04-09 15:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('icungapp', '0003_proses_alter_judulhasil_options'),
    ]

    operations = [
        migrations.DeleteModel(
            name='InputData',
        ),
        migrations.DeleteModel(
            name='Proses',
        ),
    ]
