# Generated by Django 4.0.3 on 2022-05-20 15:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('PV', '0007_alter_projet_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enseigne',
            name='projet',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.SET_DEFAULT, to='PV.projet'),
        ),
    ]