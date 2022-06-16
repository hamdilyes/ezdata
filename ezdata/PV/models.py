from django.db import models
from django.forms.models import model_to_dict

from users.models import *


# Modèles de la BDD INGENIEURS

class ModulesPV(models.Model):
    Nom = models.CharField(max_length=100)
    Puissance_modulaire_kW = models.FloatField(
        verbose_name='Puissance Modulaire (kWc)')
    Surface_Panneau_m2 = models.FloatField(verbose_name='Surface (m²)')
    Cout = models.FloatField(verbose_name="Coût d'achat € ")

    def __str__(self):
        return self.Nom

    class Meta:
        verbose_name = "PV - Module"


class Batteries(models.Model):
    model = models.CharField(max_length=100, verbose_name='Modèle')
    nom_francais = models.CharField(
        max_length=100, blank=True, verbose_name=' Nom Français')
    nom_anglais = models.CharField(
        max_length=100, blank=True, verbose_name=' Nom Anglais')
    cout = models.FloatField(verbose_name='Coût dachat€')
    capacite = models.FloatField(verbose_name='Capacité Batteries (kWh)')
    puissance = models.FloatField(verbose_name='Puissance Batteries (kWh)')

    def __str__(self):
        return self.model

    class Meta:
        verbose_name = "batteries"


class Extensions_Batteries(models.Model):
    model = models.CharField(max_length=100, verbose_name='Modèle')
    nom_francais = models.CharField(
        max_length=100, blank=True, verbose_name=' Nom Français')
    nom_anglais = models.CharField(
        max_length=100, blank=True, verbose_name=' Nom Anglais')
    cout = models.FloatField(verbose_name='Coût dachat€')
    capacite = models.FloatField(verbose_name='Capacité Batteries (kWh)')
    puissance = models.FloatField(verbose_name='Puissance Batteries (kWh)')

    class Meta:
        verbose_name = "EXTENSIONS BATTERIES "


class Onduleurs(models.Model):
    model = models.CharField(max_length=100, verbose_name="Modèle")
    nom_francais = models.CharField(
        max_length=100, blank=True, verbose_name=' Nom Français')
    nom_anglais = models.CharField(
        max_length=100, blank=True, verbose_name=' Nom Anglais')
    cout = models.FloatField(verbose_name='Coût dachat')
    install = models.CharField(
        max_length=100, verbose_name='Installation  éléctrique')
    tension = models.FloatField(
        verbose_name='Tension DC min', blank=True, null=True)
    puissance_dc = models.FloatField(verbose_name='Puissance DC max en kWc')
    puissance_ac = models.FloatField(verbose_name='Puissance AC max en kWc')

    def __str__(self):
        return self.model

    class Meta:
        verbose_name = "ONDULEURS "


class Monitoring(models.Model):
    model = models.CharField(max_length=100, verbose_name="Modèle")
    nom_francais = models.CharField(
        max_length=100, blank=True, verbose_name=' Nom Français')
    nom_anglais = models.CharField(
        max_length=100, blank=True, verbose_name=' Nom Anglais')
    cout = models.FloatField(verbose_name='Coût dachat')
    puissance_max = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.model

    class Meta:
        verbose_name = "MONITORING "

# Penser a ajouter les unités


class Main_doeuvre(models.Model):
    model = models.CharField(max_length=100, verbose_name="Modèle")
    nom_francais = models.CharField(
        max_length=100, blank=True, verbose_name=' Nom Français')
    nom_anglais = models.CharField(
        max_length=100, blank=True, verbose_name=' Nom Anglais')
    cout = models.FloatField(verbose_name='Coût dachat')

    def __str__(self):
        return self.model

    class Meta:
        verbose_name = "MAIN D'OEUVRES "


class Tableaux(models.Model):
    model = models.CharField(max_length=100, verbose_name="Modèle")
    nom_francais = models.CharField(
        max_length=100, blank=True, verbose_name=' Nom Français')
    nom_anglais = models.CharField(
        max_length=100, blank=True, verbose_name=' Nom Anglais')
    cout = models.FloatField(verbose_name='Coût dachat')

    def __str__(self):
        return self.model

    class Meta:
        verbose_name = "TABLEAUX "


class Cables(models.Model):
    model = models.CharField(max_length=100, verbose_name="Modèle")
    nom_francais = models.CharField(
        max_length=100, blank=True, verbose_name=' Nom Français')
    nom_anglais = models.CharField(
        max_length=100, blank=True, verbose_name=' Nom Anglais')
    cout = models.FloatField(verbose_name='Coût dachat + installation en €/ml')

    def __str__(self):
        return self.model

    class Meta:
        verbose_name = "CABLES "


