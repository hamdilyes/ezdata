# Generated by Django 4.0.3 on 2022-05-18 15:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('PV', '0004_alter_projet_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='enseigne',
            name='projet',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='PV.projet'),
        ),
    ]