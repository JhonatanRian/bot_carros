# Generated by Django 3.2.6 on 2022-06-06 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cars',
            name='id_car',
        ),
        migrations.AlterField(
            model_name='cars',
            name='source',
            field=models.CharField(max_length=1500, unique=True, verbose_name='link do anuncio'),
        ),
    ]
