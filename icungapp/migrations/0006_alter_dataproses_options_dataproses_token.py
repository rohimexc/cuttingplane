# Generated by Django 4.1 on 2023-04-09 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('icungapp', '0005_dataproses_delete_judulhasil'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dataproses',
            options={},
        ),
        migrations.AddField(
            model_name='dataproses',
            name='token',
            field=models.CharField(max_length=30, null=True),
        ),
    ]