class Cheminement(models.Model):
    model = models.CharField(max_length=100, verbose_name="Modèle")
    nom_francais = models.CharField(
        max_length=100, blank=True, verbose_name=' Nom Français')
    nom_anglais = models.CharField(
        max_length=100, blank=True, verbose_name=' Nom Anglais')
    cout = models.FloatField(verbose_name='Coût dachat + installation en €/ml')

    def __str__(self):
        return self.model

    class Meta:
        verbose_name = "CHEMINEMENT "


class Divers(models.Model):
    model = models.CharField(max_length=100, verbose_name="Modèle")
    nom_francais = models.CharField(
        max_length=100, blank=True, verbose_name=' Nom Français')
    nom_anglais = models.CharField(
        max_length=100, blank=True, verbose_name=' Nom Anglais')
    cout = models.FloatField(verbose_name='Coût dachat')

    def __str__(self):
        return self.model

    class Meta:
        verbose_name = "DIVERS "


class Inge(models.Model):
    model = models.CharField(max_length=100, verbose_name="Modèle")
    nom_francais = models.CharField(
        max_length=100, blank=True, verbose_name=' Nom Français')
    nom_anglais = models.CharField(
        max_length=100, blank=True, verbose_name=' Nom Anglais')
    cout = models.FloatField(verbose_name='Coût dachat en €')

    def __str__(self):
        return self.model

    class Meta:
        verbose_name = "INGENIERIE "


class Structure(models.Model):
    model = models.CharField(max_length=100, verbose_name="Modèle")
    nom_francais = models.CharField(
        max_length=100, blank=True, verbose_name=' Nom Français')
    nom_anglais = models.CharField(
        max_length=100, blank=True, verbose_name=' Nom Anglais')
    cout = models.FloatField(verbose_name='Coût dachat en €/Wc')

    def __str__(self):
        return self.model

    class Meta:
        verbose_name = "STRUCTURE "


class BDD(models.Model):
    N = models.FloatField(null=True)
    Onduleur_1 = models.CharField(max_length=100, null=True)
    Batterie_1 = models.CharField(max_length=100, blank=True, null=True)
    Nombre_Batterie_1 = models.FloatField(blank=True, null=True)
    Onduleur_2 = models.CharField(max_length=100, blank=True, null=True)
    Batterie_2 = models.CharField(max_length=100, blank=True, null=True)
    Nombre_Batterie_2 = models.PositiveIntegerField(blank=True, null=True)
    Onduleur_3 = models.CharField(max_length=100, blank=True, null=True)
    Module_batterie_1 = models.CharField(max_length=100, blank=True, null=True)
    Module_batterie_2 = models.CharField(max_length=100, blank=True, null=True)
    Electrical_installation = models.CharField(max_length=100, null=True)
    Nb_modules_min = models.FloatField(null=True)
    Puissance_centrale_max = models.FloatField(null=True)
    Capacit_batterie = models.FloatField(null=True)
    Prix_total_achat = models.FloatField(null=True)

    def __str__(self):
        return self.N

    def get_field(model):
        return model._meta.fields

    class Meta:
        verbose_name = "BASE DE DONNES DE SOLUTIONS "


# Modèles de la BDD COMMERCIAUX

class Client(models.Model):
    nom_entreprise = models.CharField(
        verbose_name='Nom Entreprise', max_length=255)
    mail = models.EmailField(verbose_name='E-mail')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    id = models.AutoField(primary_key=True, editable=False,  blank=True)

    def __str__(self):
        return str(self.nom_entreprise)


class Projet(models.Model):
    name = models.CharField(
        max_length=255, verbose_name='Nom du projet', unique=True)

    id = models.AutoField(primary_key=True, editable=False,  blank=True)

    user = models.ForeignKey(
        MyUser, on_delete=models.CASCADE)

    def _nb_enseignes(self):
        p = Projet.objects.get(pk=self.id)
        rqt = Enseigne.objects.filter(projet=p)
        nb = len(list(rqt))
        return nb
    nb_enseignes = property(_nb_enseignes)

    def __str__(self):
        return str(self.name)


