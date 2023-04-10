# Generated by Django 4.1.5 on 2023-04-08 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("icungapp", "0002_judulhasil_alter_inputdata_options"),
    ]

    operations = [
        migrations.CreateModel(
            name="Proses",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("header", models.CharField(max_length=500, null=True)),
                ("data", models.CharField(max_length=10000, null=True)),
                ("indeks", models.CharField(max_length=300, null=True)),
            ],
        ),
        migrations.AlterModelOptions(name="judulhasil", options={"ordering": ["id"]},),
    ]