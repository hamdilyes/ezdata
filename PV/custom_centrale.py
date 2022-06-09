#Création du tableau issu de la feuille Analyse de Production
from django.db import models
from .models import (BDD, ModulesPV,Emisission_CO2)
from .MDE import Coeffs_mde,Variables_mde
from .Input import Load_Input
from .dimens_centrale import courbe_de_charges, courbe_irradiation
import numpy as np
# Variables statiques
Load_Input()

#Hypthèses
Rendement_batteries_Lithium= 0.95
Decharge_maximale_batteries_Lithium = 0.8
Perte1 = 0.05 #%
Nb_jours_ouvres= 261

def calcul_taux_centraleGT_custom(centrale, batterie , panneau, conso_perso, profil, territ, surface,installation, puissance, batteries):


    #ATTENTION
    # Batterie en kWh dans les params
    #ep_ouvre_nuageux et ep_ouvre_soleil ne correspondent pas forcement à des jours ouvrés: abus de langage par Kenza

    if batteries==True:
        Batterie= batterie
        Decharge= (Batterie/2.4)*1.2

    else:
        Batterie=0
        Decharge=0

    tab = np.zeros((24, 20), float)

    G = courbe_irradiation(territ)

    Ep_moyenne = territ.Ep_moyenne  # kWh/kWc
    Ep_defavorable = territ.Ep_defavorable  # kWh/kWc
    Ep_favorable = territ.Ep_favorable  # kWh/kWc
    PR = territ.PR


    Nb_jours_favorables=365 * (Ep_moyenne-Ep_defavorable) / ( Ep_favorable -Ep_defavorable )
    coeffs_ouvre = courbe_de_charges(conso_perso, profil)[0]
    coeffs_weekend = courbe_de_charges(conso_perso, profil)[1]

    for i in range(24):
        tab[i][0] = i  # Heures
        tab[i][1] = G[i][3] * PR * centrale  # Energie produite moyenne (W)
        tab[i][2] = tab[i][1] * Ep_defavorable / Ep_moyenne  # Energie produite jour nuageux (Wh)
        tab[i][3] = tab[i][1] * Ep_favorable / Ep_moyenne  # Energie produite jour ensoleillé  (Wh)
        tab[i][4] = max(tab[i][2] - coeffs_ouvre[i], 0)  # Surplus jour ouvré nuageux  (Wh)
        tab[i][5] = max(tab[i][3] - coeffs_ouvre[i], 0)  # Surplus jour ouvré ensoleillé  (Wh)
        tab[i][6] = max(tab[i][2] - coeffs_weekend[i], 0)  # Surplus weekend nuageux  (Wh)
        tab[i][7] = max(tab[i][3] - coeffs_weekend[i], 0)  # Surplus weekend ensoleillé  (Wh)

        #Calculs de taux /jours qui seront utilisées pour les prochaines colonnes
    charge_ouvre_jour = np.sum(coeffs_ouvre)
    charge_weekend_jour = np.sum(coeffs_weekend)
    ep_ouvre_nuageux_jour = np.sum(tab[:, 2])
    ep_ouvre_soleil_jour = np.sum(tab[:, 3])
    surplus_ouvre_nuageux_jour = np.sum(tab[:, 4])
    surplus_ouvre_ensoleille_jour = np.sum(tab[:, 5])
    surplus_weekend_nuageux_jour = np.sum(tab[:, 6])
    surplus_weekend_ensoleille_jour = np.sum(tab[:, 7])


    for i in range(24):
        if (tab[i][4])>0:
            # Stockage batterie jour ouvré nuageux  (Wh)
            tab[i][8] = min(Batterie*Decharge_maximale_batteries_Lithium-np.sum(tab[0:i,8]),tab[i][4]*Rendement_batteries_Lithium,
                            charge_ouvre_jour-ep_ouvre_nuageux_jour+surplus_ouvre_nuageux_jour-np.sum(tab[0:i,8]))

        if (tab[i][8]) < 0:
            tab[i][8]=0

    stockage_ouvre_nuageux_jour= np.sum(tab[:, 8])

    for i in range(24):
        if((tab[i][5])>0):
            # Stockage batterie jour ouvré ensolleilé  (Wh)
            tab[i][9]=  min(Batterie*Decharge_maximale_batteries_Lithium-np.sum(tab[0:i,9]) ,tab[i][5]*Rendement_batteries_Lithium,
                            charge_ouvre_jour-ep_ouvre_soleil_jour+surplus_ouvre_ensoleille_jour-np.sum(tab[0:i,9]))

        if (tab[i][9]) < 0:
            tab[i][9] = 0

    stockage_ouvre_soleil_jour= np.sum(tab[:, 9])

    for i in range(24):
        if (tab[i][6]) > 0:
            # Stockage batterie weekend nuageux  (Wh)
            tab[i][10] = min(Batterie * Decharge_maximale_batteries_Lithium-np.sum(tab[0:i,10]), tab[i][6] * Rendement_batteries_Lithium,
                            charge_weekend_jour - ep_ouvre_nuageux_jour + surplus_weekend_nuageux_jour-np.sum(tab[0:i,10]))

        if (tab[i][10]) < 0:
            tab[i][10] = 0


    stockage_weekend_nuageux_jour= np.sum(tab[:, 10])

    for i in range(24):
        if (tab[i][7]) > 0:
            # Stockage batterie weekend ensolleilé  (Wh)
            tab[i][11] = min(Batterie * Decharge_maximale_batteries_Lithium, tab[i][7] * Rendement_batteries_Lithium,
                             charge_weekend_jour - ep_ouvre_soleil_jour + surplus_weekend_ensoleille_jour-np.sum(tab[0:i,11]))

        if (tab[i][11]) < 0:
            tab[i][11] = 0

    stockage_weekend_ensolleile_jour= np.sum(tab[:, 11])


    for i in range(13,24):
        # Energie fournie batterie jour ouvré nuageux (Wh)
        tab[i][12] =  min(max(coeffs_ouvre[i]-tab[i][2],0),Decharge,stockage_ouvre_nuageux_jour - np.sum(tab[12:i, 12]))

        # Energie fournie batterie jour ouvré ensolleilé (Wh)
        tab[i][13] = min(max(coeffs_ouvre[i]-tab[i][3],0),Decharge,stockage_ouvre_soleil_jour - np.sum(tab[12:i, 13]))

        # Energie fournie batterie weekend nuageux (Wh)
        tab[i][14] = min(max(coeffs_weekend[i]-tab[i][2],0),Decharge,stockage_weekend_nuageux_jour - np.sum(tab[12:i, 14]))

        # Energie fournie batterie weekend ensolleilé nuageux (Wh)
        tab[i][15] = min(max(coeffs_weekend[i]-tab[i][5],0),Decharge,stockage_weekend_ensolleile_jour - np.sum(tab[12:i, 15]))

    for i in range(0,12):
        tab[i][12] = min(max(coeffs_ouvre[i]-tab[i][2],0),Decharge,stockage_ouvre_nuageux_jour - np.sum(tab[0:i, 12])- np.sum(tab[12:24, 12]))
        tab[i][13] =  min(max(coeffs_ouvre[i]-tab[i][3],0),Decharge,stockage_ouvre_soleil_jour - np.sum(tab[0:i, 13])- np.sum(tab[12:24, 13]))
        tab[i][14] = min(max(coeffs_weekend[i]-tab[i][2],0),Decharge,stockage_weekend_nuageux_jour - np.sum(tab[0:i, 14])- np.sum(tab[12:24, 14]))
        tab[i][15] = min(max(coeffs_weekend[i]-tab[i][5],0),Decharge,stockage_weekend_ensolleile_jour - np.sum(tab[0:i, 15])- np.sum(tab[12:24, 15]))

        ########################################

    # Taux final Annuel : totaux

    #ep = Energie produite

    ep_ouvre_nuageux_annuel = np.sum(tab[:, 2]) * (365 - Nb_jours_favorables)
    ep_ouvre_soleil_annuel = np.sum(tab[:, 3]) * (Nb_jours_favorables)
    surplus_ouvre_nuageux_annuel = np.sum(tab[:, 4]) * (365 - Nb_jours_favorables) * Nb_jours_ouvres / 365
    surplus_ouvre_ensoleille_annuel = np.sum(tab[:, 5]) * Nb_jours_favorables * Nb_jours_ouvres / 365
    surplus_weekend_nuageux_annuel = np.sum(tab[:, 6]) * (365 - Nb_jours_favorables) * (365 - Nb_jours_ouvres) / 365
    surplus_weekend_ensoleille_annuel = np.sum(tab[:, 7]) * (365 - Nb_jours_ouvres) * Nb_jours_favorables / 365

    #eb = energie batterie

    eb_ouvre_nuageux_annuel =  np.sum(tab[:, 12]) * Nb_jours_ouvres* (365 - Nb_jours_favorables)/365
    eb_ouvre_soleil_annuel = np.sum(tab[:, 13]) * Nb_jours_favorables * Nb_jours_ouvres / 365
    eb_weekend_nuageux_annuel =  np.sum(tab[:, 14]) * (365 - Nb_jours_favorables) * (365 - Nb_jours_ouvres) / 365
    eb_weekend_soleil_annuel = np.sum(tab[:, 15]) * (365 - Nb_jours_ouvres) * Nb_jours_favorables / 365



    sum_charge_ouvre = np.sum(coeffs_ouvre) * Nb_jours_ouvres
    sum_charge_weekend = np.sum(coeffs_weekend) * (365 - Nb_jours_ouvres)

    taux_autoconso = (ep_ouvre_nuageux_annuel + ep_ouvre_soleil_annuel - surplus_ouvre_nuageux_annuel - surplus_ouvre_ensoleille_annuel - surplus_weekend_nuageux_annuel - surplus_weekend_ensoleille_annuel) / (
                                 ep_ouvre_nuageux_annuel + ep_ouvre_soleil_annuel) * 100


    taux_autoprod = (ep_ouvre_nuageux_annuel + ep_ouvre_soleil_annuel - surplus_ouvre_nuageux_annuel - surplus_ouvre_ensoleille_annuel - surplus_weekend_nuageux_annuel - surplus_weekend_ensoleille_annuel) / (
                                sum_charge_ouvre + sum_charge_weekend) * 100

    taux_autoconso_batterie= (ep_ouvre_nuageux_annuel + ep_ouvre_soleil_annuel - surplus_ouvre_nuageux_annuel - surplus_ouvre_ensoleille_annuel - surplus_weekend_nuageux_annuel - surplus_weekend_ensoleille_annuel
                              +eb_ouvre_nuageux_annuel+eb_ouvre_soleil_annuel+eb_weekend_nuageux_annuel+eb_weekend_soleil_annuel)/(ep_ouvre_nuageux_annuel+ ep_ouvre_soleil_annuel)* 100

    taux_autoprod_batterie= (ep_ouvre_nuageux_annuel + ep_ouvre_soleil_annuel - surplus_ouvre_nuageux_annuel - surplus_ouvre_ensoleille_annuel - surplus_weekend_nuageux_annuel - surplus_weekend_ensoleille_annuel
                             +eb_ouvre_nuageux_annuel+eb_ouvre_soleil_annuel+eb_weekend_nuageux_annuel+eb_weekend_soleil_annuel) / (
                                sum_charge_ouvre + sum_charge_weekend) * 100

    #HYPER IMPORTANT pour les économies
    taux_autoconso_economie = (ep_ouvre_nuageux_annuel + ep_ouvre_soleil_annuel - surplus_ouvre_nuageux_annuel - surplus_ouvre_ensoleille_annuel - surplus_weekend_nuageux_annuel - surplus_weekend_ensoleille_annuel
                               +eb_ouvre_nuageux_annuel+eb_ouvre_soleil_annuel+eb_weekend_nuageux_annuel+eb_weekend_soleil_annuel) / 1000

    return (tab, taux_autoconso_batterie,taux_autoprod_batterie, taux_autoconso_economie  )

def surface_range(centrale, panneau):

    panneau_requete = ModulesPV.objects.get(Nom=panneau)
    surface_panneau = panneau_requete.Surface_Panneau_m2
    puissance_panneau = panneau_requete.Puissance_modulaire_kW

    nbr_modules = centrale / puissance_panneau
    surface_toiture = surface_panneau * nbr_modules

    return surface_toiture