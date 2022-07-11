import numpy as np
from .Input import Load_Input
from .models import *
from .models import CourbeDeCharge

# Variables statiques
Load_Input()

Rendement_batteries_Lithium = 0.95
Decharge_maximale_batteries_Lithium = 0.8
Perte1 = 0.05  # %
Nb_jours_ouvres = 261


# Profil personnalisé
# Profil Mesuré
# Dimensonnement
def courbes_de_charges_coeff(profil):
    # Profil est un modèle de type Profil_types, on peut recuperer directement les paramètres.
    global coeffs_ouvre
    global coeffs_weekend

    coeffs_ouvre = CourbeDeCharge.objects.get(
        profil=profil, type="Ouvré").coeffs

    coeffs_weekend = CourbeDeCharge.objects.get(
        profil=profil, type="Weekend").coeffs

    a = np.matrix(coeffs_ouvre).flatten()
    a = a.transpose()
    b = np.matrix(coeffs_weekend).flatten()
    b = b.transpose()

    return a, b


def consommation(profil):
    # Consommation hebdo en fonction des coeffs de courbes de charges moyenne
    # Conso en kWh
    global conso

    coeff_ouvre, coeff_weekend = courbes_de_charges_coeff(profil)
    total_ouvre = np.sum(coeff_ouvre)
    total_weekend = np.sum(coeff_weekend)

    conso = 5*total_ouvre+2*total_weekend

    return conso

 # conso perso : consommation du client en une semaine
 # conso_hebdo : consommation moyenne en une semaine pour le même type de profil


def courbe_de_charges(conso_perso, profil):
    # conso perso en une semaine
    conso_hebdo = consommation(profil)
    coeffs_ouvre, coeffs_weekend = courbes_de_charges_coeff(profil)

    coeffs_ouvre = 1000 * (conso_perso / conso_hebdo) * coeffs_ouvre
    coeffs_weekend = 1000 * (conso_perso / conso_hebdo) * coeffs_weekend

    return coeffs_ouvre, coeffs_weekend


def courbe_irradiation(territ):
    # Recuperation des infos du soleil lié au territoire

    hL = territ.h_soleil  # h

    So = territ.h_ensol  # h
    H_soleil = territ.h_ensol_ref   # kWh/m2
    Ep_moyenne = territ.Ep_moyenne  # kWh/kWc
    Ep_defavorable = territ.Ep_defavorable  # kWh/kWc
    Ep_favorable = territ.Ep_favorable   # kWh/kWc
    i = 0
    global l
    l = np.zeros((24, 4), float)
    for i in range(23):
        x = min(max(np.pi*(i+1-hL)/So, 0), np.pi)  # pi*(h-hL/So)
        # print(x)
        y = (np.sin(x)*np.pi)/(2*(So/24)*24)  # sin*pi/2*So
        # print(y)
        z = y*H_soleil*1000*Ep_moyenne/4.35  # G
        # print(z)
        i += 1
        l[i][0] = i
        l[i][1] = x
        l[i][2] = y
        l[i][3] = z

    return l


def pic_production(territ):
    PR = territ.PR
    pic = max(courbe_irradiation(territ).max(axis=1))*PR/1000
    return pic  # en kWc


# conso en hebdo
def dimensionnement_potentiel_centrale_autoconso(conso_perso, profil, territ):

    ouvre = courbe_de_charges(conso_perso, profil)[0]

    extract_ouvre = ouvre[10:15]
    total_extract_ouvre = np.sum(ouvre)
    # print(total_extract_ouvre)
    min_extract_ouvre = np.min(extract_ouvre)

    weekend = courbe_de_charges(conso_perso, profil)[1]
    extract_weekend = weekend[10:15]
    total_extract_weekend = np.sum(weekend)
    # print(total_extract_weekend)

    min_extract_weekend = np.min(extract_weekend)

    value = (min_extract_ouvre * total_extract_ouvre * 5 / conso_perso + min_extract_weekend *
             total_extract_weekend * 2 / conso_perso) / 1000 / 1000 / pic_production(territ)

    return value
    # resultat en kWc


def calcul_taux_centrale_potentiel(conso_perso, profil, territ):  # conso en hebdo
    centrale_potentielle = dimensionnement_potentiel_centrale_autoconso(
        conso_perso, profil, territ)
    coeffs_ouvre = courbe_de_charges(conso_perso, profil)[0]
    coeffs_weekend = courbe_de_charges(conso_perso, profil)[1]

    Ep_moyenne = territ.Ep_moyenne  # kWh/kWc
    Ep_defavorable = territ.Ep_defavorable  # kWh/kWc
    Ep_favorable = territ.Ep_favorable  # kWh/kWc
    PR = territ.PR

    Nb_jours_favorables = 365 * \
        ((Ep_moyenne - Ep_defavorable) / (Ep_favorable - Ep_defavorable))

    G = courbe_irradiation(territ)
    tab = np.zeros((24, 8), float)

    for i in range(23):
        tab[i][0] = i  # Heures
        # Energie produite moyenne (W)
        tab[i][1] = G[i][3] * PR * centrale_potentielle
        tab[i][2] = tab[i][1] * Ep_defavorable / \
            Ep_moyenne  # Energie produite jour nuageux (Wh)
        # Energie produite jour ensoleillé  (Wh)
        tab[i][3] = tab[i][1] * Ep_favorable / Ep_moyenne
        # Surplus jour ouvré nuageux  (Wh)
        tab[i][4] = max(tab[i][2] - coeffs_ouvre[i], 0)
        # Surplus jour ouvré ensoleillé  (Wh)
        tab[i][5] = max(tab[i][3] - coeffs_ouvre[i], 0)
        # Surplus weekend nuageux  (Wh)
        tab[i][6] = max(tab[i][2] - coeffs_weekend[i], 0)
        # Surplus weekend ensoleillé  (Wh)
        tab[i][7] = max(tab[i][3] - coeffs_weekend[i], 0)

    charge_ouvre_jour = np.sum(coeffs_ouvre)
    charge_weekend_jour = np.sum(coeffs_weekend)

    surplus_ouvre_nuageux_annuel = np.sum(
        tab[:, 4]) * (365 - Nb_jours_favorables) * Nb_jours_ouvres / 365
    surplus_ouvre_ensoleille_annuel = np.sum(
        tab[:, 5]) * Nb_jours_favorables * Nb_jours_ouvres / 365
    surplus_weekend_nuageux_annuel = np.sum(
        tab[:, 6]) * (365 - Nb_jours_favorables) * (365 - Nb_jours_ouvres) / 365
    surplus_weekend_ensoleille_annuel = np.sum(
        tab[:, 7]) * (365 - Nb_jours_ouvres) * Nb_jours_favorables / 365

    centrale_autoprod = ((charge_ouvre_jour*charge_ouvre_jour*5)/conso_perso/1000)+(
        (charge_weekend_jour*charge_weekend_jour*2)/conso_perso/1000)/1000/Ep_moyenne
    centrale_entre_deux = (centrale_potentielle+centrale_autoprod)/2
    batterie = (surplus_ouvre_nuageux_annuel+surplus_ouvre_ensoleille_annuel +
                surplus_weekend_nuageux_annuel+surplus_weekend_ensoleille_annuel)/365

    return batterie, centrale_autoprod, centrale_entre_deux
