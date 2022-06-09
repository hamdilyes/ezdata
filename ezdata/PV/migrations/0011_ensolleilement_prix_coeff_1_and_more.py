# Generated by Django 4.0.3 on 2022-05-26 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PV', '0010_alter_mobilite_acces_alter_mobilite_borne_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ensolleilement',
            name='prix_coeff_1',
            field=models.FloatField(default=0, verbose_name='Coeff D 1 - Prix en c€ / kWh'),
        ),
        migrations.AddField(
            model_name='ensolleilement',
            name='prix_coeff_1_1',
            field=models.FloatField(default=0, verbose_name='Coeff D 1.1 - Prix en c€ / kWh'),
        ),
        migrations.AddField(
            model_name='ensolleilement',
            name='prix_coeff_1_2',
            field=models.FloatField(default=0, verbose_name='Coeff D 1.2 - Prix en c€ / kWh'),
        ),
        migrations.AddField(
            model_name='ensolleilement',
            name='prix_coeff_1_35',
            field=models.FloatField(default=0, verbose_name='Coeff D 1.35 - Prix en c€ / kWh'),
        ),
    ]