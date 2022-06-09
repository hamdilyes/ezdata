# TABLEAU DES SOLUTIONS TRIPHASEES avec une ligne en plus = capacité de batterie // Mettre 0 pour les 4 premières colonnes
# Aller recuperer le numero de solution de la base de données SQL pour remplir le tableau de solution
from django.db import models
from .models import (BDD, ModulesPV, Emisission_CO2)
from .MDE import Coeffs_mde, Variables_mde
from .Input import Load_Input

#import matplotlib.pyplot as plt

import numpy as np

from .dimens_centrale import dimensionnement_potentiel_centrale_autoconso, courbe_de_charges, courbe_irradiation, calcul_taux_centrale_potentiel
from operator import itemgetter

# Variables statiques
Load_Input()

# Hypthèses
Rendement_batteries_Lithium = 0.95
Decharge_maximale_batteries_Lithium = 0.8
Perte1 = 0.05  # %
Nb_jours_ouvres = 261


def tableau_solutions(panneau, installation):

    panneau_requete = ModulesPV.objects.get(Nom=panneau)
    surface_panneau = panneau_requete.Surface_Panneau_m2
    puissance_panneau = panneau_requete.Puissance_modulaire_kW

    tab = np.zeros((38, 17), float)
    # REMPLISSAGE DU TABLEAU a la main des premieres valeurs : nb de modules / ligne des sans batterie
    Capacite_Batterie = 2.4  # kWh
    tab[1][0] = 10
    tab[2][0] = 18
    tab[3][0] = 20
    tab[4][0] = 22
    tab[5][0] = 26
    tab[6][0] = 30
    tab[7][0] = 34
    tab[8][0] = 38
    tab[9][0] = 42
    tab[10][0] = 46
    tab[11][0] = 50
    tab[12][0] = 58
    tab[13][0] = 66
    tab[14][0] = 76
    tab[15][0] = 86
    tab[16][0] = 96
    tab[17][0] = 104
    tab[18][0] = 114
    tab[19][0] = 128
    tab[20][0] = 144
    tab[21][0] = 158
    tab[22][0] = 172
    tab[23][0] = 186
    tab[24][0] = 202
    tab[25][0] = 216
    tab[26][0] = 230
    tab[27][0] = 244
    tab[28][0] = 260
    tab[29][0] = 274
    tab[30][0] = 288
    tab[31][0] = 318
    tab[32][0] = 346
    tab[33][0] = 376
    tab[34][0] = 404
    tab[35][0] = 434
    tab[36][0] = 462
    tab[37][0] = 478

    # Capacités Batteries

    for i in range(1, 38):
        for j in range(1, 17):

            if j == 1:
                tab[i][j] = (tab[i][0]) * surface_panneau

            if j == 2:
                tab[i][j] = (tab[i][0]) * puissance_panneau

            # Pour Batterie = 0 kWh

            if j == 3:

                result = BDD.objects.filter(Electrical_installation=installation).filter(
                    Nb_modules_min__lt=float(tab[i][0])).filter(Puissance_centrale_max__gt=float(tab[i][2]))
                #results = list()
                # for r in result :
                #results.append((r.N, r.Prix_total_achat))

                # Prendre le numero de solution pour le prix d'achat le plus petit :
                if result.exists():
                    #t = min(result, key=result.get)
                    Final = result.order_by('Prix_total_achat')[0]
                    t = Final.N
                    # t = min(result, key=lambda t: t[1])
                    tab[i][3] = t
                else:
                    # prendre en compte les fois ou il n'y a pas de solutions
                    tab[i][3] = 0

            # Pour Batteries
            if j >= 4:
                tab[0][j] = j*Capacite_Batterie
                result = BDD.objects.filter(Electrical_installation=installation).filter(Nb_modules_min__lte=float(
                    tab[i][0])).filter(Puissance_centrale_max__gte=float(tab[i][2])).filter(Capacit_batterie=tab[0][j])

                # Prendre le numero de solution pour le prix d'achat le plus petit :
                if result.exists():
                    # t = min(result, key=result.get)
                    Final = result.order_by('Prix_total_achat')[0]
                    t = Final.N
                    # t = min(result, key=lambda t: t[1])
                    tab[i][j] = t
                else:
                    # prendre en compte les fois ou il n'y a pas de solutions
                    tab[i][j] = 0
    return tab


