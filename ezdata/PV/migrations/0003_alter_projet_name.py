# Generated by Django 4.0.3 on 2022-05-18 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PV', '0002_projet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projet',
            name='name',
            field=models.CharField(default='-', max_length=255, verbose_name='Nom du projet'),
        ),
    ]