class Enseigne(models.Model):
    projet_defaut = Projet.objects.get(name='-')

    projet = models.ForeignKey(
        Projet, on_delete=models.SET_DEFAULT, default=projet_defaut.id)
    name = models.CharField(verbose_name="Nom de l'enseigne", max_length=255)
    secteur = models.CharField(verbose_name='Secteur', max_length=255)
    nb_sites = models.PositiveIntegerField(
        verbose_name='Nombre de sites', default=1)
    effectif = models.PositiveIntegerField(verbose_name='Effectif')

    # client = models.ForeignKey(
    #     Client, on_delete=models.CASCADE, related_name='Client_Enseigne', blank=True)

    user = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, related_name='User_Enseigne')

    id = models.AutoField(primary_key=True, editable=False,  blank=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "Site"


class Batiment(models.Model):

    type_b = [
        ('Agriculture', 'Agriculture'),
        ('Activités de bureaux', 'Activités de bureaux'),
        ('Grande distribution alimentaire', 'Grande distribution alimentaire'),
        ('Petit et moyen commerce alimentaire',
         'Petit et moyen commerce alimentaire'),
        ('Commerce non alimentaire', 'Commerce non alimentaire'),
        ('Métiers de bouche', 'Métiers de bouche'),
        ('Cafés Hôtels Restaurants', 'Cafés Hôtels Restaurants'),
        ('Industrie', 'Industrie'),
        ('BTP', 'BTP'),
        ('Coiffeur, beauté, esthéticienne', 'Coiffeur, beauté, esthéticienne'),
        ('Mécanique automobile, 2 roues, vélo',
         'Mécanique automobile, 2 roues, vélo'),
        ('Santé(Clinique, laboratoire, pharmacie)',
         'Santé(Clinique, laboratoire, pharmacie)'),
        ('Agences bancaires', 'Agences bancaires'),
        ('Telecom(Data Center)', 'Telecom(Data Center)'),
        ('Autre', 'Autre'),
    ]
    type_batiment = models.CharField(
        verbose_name='Type de Bâtiment', choices=type_b, max_length=255)
    nb_batiment = models.PositiveIntegerField(
        verbose_name='Nombre de bâtiments de ce type')
    nb_etages = models.PositiveIntegerField(verbose_name="Nombre d'étages")
    num_sites = models.PositiveIntegerField(
        verbose_name="N° de site", blank=True)

    categ = [
        ('Petit', 'Petit (< 150m²)'),
        ('Moyen', 'Moyen (150-500m²)'),
        ('Grand', 'Grand (500m²-1000m²)'),
        ('Tres grand', 'Très grand (> 1000m²)'),
    ]

    taille = models.CharField(verbose_name='Taille',
                              choices=categ, max_length=255)
    enseigne = models.ForeignKey(
        Enseigne, on_delete=models.CASCADE, blank=True, related_name='Batiment_Enseigne')
    #localisation = models.ForeignKey('Localisation', on_delete=models.CASCADE,  related_name='Localisation_batiment', blank=True, null=True)
    #profil = models.ForeignKey('Profil', on_delete=models.CASCADE,related_name='Profil_batiment',blank=True, null=True)
    #toiture = models.ForeignKey('Toiture',  on_delete=models.CASCADE,related_name='Toiture_batiment', blank=True, null=True)
    #edf = models.ForeignKey('EDF', on_delete=models.CASCADE,related_name='edf_batiment',blank=True, null=True)

    id = models.AutoField(primary_key=True, editable=False,  blank=True)

    def __str__(self):
        return str(self.id)


class Ensolleilement(models.Model):
    territ = models.CharField(max_length=100, verbose_name='Territoire')
    h_soleil = models.FloatField(verbose_name='Heure de lever du soleil')  # h
    h_ensol = models.FloatField(
        verbose_name="Heure d'enseillement par jour (h)")  # h
    h_ensol_ref = models.FloatField(
        verbose_name="Heure d'enseillement journalier de référence (kWh/m2) ")  # kWh/m2
    PR = models.FloatField(verbose_name='PR (Entre 0 et 1)')
    Ep_moyenne = models.FloatField(
        verbose_name='Energie produite moyenne (kWh/kWc)')  # (kWh/kWc)
    Ep_favorable = models.FloatField(
        verbose_name='Energie produite jour favorable (kWh/kWc)')  # (kWh/kWc)
    Ep_defavorable = models.FloatField(
        verbose_name='Energie produite jour défavorable(kWh/kWc)')  # (kWh/kWc)

    prix_coeff_1 = models.FloatField(
        verbose_name='Coeff D 1 - Prix en c€ / kWh - 36-100 kWc', default=0)
    prix_coeff_1_1 = models.FloatField(
        verbose_name='Coeff D 1.1 - Prix en c€ / kWh - 9-36 kWc', default=0)
    prix_coeff_1_2 = models.FloatField(
        verbose_name='Coeff D 1.2 - Prix en c€ / kWh - 3-9 kWc', default=0)
    # prix_coeff_1_35 = models.FloatField(
    #     verbose_name='Coeff D 1.35 - Prix en c€ / kWh - < 3 kWc', default=0)

    def __str__(self):
        return str(self.territ)

    class Meta:
        verbose_name = "Territoire"


class Localisation(models.Model):
    territ = models.ForeignKey(
        Ensolleilement, on_delete=models.CASCADE, related_name='Territoire', blank=True)
    batiment = models.OneToOneField(
        Batiment, on_delete=models.CASCADE, related_name='Batiment_localisation', blank=True)

    adresse = models.CharField(max_length=255)

    #  def __str__(self):
    #    return self.territ


class Profil_types(models.Model):
    type_profil = models.CharField(verbose_name='Profil', max_length=255)

    # def __str__(self):
    #     list = [{k: str(v) for k, v in self.__dict__.items()}]
    #     return list[0]['type_profil']

    class Meta:
        verbose_name = "Profil Type"

    def __str__(self):
        return str(self.type_profil)


class Profil(models.Model):
    type_profil = models.ForeignKey(
        Profil_types, on_delete=models.CASCADE, blank=False)
    batiment = models.OneToOneField(
        Batiment, on_delete=models.CASCADE, related_name='batiment_profil', blank=True)

   # def __str__(self):
    # return json.dumps({k: str(v) for k, v in self.__dict__.items()})

    def __str__(self):
        return str(self.type_profil)


class Coeffs_Ouvres(models.Model):
    profil = models.ForeignKey(Profil_types, on_delete=models.CASCADE,
                               related_name='Profil_Ouvre', blank=False, null=True)
    heure = models.TimeField(null=True)
    coeff = models.FloatField(null=True)

    class Meta:
        verbose_name = "Coeffs Jour Ouvré"

    def __str__(self):
        return str(self.profil)


class Coeffs_Weekend(models.Model):
    profil = models.ForeignKey(Profil_types, on_delete=models.CASCADE,
                               related_name='Profil_Weekend', blank=False, null=True)
    heure = models.TimeField(null=True)
    coeff = models.FloatField(null=True)

    class Meta:
        verbose_name = "Coeffs Weekend"

    def __str__(self):
        return str(self.profil)


class CourbeDeCharge(models.Model):
    profil = models.ForeignKey(
        Profil_types, verbose_name='Profil', on_delete=models.CASCADE)
    types = (('Ouvré', 'Ouvré'),
             ('Weekend', 'Weekend'),)
    type = models.CharField(max_length=255, choices=types, verbose_name='Jour')

    coeff_0 = models.FloatField(verbose_name='00:00 (%)', default=20)
    coeff_1 = models.FloatField(verbose_name='01:00 (%)', default=20)
    coeff_2 = models.FloatField(verbose_name='02:00', default=20)
    coeff_3 = models.FloatField(verbose_name='03:00', default=20)
    coeff_4 = models.FloatField(verbose_name='04:00', default=20)
    coeff_5 = models.FloatField(verbose_name='05:00', default=20)
    coeff_6 = models.FloatField(verbose_name='06:00', default=20)
    coeff_7 = models.FloatField(verbose_name='07:00', default=20)
    coeff_8 = models.FloatField(verbose_name='08:00', default=20)
    coeff_9 = models.FloatField(verbose_name='09:00', default=20)
    coeff_10 = models.FloatField(verbose_name='10:00', default=20)
    coeff_11 = models.FloatField(verbose_name='11:00', default=20)
    coeff_12 = models.FloatField(verbose_name='12:00', default=20)
    coeff_13 = models.FloatField(verbose_name='13:00', default=20)
    coeff_14 = models.FloatField(verbose_name='14:00', default=20)
    coeff_15 = models.FloatField(verbose_name='15:00', default=20)
    coeff_16 = models.FloatField(verbose_name='16:00', default=20)
    coeff_17 = models.FloatField(verbose_name='17:00', default=20)
    coeff_18 = models.FloatField(verbose_name='18:00', default=20)
    coeff_19 = models.FloatField(verbose_name='19:00', default=20)
    coeff_20 = models.FloatField(verbose_name='20:00', default=20)
    coeff_21 = models.FloatField(verbose_name='21:00', default=20)
    coeff_22 = models.FloatField(verbose_name='22:00', default=20)
    coeff_23 = models.FloatField(verbose_name='23:00', default=20)

    # attribut coeffs pour récupérer la liste des coefficients (en %) de la courbe de charge
    def _coeffs(self):
        coeffs = list(model_to_dict(self).values())
        return coeffs[3:]
    coeffs = property(_coeffs)

    class Meta:
        unique_together = ('profil', 'type')

    def __str__(self):
        return str(self.profil) + ' - ' + str(self.type)


class CourbeChargePerso(models.Model):
    projet = models.ForeignKey(
        Projet, verbose_name='Projet', on_delete=models.CASCADE)
    name = models.CharField(
        max_length=255, verbose_name='Nom du profil', default='-')
    types = (('Ouvré', 'Ouvré'),
             ('Weekend', 'Weekend'),)
    type = models.CharField(max_length=255, choices=types,
                            verbose_name='Jour', default='Ouvré')

    coeff_0 = models.FloatField(verbose_name='00:00 (%)', default=19)
    coeff_1 = models.FloatField(verbose_name='01:00 (%)', default=18)
    coeff_2 = models.FloatField(verbose_name='02:00', default=18)
    coeff_3 = models.FloatField(verbose_name='03:00', default=19)
    coeff_4 = models.FloatField(verbose_name='04:00', default=18)
    coeff_5 = models.FloatField(verbose_name='05:00', default=19)
    coeff_6 = models.FloatField(verbose_name='06:00', default=27)
    coeff_7 = models.FloatField(verbose_name='07:00', default=50)
    coeff_8 = models.FloatField(verbose_name='08:00', default=71)
    coeff_9 = models.FloatField(verbose_name='09:00', default=92)
    coeff_10 = models.FloatField(verbose_name='10:00', default=100)
    coeff_11 = models.FloatField(verbose_name='11:00', default=93)
    coeff_12 = models.FloatField(verbose_name='12:00', default=87)
    coeff_13 = models.FloatField(verbose_name='13:00', default=81)
    coeff_14 = models.FloatField(verbose_name='14:00', default=83)
    coeff_15 = models.FloatField(verbose_name='15:00', default=83)
    coeff_16 = models.FloatField(verbose_name='16:00', default=69)
    coeff_17 = models.FloatField(verbose_name='17:00', default=44)
    coeff_18 = models.FloatField(verbose_name='18:00', default=25)
    coeff_19 = models.FloatField(verbose_name='19:00', default=22)
    coeff_20 = models.FloatField(verbose_name='20:00', default=20)
    coeff_21 = models.FloatField(verbose_name='21:00', default=18)
    coeff_22 = models.FloatField(verbose_name='22:00', default=18)
    coeff_23 = models.FloatField(verbose_name='23:00', default=18)

    # attribut coeffs pour récupérer la liste des coefficients (en %) de la courbe de charge
    def _coeffs(self):
        coeffs = list(model_to_dict(self).values())
        return coeffs[3:]
    coeffs = property(_coeffs)

    class Meta:
        unique_together = ('name', 'type')

    def __str__(self):
        return str(self.name) + ' - ' + str(self.type)


class ProfilPerso(models.Model):
    profil = models.ForeignKey(
        CourbeChargePerso, verbose_name='Profil personnalisé', on_delete=models.CASCADE, blank=True, null=True)
    batiment = models.ForeignKey(
        Batiment, on_delete=models.CASCADE, verbose_name='Batiment')

    def _type(self):
        t = self.profil.type
        return t
    type = property(_type)


class Toiture(models.Model):
    type = (('Terrasse', 'Terrasse'),
            ('Tôle bac acier trapézoïdal', 'Tôle bac acier trapézoïdal'),
            )

    toiture = models.CharField(
        verbose_name='Toiture', choices=type, max_length=255)
    surface = models.FloatField(
        verbose_name='Surface de toiture (m²)')

    batiment = models.OneToOneField(
        Batiment, on_delete=models.CASCADE, related_name='batiment_toiture', blank=True)

    def __str__(self):
        return self.toiture


class EDF(models.Model):
    puissance = models.FloatField(
        verbose_name='Puissance souscrite (kVA)')

    ref = (('Mensuelle', 'Mensuelle '),
           ('Bimestrielle', 'Bimestrielle '),
           ('Annuelle', 'Annuelle '))

    reference = models.CharField(
        verbose_name='Reference', choices=ref, max_length=255)

    nb_kW = models.FloatField(verbose_name='Nombre KWh facture')

    facture = models.FloatField(verbose_name='Montant facture (€)')
    batiment = models.OneToOneField(
        Batiment, on_delete=models.CASCADE, related_name='batiment_edf',  blank=True)


class Electrification(models.Model):
    instal = (('Monophasée', 'Monophasée'),
              ('Triphasée', 'Triphasée'),)
    installation = models.CharField(
        verbose_name='Installation', choices=instal, max_length=255)
    souscription = models.OneToOneField(
        EDF, on_delete=models.CASCADE, related_name='batiment_souscription', blank=True)

    # def __str__(self):
    #  return self.instal


class Mobilite(models.Model):
    vehicule_fonction = models.PositiveIntegerField(
        verbose_name='Nombre de véhicules de fonction')
    km_an_vehicule_fonction = models.PositiveIntegerField(
        verbose_name='Nombre de km/an véhicule de fonction', default=0)
    vehicule_utilitaire = models.PositiveIntegerField(
        verbose_name='Nombre de véhicules utilitaires')
    km_an_vehicule_utilitaire = models.PositiveIntegerField(
        verbose_name='Nombre de km/an véhicule utilitaires', default=0)
    choix = (('Oui', 'Oui'),
             ('Non', 'Non'))
    parking = models.CharField(
        verbose_name='Présence parking ', choices=choix, max_length=255)
    choix1 = (('Public', 'Public'),
              ('Privé', 'Privé'))
    acces = models.CharField(
        verbose_name='Accessibilité Parking', choices=choix1, max_length=255, default='Privé')
    borne = models.CharField(verbose_name='Option Borne',
                             choices=choix, max_length=255, default='Non')
    pt_de_charge = models.PositiveIntegerField(
        verbose_name='Nombre de point de charges desirés', default=0)

    batiment = models.OneToOneField(
        Batiment, on_delete=models.CASCADE, related_name='batiment_mobilite', blank=True)


# Modèles de la BDD FINANCE

class Taxe(models.Model):
    territ = models.CharField(max_length=100, verbose_name='Territoire')
    transport_1 = models.FloatField(verbose_name='Main doeuvre en %')
    transport_2 = models.FloatField(verbose_name='Panneaux en %')
    transport_3 = models.FloatField(verbose_name='Le reste en %')
    Pose_PV_toiture_tole = models.FloatField(
        verbose_name=' Pose PV toiture tôle + Raccordement < 50kWc')
    Pose_PV_toiture_tole_2 = models.FloatField(
        verbose_name='Pose PV toiture tôle + Raccordement > 50kWc')
    Pose_PV_toiture_terrasse = models.FloatField(
        verbose_name='Pose PV toiture Terrasse + Raccordement < 50kWc')
    Pose_PV_toiture_terrasse_2 = models.FloatField(
        verbose_name=' Pose PV toiture Terrasse + Raccordement > 50kWc')
    Pose_PV_toiture_tuile = models.FloatField(
        verbose_name=' Pose PV toiture Tuiles +Raccordement < 10kWc')
    Pose_PV_toiture_tuile_2 = models.FloatField(
        verbose_name=' Pose PV toiture Tuiles +Raccordement < 50kWc')
    Pose_PV_toiture_tole_3 = models.FloatField(
        verbose_name='  Pose PV toiture Tuiles +Raccordement > 50kWc')
    pose = models.FloatField(verbose_name=' Pose plot soprasolar ')
    install = models.FloatField(
        verbose_name=' Installation et mise en service borne')
    tva_entreprise = models.FloatField()
    tva_particulier = models.FloatField()

    def __str__(self):
        return self.territ


class Tailles_Standards(models.Model):
    taille = models.FloatField(verbose_name="Taille standard")

    unite = (('Centrale', 'Centrale '),
             ('Batterie', 'Batterie '))

    catag = models.CharField(verbose_name=" Type d'équipement",
                             choices=unite, max_length=255, default='Batterie')

    def __str__(self):
        return str(self.taille) + " : " + str(self.catag)


# class Catalogue_GT(models.Model):
#     toit = (('Terrasse', 'Terrasse'),
#             ('Tôle bac acier trapézoïdal', 'Tôle bac acier trapézoïdal'),
#             )

#     tailles = models.ManyToManyField(Tailles_Standards, blank=True)
#     toiture = models.CharField(
#         verbose_name="Type de toiture", choices=toit, max_length=255)

#     panneau = models.ManyToManyField(ModulesPV, blank=True)
#     fixation = models.ManyToManyField(Structure,  blank=True)
#     onduleurs = models.ManyToManyField(Onduleurs,  blank=True)
#     monitoring = models.ManyToManyField(Monitoring,  blank=True)
#     batteries = models.ManyToManyField(Batteries, blank=True)
#     extensions_batteries = models.ManyToManyField(
#         Extensions_Batteries, blank=True)
#     cables = models.ManyToManyField(Cables, blank=True)
#     tableaux = models.ManyToManyField(Tableaux, blank=True)
#     cheminement = models.ManyToManyField(Cheminement, blank=True)
#     divers = models.ManyToManyField(Divers, blank=True)
#     main_doeuvre = models.ManyToManyField(Main_doeuvre, blank=True)

#     marge = models.FloatField(verbose_name="Marge sur le projet (en %)")

#     def __str__(self):
#         rqt0 = self.tailles.all()
#         rqt1 = rqt0.values_list('taille', 'catag')
#         value = np.array(rqt1).flatten().tolist()
#         return str(value) + " : " + str(self.toiture)


class FacturationItem(models.Model):
    type = models.CharField(max_length=255, verbose_name="Type d'équipement")

    article = models.CharField(max_length=255, verbose_name='Article')

    cout_HA_unit = models.FloatField(
        verbose_name='Coût HA unitaire')

    taux_transport = models.FloatField(
        verbose_name='Taux transport en % du prix HA')

    unites = (('Unité', 'Unité'),
              ('/ Wc', '/ Wc'),
              ('/ ml', '/ ml'),)

    unite = models.CharField(
        max_length=255, choices=unites, verbose_name='Unité', default='Unité')

    class Meta:
        verbose_name = 'Equipement'

    def __str__(self):
        return str(self.article)


# catalogue de MZ - 01/04/2022
class CatalogueSolution(models.Model):
    taille = models.FloatField(verbose_name='Taille en kWc')
    instal = (('Monophasée', 'Monophasée'),
              ('Triphasée', 'Triphasée'),)
    installation = models.CharField(
        verbose_name='Installation', choices=instal, max_length=255)
    marge = models.FloatField(verbose_name='marge en %')

    elements = models.ManyToManyField(
        FacturationItem, through='ItemQuantite')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['taille', 'installation'], name="solutions uniques")
        ]

    class Meta:
        verbose_name = 'Catalogue - Solution'

    def __str__(self):
        return str(self.taille)+' kWc - '+str(self.installation)


