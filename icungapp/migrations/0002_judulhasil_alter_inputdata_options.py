# Generated by Django 4.1 on 2022-12-28 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('icungapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='JudulHasil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('judul', models.CharField(max_length=30, null=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name='inputdata',
            options={'ordering': ['id']},
        ),
    ]
