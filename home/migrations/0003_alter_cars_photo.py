# Generated by Django 3.2.6 on 2022-06-06 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20220606_2148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cars',
            name='photo',
            field=models.CharField(max_length=2500, unique=True, verbose_name='foto'),
        ),
    ]