class ItemQuantite(models.Model):
    catalogue_solution = models.ForeignKey(
        CatalogueSolution, on_delete=models.CASCADE, verbose_name='Solution')
    facturation_item = models.ForeignKey(
        FacturationItem, on_delete=models.CASCADE, verbose_name='Elément')

    quantite = models.IntegerField(default=0, verbose_name='Quantité')

    # # # # # # # # # # #
    # Calculés

    def _cout_HA_unit(self):
        cout = self.facturation_item.cout_HA_unit
        return round(cout, 2)
    cout_HA_unit = property(_cout_HA_unit)

    def _cout_transport_unit(self):
        taux = self.facturation_item.taux_transport/100
        cout = taux*self.facturation_item.cout_HA_unit
        return round(cout, 2)
    cout_transport_unit = property(_cout_transport_unit)

    def _cout_HA(self):
        cout = self.facturation_item.cout_HA_unit*self.quantite
        return round(cout, 2)
    cout_HA = property(_cout_HA)

    def _cout_transport(self):
        taux = self.facturation_item.taux_transport/100
        cout_transport_unit = taux*self.facturation_item.cout_HA_unit
        cout = cout_transport_unit*self.quantite
        return round(cout, 2)
    cout_transport = property(_cout_transport)

    def _prix_unit(self):
        taux = self.facturation_item.taux_transport/100
        cout_transport_unit = taux*self.facturation_item.cout_HA_unit
        marge = self.catalogue_solution.marge/100
        prix = self.facturation_item.cout_HA_unit*(1+marge)+cout_transport_unit
        return round(prix, 2)
    prix_unit = property(_prix_unit)

    def _prix(self):
        marge = self.catalogue_solution.marge/100
        cout_HA = self.facturation_item.cout_HA_unit*self.quantite
        taux = self.facturation_item.taux_transport/100
        cout_transport_unit = taux*self.facturation_item.cout_HA_unit
        cout_transport = cout_transport_unit*self.quantite
        prix = cout_HA*(1+marge)+cout_transport
        return round(prix, 2)
    prix = property(_prix)

    def _marge(self):
        marge = self.catalogue_solution.marge/100
        cout_HA = self.facturation_item.cout_HA_unit*self.quantite
        return round(cout_HA*marge, 2)
    marge = property(_marge)

    # Calculés
    # # # # # # # # # # #

    # class Meta:
    #     unique_together = ('catalogue_solution', 'facturation_item')

    class Meta:
        verbose_name = 'Catalogue - Entrée'

    def __str__(self):
        return str(self.facturation_item)