def solution(panneau, conso_perso, profil, territ, surface, installation, puissance, batteries, centrale_autoprod, centrale_entrelesdeux):

    # Choix du type de centrale :
    if centrale_autoprod == True:
        potentiel = calcul_taux_centrale_potentiel(
            conso_perso, profil, territ)[1]

    if centrale_entrelesdeux == True:
        potentiel = calcul_taux_centrale_potentiel(
            conso_perso, profil, territ)[2]

    else:
        potentiel = dimensionnement_potentiel_centrale_autoconso(
            conso_perso, profil, territ)

    if batteries == True:
        batterie_potentielle = (calcul_taux_centrale_potentiel(
            conso_perso, profil, territ)[0])/1000
    else:
        batterie_potentielle = 0

    tab = tableau_solutions(panneau, installation)
    tab2 = np.zeros((38, 15), float)
    tab2[0][0] = 0
    tab2[0][1] = 0

    # Remplir les tailles de batteries possible en fonction des calculs effectués précedemment
    for i in range(4, 17):
        tab2[0][i-2] = tab[0][i]

    # Prendre en compte le cas ou pas de puissance souscrite = pas de facture EDF
    # if puissance = 0 :
    # puissance = 1000  # VA

    for i in range(1, 38):
        for j in range(3, 17):
            # print(i)
            tab2[i][0] = tab[i][2]
            if (np.any(tab[i][j] > 0)):
                if (np.any(tab[i][1] <= surface)):
                    if (np.any(tab[i][2] <= puissance + 1)):
                        if (batterie_potentielle > 0):
                            if (np.any(tab2[0][j-2]) > 0):
                                tab2[i][j-2] = 1 - ((abs(potentiel - tab[i][2]) / max(potentiel, tab[i][2]) / 2)+(
                                    abs(batterie_potentielle - tab[0][j])/max(batterie_potentielle, tab[0][j]) / 2))
                        if (batterie_potentielle == 0):
                            if (np.any(tab2[0][j-2]) == 0):
                                tab2[i][j - 2] = 1 - \
                                    (abs(potentiel - tab[i][2]) /
                                     max(potentiel, tab[i][2]) / 2)

            else:
                tab2[i][j-2] = -1

    # Tableau sur lequel faire les recherches d'atteinte potentiel
    # ON enleve les tailles de centrales + batteries car risquerait de fausser le resultat de la recherche de maximum

    extract = tab2[1:39, 1:16]

    result = np.where(extract == np.amax(extract))

    ligne = result[0][0]
    colonne = result[1][0]

    # Taille de la centrale envisageable
    atteinte_potentiel = extract[ligne][colonne]

    if atteinte_potentiel == -1:
        print("Aucune solution")

    if atteinte_potentiel == 0:
        print("Aucune solution")

    # Taille de la batterie envisageable
    batterie = tab2[0][colonne+1]

    # retourne la centrale GT + le numero de la solution + la taille de la batterie
    taille_centrale = tab2[ligne+1][0]
    numero_solution = tab[ligne+1][colonne+3]
    batterie = tab2[0][colonne + 1]

    return taille_centrale, numero_solution, batterie


def solution_GT(panneau, conso_perso, profil, territ, surface, installation, puissance, batteries, centrale_autoprod,
                centrale_entrelesdeux):

    panneau_requete = ModulesPV.objects.get(Nom=panneau)
    surface_panneau = panneau_requete.Surface_Panneau_m2
    puissance_panneau = panneau_requete.Puissance_modulaire_kW

    centrale_GT = solution(panneau, conso_perso, profil, territ, surface, installation, puissance, batteries, centrale_autoprod,
                           centrale_entrelesdeux)[0]
    numero_solution = solution(panneau, conso_perso, profil, territ, surface, installation, puissance, batteries, centrale_autoprod,
                               centrale_entrelesdeux)[1]
    batterie = solution(panneau, conso_perso, profil, territ, surface, installation, puissance, batteries, centrale_autoprod,
                        centrale_entrelesdeux)[2]

    nbr_modules = centrale_GT / puissance_panneau
    surface_toiture = surface_panneau * nbr_modules

    # rep = "La taille de la centrale proposé par GT est de " + str(centrale_GT) + "kWc. Elle est composé de " + str(
    #   nbr_modules) + " modules. Pour une surface totale de " + str(
    #   surface_toiture) + " m2.     Cela correspond à la solution " + str(numero_solution)
    rep = [centrale_GT, nbr_modules, surface_toiture, numero_solution, batterie]
    return rep

# Création du tableau issu de la feuille Analyse de Production


