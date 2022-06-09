# Generated by Django 4.0.3 on 2022-05-18 13:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Batiment',
            fields=[
                ('type_batiment', models.CharField(choices=[('Agriculture', 'Agriculture'), ('Activités de bureaux', 'Activités de bureaux'), ('Grande distribution alimentaire', 'Grande distribution alimentaire'), ('Petit et moyen commerce alimentaire', 'Petit et moyen commerce alimentaire'), ('Commerce non alimentaire', 'Commerce non alimentaire'), ('Métiers de bouche', 'Métiers de bouche'), ('Cafés Hôtels Restaurants', 'Cafés Hôtels Restaurants'), ('Industrie', 'Industrie'), ('BTP', 'BTP'), ('Coiffeur, beauté, esthéticienne', 'Coiffeur, beauté, esthéticienne'), ('Mécanique automobile, 2 roues, vélo', 'Mécanique automobile, 2 roues, vélo'), ('Santé(Clinique, laboratoire, pharmacie)', 'Santé(Clinique, laboratoire, pharmacie)'), ('Agences bancaires', 'Agences bancaires'), ('Telecom(Data Center)', 'Telecom(Data Center)'), ('Autre', 'Autre')], max_length=255, verbose_name='Type de Bâtiment')),
                ('nb_batiment', models.PositiveIntegerField(verbose_name='Nombre de bâtiments de ce type')),
                ('nb_etages', models.PositiveIntegerField(verbose_name="Nombre d'étages")),
                ('num_sites', models.PositiveIntegerField(blank=True, verbose_name='N° de site')),
                ('taille', models.CharField(choices=[('Petit', 'Petit (< 150m²)'), ('Moyen', 'Moyen (150-500m²)'), ('Grand', 'Grand (500m²-1000m²)'), ('Tres grand', 'Très grand (> 1000m²)')], max_length=255, verbose_name='Taille')),
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Batteries',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=100, verbose_name='Modèle')),
                ('nom_francais', models.CharField(blank=True, max_length=100, verbose_name=' Nom Français')),
                ('nom_anglais', models.CharField(blank=True, max_length=100, verbose_name=' Nom Anglais')),
                ('cout', models.FloatField(verbose_name='Coût dachat€')),
                ('capacite', models.FloatField(verbose_name='Capacité Batteries (kWh)')),
                ('puissance', models.FloatField(verbose_name='Puissance Batteries (kWh)')),
            ],
            options={
                'verbose_name': 'batteries',
            },
        ),
        migrations.CreateModel(
            name='BDD',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('N', models.FloatField(null=True)),
                ('Onduleur_1', models.CharField(max_length=100, null=True)),
                ('Batterie_1', models.CharField(blank=True, max_length=100, null=True)),
                ('Nombre_Batterie_1', models.FloatField(blank=True, null=True)),
                ('Onduleur_2', models.CharField(blank=True, max_length=100, null=True)),
                ('Batterie_2', models.CharField(blank=True, max_length=100, null=True)),
                ('Nombre_Batterie_2', models.PositiveIntegerField(blank=True, null=True)),
                ('Onduleur_3', models.CharField(blank=True, max_length=100, null=True)),
                ('Module_batterie_1', models.CharField(blank=True, max_length=100, null=True)),
                ('Module_batterie_2', models.CharField(blank=True, max_length=100, null=True)),
                ('Electrical_installation', models.CharField(max_length=100, null=True)),
                ('Nb_modules_min', models.FloatField(null=True)),
                ('Puissance_centrale_max', models.FloatField(null=True)),
                ('Capacit_batterie', models.FloatField(null=True)),
                ('Prix_total_achat', models.FloatField(null=True)),
            ],
            options={
                'verbose_name': 'BASE DE DONNES DE SOLUTIONS ',
            },
        ),
        migrations.CreateModel(
            name='BDDBat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=100, verbose_name="Secteurs d'activité proposés par SEIZE (utilisé)")),
                ('moy_kWh_avant', models.FloatField(verbose_name='Moyenne par Secteur (kWh/an/m²) AVANT AUDIT ')),
                ('moy_kWh_apres', models.FloatField(verbose_name='Moyenne par Secteur (kWh/an/m²) APRES AUDIT')),
                ('moy_euros_avant', models.FloatField(verbose_name='Moyenne par Secteur (€/an/m²) AVANT AUDIT ')),
                ('moy_euros_apres', models.FloatField(verbose_name='Moyenne par Secteur (€/an/m²) APRES AUDIT')),
                ('cout_kWh_avant', models.FloatField(verbose_name='Coût du kWh moyen avant audit')),
                ('cout_kWh_apres', models.FloatField(blank=True, null=True, verbose_name='Coût du kWh moyen après audit')),
                ('gain', models.FloatField(blank=True, null=True, verbose_name='Gain atteingable dans le secteur')),
            ],
        ),
        migrations.CreateModel(
            name='Cables',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=100, verbose_name='Modèle')),
                ('nom_francais', models.CharField(blank=True, max_length=100, verbose_name=' Nom Français')),
                ('nom_anglais', models.CharField(blank=True, max_length=100, verbose_name=' Nom Anglais')),
                ('cout', models.FloatField(verbose_name='Coût dachat + installation en €/ml')),
            ],
            options={
                'verbose_name': 'CABLES ',
            },
        ),
        migrations.CreateModel(
            name='CatalogueSolution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('taille', models.FloatField(verbose_name='Taille en kWc')),
                ('installation', models.CharField(choices=[('Monophasée', 'Monophasée'), ('Triphasée', 'Triphasée')], max_length=255, verbose_name='Installation')),
                ('marge', models.FloatField(verbose_name='marge en %')),
            ],
            options={
                'verbose_name': 'Catalogue - Solution',
            },
        ),
        migrations.CreateModel(
            name='CentraleBatiment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('batiment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PV.batiment')),
            ],
        ),
        migrations.CreateModel(
            name='Cheminement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=100, verbose_name='Modèle')),
                ('nom_francais', models.CharField(blank=True, max_length=100, verbose_name=' Nom Français')),
                ('nom_anglais', models.CharField(blank=True, max_length=100, verbose_name=' Nom Anglais')),
                ('cout', models.FloatField(verbose_name='Coût dachat + installation en €/ml')),
            ],
            options={
                'verbose_name': 'CHEMINEMENT ',
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('nom_entreprise', models.CharField(max_length=255, verbose_name='Nom Entreprise')),
                ('mail', models.EmailField(max_length=254, verbose_name='E-mail')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Divers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=100, verbose_name='Modèle')),
                ('nom_francais', models.CharField(blank=True, max_length=100, verbose_name=' Nom Français')),
                ('nom_anglais', models.CharField(blank=True, max_length=100, verbose_name=' Nom Anglais')),
                ('cout', models.FloatField(verbose_name='Coût dachat')),
            ],
            options={
                'verbose_name': 'DIVERS ',
            },
        ),
        migrations.CreateModel(
            name='EDF',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('puissance', models.FloatField(verbose_name='Puissance souscrite (kVA)')),
                ('reference', models.CharField(choices=[('Mensuelle', 'Mensuelle '), ('Bimestrielle', 'Bimestrielle '), ('Annuelle', 'Annuelle ')], max_length=255, verbose_name='Reference')),
                ('nb_kW', models.FloatField(verbose_name='Nombre KWh facture')),
                ('facture', models.FloatField(verbose_name='Montant facture (€)')),
                ('batiment', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='batiment_edf', to='PV.batiment')),
            ],
        ),
        migrations.CreateModel(
            name='Emisission_CO2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('territ', models.CharField(max_length=100, verbose_name='Territoire')),
                ('emission', models.FloatField(verbose_name='Hypothèses Emissions CO2 en kg CO2/kWh\t')),
            ],
        ),
        migrations.CreateModel(
            name='Ensolleilement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('territ', models.CharField(max_length=100, verbose_name='Territoire')),
                ('h_soleil', models.FloatField(verbose_name='Heure de lever du soleil')),
                ('h_ensol', models.FloatField(verbose_name="Heure d'enseillement par jour (h)")),
                ('h_ensol_ref', models.FloatField(verbose_name="Heure d'enseillement journalier de référence (kWh/m2) ")),
                ('PR', models.FloatField(verbose_name='PR (Entre 0 et 1)')),
                ('Ep_moyenne', models.FloatField(verbose_name='Energie produite moyenne (kWh/kWc)')),
                ('Ep_favorable', models.FloatField(verbose_name='Energie produite jour favorable (kWh/kWc)')),
                ('Ep_defavorable', models.FloatField(verbose_name='Energie produite jour défavorable(kWh/kWc)')),
            ],
            options={
                'verbose_name': 'Territoire',
            },
        ),
        migrations.CreateModel(
            name='Extensions_Batteries',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=100, verbose_name='Modèle')),
                ('nom_francais', models.CharField(blank=True, max_length=100, verbose_name=' Nom Français')),
                ('nom_anglais', models.CharField(blank=True, max_length=100, verbose_name=' Nom Anglais')),
                ('cout', models.FloatField(verbose_name='Coût dachat€')),
                ('capacite', models.FloatField(verbose_name='Capacité Batteries (kWh)')),
                ('puissance', models.FloatField(verbose_name='Puissance Batteries (kWh)')),
            ],
            options={
                'verbose_name': 'EXTENSIONS BATTERIES ',
            },
        ),
        migrations.CreateModel(
            name='EZ_DRIVE',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=1000, verbose_name='Produit')),
                ('valeur', models.FloatField(verbose_name='Valeur')),
                ('unite', models.CharField(max_length=100, verbose_name='Unité')),
                ('invest', models.FloatField(blank=True, null=True, verbose_name='Investissement initial en €')),
            ],
        ),
        migrations.CreateModel(
            name='FacturationItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=255, verbose_name="Type d'équipement")),
                ('article', models.CharField(max_length=255, verbose_name='Article')),
                ('cout_HA_unit', models.FloatField(verbose_name='Coût HA unitaire')),
                ('taux_transport', models.FloatField(verbose_name='Taux transport en % du prix HA')),
                ('unite', models.CharField(choices=[('Unité', 'Unité'), ('/ Wc', '/ Wc'), ('/ ml', '/ ml')], default='Unité', max_length=255, verbose_name='Unité')),
            ],
            options={
                'verbose_name': 'Equipement',
            },
        ),
        migrations.CreateModel(
            name='Hyp_cout_mobilite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=1000, verbose_name='Produit')),
                ('valeur', models.FloatField(verbose_name='Valeur')),
                ('unite', models.CharField(max_length=100, verbose_name='Unité')),
            ],
            options={
                'verbose_name': 'Coût Mobilité',
            },
        ),
        migrations.CreateModel(
            name='Inge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=100, verbose_name='Modèle')),
                ('nom_francais', models.CharField(blank=True, max_length=100, verbose_name=' Nom Français')),
                ('nom_anglais', models.CharField(blank=True, max_length=100, verbose_name=' Nom Anglais')),
                ('cout', models.FloatField(verbose_name='Coût dachat en €')),
            ],
            options={
                'verbose_name': 'INGENIERIE ',
            },
        ),
        migrations.CreateModel(
            name='Main_doeuvre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=100, verbose_name='Modèle')),
                ('nom_francais', models.CharField(blank=True, max_length=100, verbose_name=' Nom Français')),
                ('nom_anglais', models.CharField(blank=True, max_length=100, verbose_name=' Nom Anglais')),
                ('cout', models.FloatField(verbose_name='Coût dachat')),
            ],
            options={
                'verbose_name': "MAIN D'OEUVRES ",
            },
        ),
        migrations.CreateModel(
            name='ModulesPV',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nom', models.CharField(max_length=100)),
                ('Puissance_modulaire_kW', models.FloatField(verbose_name='Puissance Modulaire (kWc)')),
                ('Surface_Panneau_m2', models.FloatField(verbose_name='Surface (m2)')),
                ('Cout', models.FloatField(verbose_name="Coût d'achat € ")),
            ],
            options={
                'verbose_name': 'PV - Module',
            },
        ),
        migrations.CreateModel(
            name='Monitoring',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=100, verbose_name='Modèle')),
                ('nom_francais', models.CharField(blank=True, max_length=100, verbose_name=' Nom Français')),
                ('nom_anglais', models.CharField(blank=True, max_length=100, verbose_name=' Nom Anglais')),
                ('cout', models.FloatField(verbose_name='Coût dachat')),
                ('puissance_max', models.FloatField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'MONITORING ',
            },
        ),
        migrations.CreateModel(
            name='Onduleurs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=100, verbose_name='Modèle')),
                ('nom_francais', models.CharField(blank=True, max_length=100, verbose_name=' Nom Français')),
                ('nom_anglais', models.CharField(blank=True, max_length=100, verbose_name=' Nom Anglais')),
                ('cout', models.FloatField(verbose_name='Coût dachat')),
                ('install', models.CharField(max_length=100, verbose_name='Installation  éléctrique')),
                ('tension', models.FloatField(blank=True, null=True, verbose_name='Tension DC min')),
                ('puissance_dc', models.FloatField(verbose_name='Puissance DC max en kWc')),
                ('puissance_ac', models.FloatField(verbose_name='Puissance AC max en kWc')),
            ],
            options={
                'verbose_name': 'ONDULEURS ',
            },
        ),
        migrations.CreateModel(
            name='Profil_types',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_profil', models.CharField(max_length=255, verbose_name='Profil')),
            ],
            options={
                'verbose_name': 'Profil Type',
            },
        ),
        migrations.CreateModel(
            name='Structure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=100, verbose_name='Modèle')),
                ('nom_francais', models.CharField(blank=True, max_length=100, verbose_name=' Nom Français')),
                ('nom_anglais', models.CharField(blank=True, max_length=100, verbose_name=' Nom Anglais')),
                ('cout', models.FloatField(verbose_name='Coût dachat en €/Wc')),
            ],
            options={
                'verbose_name': 'STRUCTURE ',
            },
        ),
        migrations.CreateModel(
            name='Tableaux',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=100, verbose_name='Modèle')),
                ('nom_francais', models.CharField(blank=True, max_length=100, verbose_name=' Nom Français')),
                ('nom_anglais', models.CharField(blank=True, max_length=100, verbose_name=' Nom Anglais')),
                ('cout', models.FloatField(verbose_name='Coût dachat')),
            ],
            options={
                'verbose_name': 'TABLEAUX ',
            },
        ),
        migrations.CreateModel(
            name='Tailles_Standards',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('taille', models.FloatField(verbose_name='Taille standard')),
                ('catag', models.CharField(choices=[('Centrale', 'Centrale '), ('Batterie', 'Batterie ')], default='Batterie', max_length=255, verbose_name=" Type d'équipement")),
            ],
        ),
        migrations.CreateModel(
            name='Taxe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('territ', models.CharField(max_length=100, verbose_name='Territoire')),
                ('transport_1', models.FloatField(verbose_name='Main doeuvre en %')),
                ('transport_2', models.FloatField(verbose_name='Panneaux en %')),
                ('transport_3', models.FloatField(verbose_name='Le reste en %')),
                ('Pose_PV_toiture_tole', models.FloatField(verbose_name=' Pose PV toiture tôle + Raccordement < 50kWc')),
                ('Pose_PV_toiture_tole_2', models.FloatField(verbose_name='Pose PV toiture tôle + Raccordement > 50kWc')),
                ('Pose_PV_toiture_terrasse', models.FloatField(verbose_name='Pose PV toiture Terrasse + Raccordement < 50kWc')),
                ('Pose_PV_toiture_terrasse_2', models.FloatField(verbose_name=' Pose PV toiture Terrasse + Raccordement > 50kWc')),
                ('Pose_PV_toiture_tuile', models.FloatField(verbose_name=' Pose PV toiture Tuiles +Raccordement < 10kWc')),
                ('Pose_PV_toiture_tuile_2', models.FloatField(verbose_name=' Pose PV toiture Tuiles +Raccordement < 50kWc')),
                ('Pose_PV_toiture_tole_3', models.FloatField(verbose_name='  Pose PV toiture Tuiles +Raccordement > 50kWc')),
                ('pose', models.FloatField(verbose_name=' Pose plot soprasolar ')),
                ('install', models.FloatField(verbose_name=' Installation et mise en service borne')),
                ('tva_entreprise', models.FloatField()),
                ('tva_particulier', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Toiture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('toiture', models.CharField(choices=[('Terrasse', 'Terrasse'), ('Tôle bac acier trapézoïdal', 'Tôle bac acier trapézoïdal')], max_length=255, verbose_name='Toiture')),
                ('surface', models.FloatField(verbose_name='Surface de toiture (m²)')),
                ('batiment', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='batiment_toiture', to='PV.batiment')),
            ],
        ),
        migrations.CreateModel(
            name='SolutionBatiment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('centrale_batiment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PV.centralebatiment')),
                ('solution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PV.cataloguesolution')),
            ],
        ),
        migrations.CreateModel(
            name='Profil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('batiment', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='batiment_profil', to='PV.batiment')),
                ('type_profil', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PV.profil_types')),
            ],
        ),
        migrations.CreateModel(
            name='Modules_factu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('module', models.CharField(max_length=255)),
                ('qt', models.PositiveIntegerField(verbose_name='Quantité')),
                ('cout_unitaire', models.FloatField(verbose_name='Coût HA unitaire')),
                ('cout_unitaire_transport', models.FloatField(blank=True, verbose_name='Coût Unitaire Transport')),
                ('cout_total', models.FloatField(verbose_name='Coût Total HA')),
                ('cout_total_transport', models.FloatField(blank=True, verbose_name='Coût Total Transport')),
                ('marge', models.FloatField()),
                ('prix', models.FloatField(verbose_name='Prix Vendu')),
                ('prix_unitaire', models.FloatField(verbose_name='Prix Unitaire')),
                ('batiment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PV.batiment')),
            ],
        ),
        migrations.CreateModel(
            name='Mobilite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vehicule_fonction', models.PositiveIntegerField(verbose_name='Nombre de véhicules de fonction')),
                ('km_an_vehicule_fonction', models.PositiveIntegerField(verbose_name='Nombre de km/an véhicule de fonction')),
                ('vehicule_utilitaire', models.PositiveIntegerField(verbose_name='Nombre de véhicules utilitaires')),
                ('km_an_vehicule_utilitaire', models.PositiveIntegerField(verbose_name='Nombre de km/an véhicule utilitaires')),
                ('parking', models.CharField(choices=[('Oui', 'Oui '), ('Non', 'Non ')], max_length=255, verbose_name='Présence parking ')),
                ('acces', models.CharField(blank=True, choices=[('Public', 'Public '), ('Privé', 'Privé ')], max_length=255, verbose_name='Accessibilité Parking')),
                ('borne', models.CharField(choices=[('Oui', 'Oui '), ('Non', 'Non ')], max_length=255, verbose_name='Option Borne')),
                ('pt_de_charge', models.PositiveIntegerField(blank=True, verbose_name='Nombre de point de charges desirés')),
                ('batiment', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='batiment_mobilite', to='PV.batiment')),
            ],
        ),
        migrations.CreateModel(
            name='Localisation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adresse', models.CharField(max_length=255)),
                ('batiment', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='Batiment_localisation', to='PV.batiment')),
                ('territ', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='Territoire', to='PV.ensolleilement')),
            ],
        ),
        migrations.CreateModel(
            name='ItemQuantite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantite', models.IntegerField(default=0, verbose_name='Quantité')),
                ('catalogue_solution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PV.cataloguesolution', verbose_name='Solution')),
                ('facturation_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PV.facturationitem', verbose_name='Elément')),
            ],
            options={
                'verbose_name': 'Catalogue - Entrée',
            },
        ),
        migrations.CreateModel(
            name='Enseigne',
            fields=[
                ('name', models.CharField(max_length=255, verbose_name="Nom de l'enseigne")),
                ('secteur', models.CharField(max_length=255, verbose_name='Secteur')),
                ('nb_sites', models.PositiveIntegerField(verbose_name='Nombre de sites')),
                ('effectif', models.PositiveIntegerField(verbose_name='Effectif')),
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='User_Enseigne', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Electrification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('installation', models.CharField(choices=[('Monophasée', 'Monophasée'), ('Triphasée', 'Triphasée')], max_length=255, verbose_name='Installation')),
                ('souscription', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='batiment_souscription', to='PV.edf')),
            ],
        ),
        migrations.CreateModel(
            name='Coeffs_Weekend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heure', models.TimeField(null=True)),
                ('coeff', models.FloatField(null=True)),
                ('profil', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Profil_Weekend', to='PV.profil_types')),
            ],
            options={
                'verbose_name': 'Coeffs Weekend',
            },
        ),
        migrations.CreateModel(
            name='Coeffs_Ouvres',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heure', models.TimeField(null=True)),
                ('coeff', models.FloatField(null=True)),
                ('profil', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Profil_Ouvre', to='PV.profil_types')),
            ],
            options={
                'verbose_name': 'Coeffs Jour Ouvré',
            },
        ),
        migrations.AddField(
            model_name='cataloguesolution',
            name='elements',
            field=models.ManyToManyField(through='PV.ItemQuantite', to='PV.facturationitem'),
        ),
        migrations.AddField(
            model_name='batiment',
            name='enseigne',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='Batiment_Enseigne', to='PV.enseigne'),
        ),
        migrations.CreateModel(
            name='CourbeDeCharge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('Ouvré', 'Ouvré'), ('Weekend', 'Weekend')], max_length=255, verbose_name='Jour')),
                ('coeff_0', models.FloatField(default=20, verbose_name='00:00 (%)')),
                ('coeff_1', models.FloatField(default=20, verbose_name='01:00 (%)')),
                ('coeff_2', models.FloatField(default=20, verbose_name='02:00')),
                ('coeff_3', models.FloatField(default=20, verbose_name='03:00')),
                ('coeff_4', models.FloatField(default=20, verbose_name='04:00')),
                ('coeff_5', models.FloatField(default=20, verbose_name='05:00')),
                ('coeff_6', models.FloatField(default=20, verbose_name='06:00')),
                ('coeff_7', models.FloatField(default=20, verbose_name='07:00')),
                ('coeff_8', models.FloatField(default=20, verbose_name='08:00')),
                ('coeff_9', models.FloatField(default=20, verbose_name='09:00')),
                ('coeff_10', models.FloatField(default=20, verbose_name='10:00')),
                ('coeff_11', models.FloatField(default=20, verbose_name='11:00')),
                ('coeff_12', models.FloatField(default=20, verbose_name='12:00')),
                ('coeff_13', models.FloatField(default=20, verbose_name='13:00')),
                ('coeff_14', models.FloatField(default=20, verbose_name='14:00')),
                ('coeff_15', models.FloatField(default=20, verbose_name='15:00')),
                ('coeff_16', models.FloatField(default=20, verbose_name='16:00')),
                ('coeff_17', models.FloatField(default=20, verbose_name='17:00')),
                ('coeff_18', models.FloatField(default=20, verbose_name='18:00')),
                ('coeff_19', models.FloatField(default=20, verbose_name='19:00')),
                ('coeff_20', models.FloatField(default=20, verbose_name='20:00')),
                ('coeff_21', models.FloatField(default=20, verbose_name='21:00')),
                ('coeff_22', models.FloatField(default=20, verbose_name='22:00')),
                ('coeff_23', models.FloatField(default=20, verbose_name='23:00')),
                ('profil', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PV.profil_types', verbose_name='Profil')),
            ],
            options={
                'unique_together': {('profil', 'type')},
            },
        ),
    ]