class CentraleBatiment(models.Model):
    batiment = models.ForeignKey(Batiment, on_delete=models.CASCADE)


class SolutionBatiment(models.Model):
    centrale_batiment = models.ForeignKey(
        CentraleBatiment, on_delete=models.CASCADE)
    solution = models.ForeignKey(CatalogueSolution, on_delete=models.CASCADE)


# class ItemQuantiteBatiment(models.Model):

#     def __str__(self):
#         return self.item


class Modules_factu(models.Model):
    module = models.CharField(max_length=255)
    batiment = models.ForeignKey(Batiment,  on_delete=models.CASCADE)

    qt = models.PositiveIntegerField(verbose_name='Quantité')
    cout_unitaire = models.FloatField(
        verbose_name='Coût HA unitaire')
    cout_unitaire_transport = models.FloatField(
        verbose_name='Coût Unitaire Transport', blank=True)
    cout_total = models.FloatField(verbose_name='Coût Total HA')
    cout_total_transport = models.FloatField(
        verbose_name='Coût Total Transport',  blank=True)
    marge = models.FloatField()
    prix = models.FloatField(verbose_name='Prix Vendu')
    prix_unitaire = models.FloatField(verbose_name='Prix Unitaire')

    def fields(self):
        l = list(model_to_dict(self).values())
        l.pop(0)
        l.pop(1)
        l.pop(1)
        for i in range(len(l)):
            if type(l[i]) not in [int, str]:
                l[i] = round(l[i], 2)
        return l