def calcul_taux_centraleGT(panneau, conso_perso, profil, territ, surface, installation, puissance, batteries, centrale_autoprod,
                           centrale_entrelesdeux):

    centrale_GT = solution(panneau, conso_perso, profil, territ, surface, installation, puissance, batteries, centrale_autoprod,
                           centrale_entrelesdeux)[0]

    # ATTENTION
    # Batterie en kWh dans les params

    if batteries == True:
        Batterie = solution(panneau, conso_perso, profil, territ, surface, installation, puissance, batteries, centrale_autoprod,
                            centrale_entrelesdeux)[2]*1000
        Decharge = (Batterie/2.4)*1.2

    else:
        Batterie = 0
        Decharge = 0

    tab = np.zeros((24, 20), float)

    G = courbe_irradiation(territ)

    Ep_moyenne = territ.Ep_moyenne  # kWh/kWc
    Ep_defavorable = territ.Ep_defavorable  # kWh/kWc
    Ep_favorable = territ.Ep_favorable  # kWh/kWc
    PR = territ.PR

    Nb_jours_favorables = 365 * \
        (Ep_moyenne-Ep_defavorable) / (Ep_favorable - Ep_defavorable)
    coeffs_ouvre = courbe_de_charges(conso_perso, profil)[0]
    coeffs_weekend = courbe_de_charges(conso_perso, profil)[1]

    for i in range(24):
        tab[i][0] = i  # Heures
        tab[i][1] = G[i][3] * PR * centrale_GT  # Energie produite moyenne (W)
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

        # Calculs de taux /jours qui seront utilisées pour les prochaines colonnes
    charge_ouvre_jour = np.sum(coeffs_ouvre)
    charge_weekend_jour = np.sum(coeffs_weekend)
    ep_nuageux_jour = np.sum(tab[:, 2])
    ep_soleil_jour = np.sum(tab[:, 3])
    surplus_ouvre_nuageux_jour = np.sum(tab[:, 4])
    surplus_ouvre_ensoleille_jour = np.sum(tab[:, 5])
    surplus_weekend_nuageux_jour = np.sum(tab[:, 6])
    surplus_weekend_ensoleille_jour = np.sum(tab[:, 7])

    for i in range(24):
        if (tab[i][4]) > 0:
            # Stockage batterie jour ouvré nuageux  (Wh)
            tab[i][8] = min(Batterie*Decharge_maximale_batteries_Lithium-np.sum(tab[0:i, 8]), tab[i][4]*Rendement_batteries_Lithium,
                            charge_ouvre_jour-ep_nuageux_jour+surplus_ouvre_nuageux_jour-np.sum(tab[0:i, 8]))

        if (tab[i][8]) < 0:
            tab[i][8] = 0

    stockage_ouvre_nuageux_jour = np.sum(tab[:, 8])

    for i in range(24):
        if((tab[i][5]) > 0):
            # Stockage batterie jour ouvré ensolleilé  (Wh)
            tab[i][9] = min(Batterie*Decharge_maximale_batteries_Lithium-np.sum(tab[0:i, 9]), tab[i][5]*Rendement_batteries_Lithium,
                            charge_ouvre_jour-ep_soleil_jour+surplus_ouvre_ensoleille_jour-np.sum(tab[0:i, 9]))

        if (tab[i][9]) < 0:
            tab[i][9] = 0

    stockage_ouvre_soleil_jour = np.sum(tab[:, 9])

    for i in range(24):
        if (tab[i][6]) > 0:
            # Stockage batterie weekend nuageux  (Wh)
            tab[i][10] = min(Batterie * Decharge_maximale_batteries_Lithium-np.sum(tab[0:i, 10]), tab[i][6] * Rendement_batteries_Lithium,
                             charge_weekend_jour - ep_nuageux_jour + surplus_weekend_nuageux_jour-np.sum(tab[0:i, 10]))

        if (tab[i][10]) < 0:
            tab[i][10] = 0

    stockage_weekend_nuageux_jour = np.sum(tab[:, 10])

    for i in range(24):
        if (tab[i][7]) > 0:
            # Stockage batterie weekend ensolleilé  (Wh)
            tab[i][11] = min(Batterie * Decharge_maximale_batteries_Lithium, tab[i][7] * Rendement_batteries_Lithium,
                             charge_weekend_jour - ep_soleil_jour + surplus_weekend_ensoleille_jour-np.sum(tab[0:i, 11]))

        if (tab[i][11]) < 0:
            tab[i][11] = 0

    stockage_weekend_ensolleile_jour = np.sum(tab[:, 11])

    for i in range(13, 24):
        # Energie fournie batterie jour ouvré nuageux (Wh)
        tab[i][12] = min(max(coeffs_ouvre[i]-tab[i][2], 0), Decharge,
                         stockage_ouvre_nuageux_jour - np.sum(tab[12:i, 12]))

        # Energie fournie batterie jour ouvré ensolleilé (Wh)
        tab[i][13] = min(max(coeffs_ouvre[i]-tab[i][3], 0), Decharge,
                         stockage_ouvre_soleil_jour - np.sum(tab[12:i, 13]))

        # Energie fournie batterie weekend nuageux (Wh)
        tab[i][14] = min(max(coeffs_weekend[i]-tab[i][2], 0), Decharge,
                         stockage_weekend_nuageux_jour - np.sum(tab[12:i, 14]))

        # Energie fournie batterie weekend ensolleilé nuageux (Wh)
        tab[i][15] = min(max(coeffs_weekend[i]-tab[i][5], 0), Decharge,
                         stockage_weekend_ensolleile_jour - np.sum(tab[12:i, 15]))

    for i in range(0, 12):
        tab[i][12] = min(max(coeffs_ouvre[i]-tab[i][2], 0), Decharge,
                         stockage_ouvre_nuageux_jour - np.sum(tab[0:i, 12]) - np.sum(tab[12:24, 12]))
        tab[i][13] = min(max(coeffs_ouvre[i]-tab[i][3], 0), Decharge,
                         stockage_ouvre_soleil_jour - np.sum(tab[0:i, 13]) - np.sum(tab[12:24, 13]))
        tab[i][14] = min(max(coeffs_weekend[i]-tab[i][2], 0), Decharge,
                         stockage_weekend_nuageux_jour - np.sum(tab[0:i, 14]) - np.sum(tab[12:24, 14]))
        tab[i][15] = min(max(coeffs_weekend[i]-tab[i][5], 0), Decharge,
                         stockage_weekend_ensolleile_jour - np.sum(tab[0:i, 15]) - np.sum(tab[12:24, 15]))

        ########################################

    # Taux final Annuel : totaux

    # ep = Energie produite

    ep_nuageux_annuel = np.sum(tab[:, 2]) * (365 - Nb_jours_favorables)
    ep_soleil_annuel = np.sum(tab[:, 3]) * (Nb_jours_favorables)
    surplus_ouvre_nuageux_annuel = np.sum(
        tab[:, 4]) * (365 - Nb_jours_favorables) * Nb_jours_ouvres / 365
    surplus_ouvre_ensoleille_annuel = np.sum(
        tab[:, 5]) * Nb_jours_favorables * Nb_jours_ouvres / 365
    surplus_weekend_nuageux_annuel = np.sum(
        tab[:, 6]) * (365 - Nb_jours_favorables) * (365 - Nb_jours_ouvres) / 365
    surplus_weekend_ensoleille_annuel = np.sum(
        tab[:, 7]) * (365 - Nb_jours_ouvres) * Nb_jours_favorables / 365

    # eb = energie batterie

    eb_ouvre_nuageux_annuel = np.sum(
        tab[:, 12]) * Nb_jours_ouvres * (365 - Nb_jours_favorables)/365
    eb_ouvre_soleil_annuel = np.sum(
        tab[:, 13]) * Nb_jours_favorables * Nb_jours_ouvres / 365
    eb_weekend_nuageux_annuel = np.sum(
        tab[:, 14]) * (365 - Nb_jours_favorables) * (365 - Nb_jours_ouvres) / 365
    eb_weekend_soleil_annuel = np.sum(
        tab[:, 15]) * (365 - Nb_jours_ouvres) * Nb_jours_favorables / 365

    sum_charge_ouvre = np.sum(coeffs_ouvre) * Nb_jours_ouvres
    sum_charge_weekend = np.sum(coeffs_weekend) * (365 - Nb_jours_ouvres)

    taux_autoconso = (ep_nuageux_annuel + ep_soleil_annuel - surplus_ouvre_nuageux_annuel - surplus_ouvre_ensoleille_annuel - surplus_weekend_nuageux_annuel - surplus_weekend_ensoleille_annuel) / (
        ep_nuageux_annuel + ep_soleil_annuel) * 100

    taux_autoprod = (ep_nuageux_annuel + ep_soleil_annuel) / (
        sum_charge_ouvre + sum_charge_weekend) * 100

    taux_autoconso_batterie = (ep_nuageux_annuel + ep_soleil_annuel - surplus_ouvre_nuageux_annuel - surplus_ouvre_ensoleille_annuel - surplus_weekend_nuageux_annuel - surplus_weekend_ensoleille_annuel
                               + eb_ouvre_nuageux_annuel+eb_ouvre_soleil_annuel+eb_weekend_nuageux_annuel+eb_weekend_soleil_annuel)/(ep_nuageux_annuel + ep_soleil_annuel) * 100

    taux_autoprod_batterie = taux_autoprod

    # HYPER IMPORTANT pour les économies
    energie_autoconsommee = (ep_nuageux_annuel + ep_soleil_annuel - surplus_ouvre_nuageux_annuel - surplus_ouvre_ensoleille_annuel - surplus_weekend_nuageux_annuel - surplus_weekend_ensoleille_annuel
                             + eb_ouvre_nuageux_annuel+eb_ouvre_soleil_annuel+eb_weekend_nuageux_annuel+eb_weekend_soleil_annuel) / 1000  # unité ?

    return (tab, taux_autoconso_batterie, taux_autoprod_batterie, energie_autoconsommee)


