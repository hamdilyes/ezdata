# Generated by Django 4.0.3 on 2022-06-28 16:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('PV', '0019_alter_profilperso_profil'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExportSite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enseigne', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PV.enseigne', verbose_name='Enseigne')),
                ('projet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PV.projet', verbose_name='Projet')),
            ],
        ),
    ]
