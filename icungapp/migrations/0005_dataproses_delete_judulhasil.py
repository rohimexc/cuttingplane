# Generated by Django 4.1 on 2023-04-09 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('icungapp', '0004_delete_inputdata_delete_proses'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataProses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hasil', models.CharField(max_length=30, null=True)),
                ('kendala', models.IntegerField(null=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.DeleteModel(
            name='JudulHasil',
        ),
    ]