# class Info_facturation(models.Model):
#     client = models.ForeignKey(Client,  on_delete=models.CASCADE)
#     batiment = models.ForeignKey(Batiment,  on_delete=models.CASCADE)

#     qt = models.PositiveIntegerField(verbose_name='Quantité')
#     cout_unitaire = models.FloatField(
#         verbose_name='Coût HA unitaire')
#     cout_unitaire_transport = models.FloatField(
#         verbose_name='Coût Unitaire Transport', blank=True)
#     cout_total = models.FloatField(verbose_name='Coût Total HA')
#     cout_total_transport = models.FloatField(
#         verbose_name='Coût Total Transport', blank=True)
#     marge = models.FloatField()
#     prix = models.FloatField(verbose_name='Prix Vendu')
#     prix_unitaire = models.FloatField(verbose_name='Prix Unitaire')

#     class Meta:
#         abstract = True


# Modèles de la BDD ETUDES

class BDDBat(models.Model):
    type = models.CharField(
        max_length=100, verbose_name="Secteurs d'activité proposés par SEIZE (utilisé)")
    moy_kWh_avant = models.FloatField(
        verbose_name="Moyenne par Secteur (kWh/an/m²) AVANT AUDIT ")
    moy_kWh_apres = models.FloatField(
        verbose_name="Moyenne par Secteur (kWh/an/m²) APRES AUDIT")
    moy_euros_avant = models.FloatField(
        verbose_name="Moyenne par Secteur (€/an/m²) AVANT AUDIT ")
    moy_euros_apres = models.FloatField(
        verbose_name="Moyenne par Secteur (€/an/m²) APRES AUDIT")
    cout_kWh_avant = models.FloatField(
        verbose_name="Coût du kWh moyen avant audit")
    cout_kWh_apres = models.FloatField(
        verbose_name="Coût du kWh moyen après audit", blank=True, null=True)
    gain = models.FloatField(
        verbose_name="Gain atteingable dans le secteur", blank=True, null=True)

    def __str__(self):
        return self.type


class Emisission_CO2(models.Model):
    territ = models.CharField(max_length=100, verbose_name="Territoire")
    emission = models.FloatField(
        verbose_name="Hypothèses Emissions CO2 en kg CO2/kWh	")


class Hyp_cout_mobilite(models.Model):
    model = models.CharField(max_length=1000, verbose_name="Produit")
    valeur = models.FloatField(verbose_name="Valeur")
    unite = models.CharField(max_length=100, verbose_name="Unité")

    class Meta:
        verbose_name = "Coût Mobilité"


class EZ_DRIVE(models.Model):
    model = models.CharField(max_length=1000, verbose_name="Produit")
    valeur = models.FloatField(verbose_name="Valeur")
    unite = models.CharField(max_length=100, verbose_name="Unité")
    invest = models.FloatField(
        verbose_name="Investissement initial en €", blank=True, null=True)