# A la fin on retourne : taux_autoconso de la centrale + taux_autoprod
# return surplus_ouvre_ensoleille_annuel

def Economies_pv(panneau, conso_perso, profil, territ, surface, installation, puissance, NbrekWhfacture, Recurrencefacture, Montantfacture, Nbreetages, type, batteries, centrale_autoprod,
                 centrale_entrelesdeux):

    #coeff_ouvre = courbe_de_charges(conso_perso, profil)[0]
   # coeff_weekend = courbe_de_charges(conso_perso, profil)[1]
    # energie_autoconsome= calcul_taux_centraleGT(panneau, conso_perso, profil, territ, surface,installation, puissance, batteries, centrale_autoprod,
    # centrale_entrelesdeux)[3]

    #sum_coeff_ouvre = np.sum(coeff_ouvre)*Nb_jours_ouvres
   # sum_coeff_weekend= np.sum(coeff_weekend)*(365-Nb_jours_ouvres)

    # Prendre les mêmes variables que pour la MDE pour avoir de la cohérence !
    NbrekWhannuel = Variables_mde(
        NbrekWhfacture, Recurrencefacture, Montantfacture, surface, Nbreetages)[2]

    energie_autoconsome = calcul_taux_centraleGT(panneau, conso_perso, profil, territ, surface, installation, puissance, batteries,
                                                 centrale_autoprod, centrale_entrelesdeux)[3]

    ancienne_conso = [NbrekWhannuel] * 20

    pv_autoconsomme = [0] * 20
    conso_reduite = [0] * 20

    for i in range(20):
        coeff = 0.995  # A REVOIR !
        pv_autoconsomme[i] = coeff**i*energie_autoconsome
        conso_reduite[i] = ancienne_conso[i] - pv_autoconsomme[i]

    tab_prix_elec = Coeffs_mde(
        NbrekWhfacture, Recurrencefacture, Montantfacture, surface, Nbreetages, type)[2]

    difference = [0] * 20
    for i in range(20):
        difference[i] = (ancienne_conso[i] -
                         conso_reduite[i]) * tab_prix_elec[i]

    Inaction = [0] * 20
    for i in range(20):
        Inaction[i] = round(ancienne_conso[i] * tab_prix_elec[i], 2)

    Bilan_Economique = [0] * 3
    Bilan_Economique[0] = round(difference[0], 2)
    Bilan_Economique[1] = 0

    for k in range(10):
        Bilan_Economique[1] += difference[k]
    Bilan_Economique[1] = round(Bilan_Economique[1], 2)
    Bilan_Economique[2] = round(sum(difference), 2)

    Bilan_Energétique = [0] * 3
    Bilan_Energétique[0] = ancienne_conso[0] - conso_reduite[0]
    Bilan_Energétique[1] = Bilan_Energétique[0] * 10
    Bilan_Energétique[2] = Bilan_Energétique[0] * 20

    # A aller chercher dans INPUT et dépend du territoire
    rqt = Emisission_CO2.objects.get(territ=territ)
    hyp_emissions_CO2 = rqt.emission

    Bilan_Environnemental = [0] * 3
    Bilan_Environnemental[0] = Bilan_Energétique[0] * hyp_emissions_CO2
    Bilan_Environnemental[1] = Bilan_Energétique[1] * hyp_emissions_CO2
    Bilan_Environnemental[2] = Bilan_Energétique[2] * hyp_emissions_CO2

    # Bilan_Eco_MDE = [Bilan_Economique, Bilan_Energétique, Bilan_Environnemental]
    return Bilan_Economique, Bilan_Energétique, Bilan_Environnemental, Inaction
