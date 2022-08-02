from .models import *
from .solutions import *
from .mobilite import *
from .MDE import *
import numpy as np


def solution_catalogue(conso_perso, profil, perso, territ, surface, installation, puissance, batteries, centrale_autoprod,
                       centrale_entrelesdeux):

    catalogue = CatalogueSolution.objects.filter(installation=installation)

    choices = FacturationItem.objects.filter(type="Module photovoltaïque")
    choices = [x for x in choices]
    modulepv_qt = ItemQuantite.objects.get(
        catalogue_solution=catalogue[0], facturation_item__in=choices)
    modulepv = modulepv_qt.facturation_item
    panneau_name = modulepv.article
    panneau_qt = modulepv_qt.quantite
    panneau = ModulesPV.objects.get(Nom=panneau_name)

    # les tailles standard < 100 kWc
    tailles = [x.taille for x in catalogue if x.taille < 100]
    tailles.sort()

    n = len(tailles)-1  # de 0 à n

    surface_panneau = panneau.Surface_Panneau_m2

    # taille_GT = solution(panneau_name, conso_perso, profil, territ, surface, installation, puissance, batteries, centrale_autoprod,
    #                      centrale_entrelesdeux)[0]

    taille_GT = dimensionnement_potentiel_centrale_autoconso(
        conso_perso, profil, perso, territ)

    # batterie = solution(panneau_name, conso_perso, profil, territ, surface, installation, puissance, batteries, centrale_autoprod,
    #                     centrale_entrelesdeux)[2]

    # on sélectionne la centrale standard juste au-dessus de la centrale idéale
    # on vérifie que la surface est assez grande, on réduit la taille si besoin

    tailles_sols = choose_tailles(
        taille_GT, installation, surface, surface_panneau)

    sols = [CatalogueSolution.objects.get(
        taille=t, installation=installation) for t in tailles_sols]

    sol = concat_solutions(sols, installation)

    return sol


def choose_tailles(taille_GT, installation, surface, surface_panneau):
    catalogue = CatalogueSolution.objects.filter(installation=installation)

    # les tailles standard < 100 kWc
    tailles = [x.taille for x in catalogue if x.taille < 100]
    tailles.sort()

    sols = [CatalogueSolution.objects.get(
        taille=t, installation=installation) for t in tailles]
    choices = FacturationItem.objects.filter(type="Module photovoltaïque")
    choices = [x for x in choices]
    panneau_qts = [ItemQuantite.objects.get(
        catalogue_solution=sol, facturation_item__in=choices) for sol in sols]
    nbs = [x.quantite for x in panneau_qts]

    n = len(tailles) - 1

    nb = 0
    taille = 0
    tailles_sols = []
    surface_min = 0

    # petite centrale
    if taille_GT <= tailles[0]:
        taille += tailles[0]
        nb += nbs[0]
        tailles_sols.append(tailles[0])
        surface_min = nb*surface_panneau

    # petite centrale
    elif tailles[0] < taille_GT <= tailles[n]:
        i = 0
        surface_min = nbs[1]*surface_panneau
        while tailles[i] < taille_GT and i < n and surface > surface_min:
            i += 1
            if i < n:
                surface_min = nbs[i+1]*surface_panneau

        taille += tailles[i]
        nb += nbs[i]
        tailles_sols.append(tailles[i])
        surface_min = nb*surface_panneau

    # centrale > 100 kWc
    else:
        nb_big = 0

        # >= 1 centrale de 100 ?
        surface_min = nbs[n]*surface_panneau

        taille_reste = taille_GT  # taille_reste pour gérer le nombre de centrales de 100

        if surface > surface_min:
            taille_reste -= tailles[n]
            taille += tailles[n]
            nb += nbs[n]
            nb_big += 1

        # pas assez de surface pour 1 centrale de 100
        else:
            surface_min = nbs[0]*surface_panneau
            if surface > surface_min:
                i = 0
                surface_min = nbs[1]*surface_panneau
                while surface > surface_min and i < n:
                    i += 1
                    if i < n:
                        surface_min = nbs[i+1]*surface_panneau

                taille += tailles[i]
                nb += nbs[i]
                tailles_sols.append(tailles[i])
                surface_min = nb*surface_panneau

        # multiple d'une centrale de 100
        surface_min = (nb+nbs[n])*surface_panneau
        while surface > surface_min and taille_reste > tailles[n]:
            nb_big += 1
            taille_reste -= tailles[n]
            taille += tailles[n]
            nb += nbs[n]
            surface_min = (nb+nbs[n])*surface_panneau

        for _ in range(nb_big):
            tailles_sols.append(tailles[n])

        # on choisit une petite centrale à ajouter en bonus
        if taille_reste <= tailles[n]:
            surface_min = (nb+nbs[0])*surface_panneau
            if taille_reste <= tailles[0] and surface > surface_min:
                taille += tailles[0]
                nb += nbs[0]
                tailles_sols.append(tailles[0])
                surface_min = nb*surface_panneau

            surface_min = (nb+nbs[0])*surface_panneau
            if taille_reste > tailles[0] and surface > surface_min:
                i = 0
                surface_min = (nb+nbs[1])*surface_panneau
                while tailles[i] < taille_reste and i < n and surface > surface_min:
                    i += 1
                    if i < n:
                        surface_min = (nb+nbs[i+1])*surface_panneau

                taille += tailles[i]
                nb += nbs[i]
                tailles_sols.append(tailles[i])
                surface_min = nb*surface_panneau

        else:
            i = 0
            surface_min = nbs[1]*surface_panneau
            while surface > surface_min and i < n:
                i += 1
                if i < n:
                    surface_min = nbs[i+1]*surface_panneau

            taille += tailles[i]
            nb += nbs[i]
            tailles_sols.append(tailles[i])
            surface_min = nb*surface_panneau
            taille_reste -= tailles[i]

    return tailles_sols


def concat_solutions(solutions_list, installation):
    if len(solutions_list) == 1:
        t = solutions_list[0].taille
        sol = CatalogueSolution.objects.get(
            taille=t, installation=installation)
        return sol

    taille_concat = 0
    qt = {}

    for solution in solutions_list:
        rqt = ItemQuantite.objects.filter(catalogue_solution=solution)
        for el in rqt:
            qt[el.facturation_item] = 0

        taille_concat += solution.taille
    taille_concat = round(taille_concat, 1)

    for solution in solutions_list:
        rqt = ItemQuantite.objects.filter(catalogue_solution=solution)
        for el in rqt:
            qt[el.facturation_item] += el.quantite

    if not CatalogueSolution.objects.filter(taille=taille_concat).exists():
        sol = CatalogueSolution(taille=taille_concat,
                                installation="Triphasée", marge=30)
        sol.save()
    else:
        sol = CatalogueSolution.objects.get(taille=taille_concat)

    ItemQuantite.objects.filter(catalogue_solution=sol).delete()
    for el in qt.keys():
        if not ItemQuantite.objects.filter(catalogue_solution=sol,
                                           facturation_item=el).exists():
            x = ItemQuantite(catalogue_solution=sol,
                             facturation_item=el, quantite=qt[el])
            x.save()

    return sol


def change(sol, plus):
    # plus = True pour passer à la prochaine centrale en termes de taille
    # plus = False pour passer à celle juste avant

    installation = "Triphasée"
    catalogue = CatalogueSolution.objects.filter(installation=installation)
    # les tailles standard < 100 kWc
    tailles = [x.taille for x in catalogue if x.taille < 100]
    n = len(tailles)-1
    tailles.sort()
    t_max = tailles[n]

    # solution actuelle
    t = sol.taille

    # recréer la liste solutions_list à partir de la taille de la centrale déjà sélectionnée
    # et modifier pour avoir la centrale juste après
    tailles_sols = []
    ta = t
    ta = round(ta, 1)

    while ta >= t_max:
        ta -= t_max
        tailles_sols.append(t_max)
    print(1)
    ta = round(ta, 1)
    # maintenant ta < t_max
    if ta >= tailles[0]:
        print(2)
        print(ta)
        print(tailles[0])
        i = 0
        while i < n-1 and ta > tailles[i]:
            i += 1
        # on sait que i<n
        if plus:
            i += 1
            tailles_sols.append(tailles[i])
            print(3)
        else:
            print(4)
            if i > 0:
                print(5)
                tailles_sols.append(tailles[i-1])
            else:
                print(6)
                if tailles_sols == []:
                    tailles_sols.append(tailles[0])
    else:
        print(7)
        if plus:
            print(8)
            tailles_sols.append(tailles[0])
        else:
            print(8)
            if tailles_sols != []:
                print(9)
                tailles_sols.pop(-1)
                tailles_sols.append(tailles[n-1])
            else:
                print(10)
                tailles_sols.append(tailles[0])

    sols = [CatalogueSolution.objects.get(
        taille=t, installation=installation) for t in tailles_sols]

    sol = concat_solutions(sols, installation="Triphasée")

    return sol


def calcul_taux_centraleGT_catalogue(conso_perso, profil, perso, territ, surface, installation, puissance, batteries, centrale_autoprod,
                                     centrale_entrelesdeux):

    catalogue = CatalogueSolution.objects.filter(installation=installation)

    choices = FacturationItem.objects.filter(type="Module photovoltaïque")
    choices = [x for x in choices]
    modulepv_qt = ItemQuantite.objects.get(
        catalogue_solution=catalogue[0], facturation_item__in=choices)
    modulepv = modulepv_qt.facturation_item
    panneau_name = modulepv.article
    panneau = ModulesPV.objects.get(Nom=panneau_name)

    centrale_GT = solution_catalogue(conso_perso, profil, perso, territ, surface, installation, puissance, batteries, centrale_autoprod,
                                     centrale_entrelesdeux).taille

    # ATTENTION
    # Batterie en kWh dans les params

    if batteries == True:
        Batterie = solution_catalogue(conso_perso, profil, perso, territ, surface, installation, puissance, batteries, centrale_autoprod,
                                      centrale_entrelesdeux)*1000
        Batterie = 0
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
    coeffs_ouvre = courbe_de_charges(conso_perso, profil, perso)[0]
    coeffs_weekend = courbe_de_charges(conso_perso, profil, perso)[1]

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

    # surplus annuel
    surplus = surplus_ouvre_ensoleille_annuel+surplus_weekend_ensoleille_annuel + \
        surplus_ouvre_nuageux_annuel+surplus_weekend_nuageux_annuel
    surplus = surplus/1000  # kWh

    # HYPER IMPORTANT pour les économies
    energie_autoconsommee = (ep_nuageux_annuel + ep_soleil_annuel - surplus_ouvre_nuageux_annuel - surplus_ouvre_ensoleille_annuel - surplus_weekend_nuageux_annuel - surplus_weekend_ensoleille_annuel
                             + eb_ouvre_nuageux_annuel+eb_ouvre_soleil_annuel+eb_weekend_nuageux_annuel+eb_weekend_soleil_annuel) / 1000  # unité ?

    return tab, taux_autoconso_batterie, taux_autoprod_batterie, energie_autoconsommee, surplus


def Economies_pv_catalogue(conso_perso, profil, perso, territ, surface, installation, puissance, NbrekWhfacture, Recurrencefacture, Montantfacture, Nbreetages, type, batteries, centrale_autoprod,
                           centrale_entrelesdeux):

    catalogue = CatalogueSolution.objects.filter(installation=installation)

    choices = FacturationItem.objects.filter(type="Module photovoltaïque")
    choices = [x for x in choices]
    modulepv_qt = ItemQuantite.objects.get(
        catalogue_solution=catalogue[0], facturation_item__in=choices)
    modulepv = modulepv_qt.facturation_item
    panneau_name = modulepv.article
    panneau = ModulesPV.objects.get(Nom=panneau_name)

    #coeff_ouvre = courbe_de_charges(conso_perso, profil)[0]
   # coeff_weekend = courbe_de_charges(conso_perso, profil)[1]
    # energie_autoconsome= calcul_taux_centraleGT(panneau, conso_perso, profil, territ, surface,installation, puissance, batteries, centrale_autoprod,
    # centrale_entrelesdeux)[3]

    #sum_coeff_ouvre = np.sum(coeff_ouvre)*Nb_jours_ouvres
   # sum_coeff_weekend= np.sum(coeff_weekend)*(365-Nb_jours_ouvres)

    # Prendre les mêmes variables que pour la MDE pour avoir de la cohérence !
    NbrekWhannuel = Variables_mde(
        NbrekWhfacture, Recurrencefacture, Montantfacture, surface, Nbreetages)[2]

    energie_autoconsome = calcul_taux_centraleGT_catalogue(conso_perso, profil, perso, territ, surface, installation, puissance, batteries,
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

    # taille de la centrale
    centrale_GT = solution_catalogue(conso_perso, profil, perso, territ, surface, installation, puissance, batteries, centrale_autoprod,
                                     centrale_entrelesdeux).taille

    # € / kWh
    if centrale_GT < 9:
        prix_vente = territ.prix_coeff_1_2 / 100
    elif centrale_GT < 36:
        prix_vente = territ.prix_coeff_1_1 / 100
    elif centrale_GT < 100:
        prix_vente = territ.prix_coeff_1 / 100
    else:
        prix_vente = 0
    surplus_annuel = calcul_taux_centraleGT_catalogue(conso_perso, profil, perso, territ, surface, installation, puissance, batteries, centrale_autoprod,
                                                      centrale_entrelesdeux)[4]
    revente_surplus = round(surplus_annuel*prix_vente, 2)

    print(surplus_annuel)

    difference = [0] * 20
    for i in range(20):
        difference[i] = (ancienne_conso[i] -
                         conso_reduite[i]) * tab_prix_elec[i]

    Inaction = [0] * 20
    for i in range(20):
        Inaction[i] = round(ancienne_conso[i] * tab_prix_elec[i], 2)

    Bilan_Economique = [0] * 3
    # économies sur la facture EDF grâce au PV autoconsommé année 1
    Bilan_Economique[0] = round(difference[0]+revente_surplus, 2)
    # idem sur 10 ans
    Bilan_Economique[1] = 0

    for k in range(10):
        Bilan_Economique[1] += difference[k]+revente_surplus
    Bilan_Economique[1] = round(Bilan_Economique[1], 2)
    # idem sur 20 ans
    Bilan_Economique[2] = round(sum(difference)+revente_surplus*20, 2)

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
    return Bilan_Economique, Bilan_Energétique, Bilan_Environnemental, Inaction, revente_surplus


def Bilan1_catalogue(conso_perso, profil, perso, territ, surface, installation, puissance, NbrekWhfacture, Recurrencefacture,
                     Montantfacture, Nbreetages, type, NbreVS, NbkmanVS, NbreVU, NbkmanVU):

    rqt0 = Emisission_CO2.objects.get(territ=territ)
    rqt1 = Emisission_CO2.objects.get(territ="Litre d'essence")
    prix_L_essence = rqt1.emission

    # Creation du tableau e l'onglet Bilan 1 Bât
    # Bilan_avant [0,0]: Economique : MDE/PV sur 1 an
    # Bilan_avant [0,1]: Economique : Mobilité sur 1 an
    # Bilan_avant [0,2]: Economique : Total MDE/PV + Mobilite sur 1 an

    # Bilan_avant [0,3]: Economique : MDE/PV sur 10 ans
    # Bilan_avant [0,4]: Economique : Mobilité sur 10 ans
    # Bilan_avant [0,5]: Economique : Total MDE/PV + Mobilite sur 10 ans

    # Bilan_avant [0,6]: Economique : MDE/PV sur 20 ans
    # Bilan_avant [0,7]: Economique : Mobilité sur 20 ans
    # Bilan_avant [0,8]: Economique : Total MDE/PV + Mobilite sur 20 ans

    # Bilan_avant [1,0]: Energetique : MDE/PV sur 1 an
    # Bilan_avant [1,1]: Energetique : Mobilité sur 1 an
    # Bilan_avant [1,2]: Energetique : Total MDE/PV + Mobilite sur 1 an

    # Bilan_avant [1,3]: Energetique : MDE/PV sur 10 ans
    # Bilan_avant [1,4]: Energetique : Mobilité sur 10 ans
    # Bilan_avant [1,5]: Energetique : Total MDE/PV + Mobilite sur 10 ans

    # Bilan_avant [1,6]: Energetique : MDE/PV sur 20 ans
    # Bilan_avant [1,7]: Energetique : Mobilité sur 20 ans
    # Bilan_avant [1,8]: Energetique : Total MDE/PV + Mobilite sur 20 ans

    # Bilan_avant [2,0]: Environnement : MDE/PV sur 1 an
    # Bilan_avant [2,1]: Environnement : Mobilité sur 1 an
    # Bilan_avant [1,2]: Environnement : Total MDE/PV + Mobilite sur 1an

    # Bilan_avant [2,3]: Environnement : MDE/PV sur 10 ans
    # Bilan_avant [2,4]: Environnement : Mobilité sur 10 ans
    # Bilan_avant [2,5]: Environnement : Total MDE/PV + Mobilite sur 10 ans

    # Bilan_avant [2,6]: Environnement : MDE/PV sur 20 ans
    # Bilan_avant [2,7]: Environnement : Mobilité sur 20 ans
    # Bilan_avant [2,8]: Environnement : Total MDE/PV + Mobilite sur 20 ans

    # Tous ce qui est util :
    Inaction = Economies_pv_catalogue(conso_perso, profil, perso, territ, surface, installation, puissance, NbrekWhfacture, Recurrencefacture,
                                      Montantfacture, Nbreetages, type, batteries=False, centrale_autoprod=False,
                                      centrale_entrelesdeux=False)[3]

    Mobilite_1an = Vehicule_thermique_annuel(
        NbreVS, NbkmanVS, NbreVU, NbkmanVU)[4]

    Ancienne_conso = Variables_mde(
        NbrekWhfacture, Recurrencefacture, Montantfacture, surface, Nbreetages)[2]
    L_carburant = Vehicule_thermique_annuel(
        NbreVS, NbkmanVS, NbreVU, NbkmanVU)[3]

    Bilan_avant = np.zeros((3, 9), object)
    Bilan_avant[0, 0] = Inaction[0]
    Bilan_avant[0, 1] = Mobilite_1an[0]
    Bilan_avant[0, 2] = Bilan_avant[0, 0]+Bilan_avant[0, 1]

    Bilan_avant[0, 3] = sum(Inaction[0:9])
    Bilan_avant[0, 4] = sum(Mobilite_1an[0:9])
    Bilan_avant[0, 5] = Bilan_avant[0, 3] + Bilan_avant[0, 4]

    Bilan_avant[0, 6] = sum(Inaction[0:19])
    Bilan_avant[0, 7] = sum(Mobilite_1an[0:19])
    Bilan_avant[0, 8] = Bilan_avant[0, 3] + Bilan_avant[0, 4]

    Bilan_avant[1, 0] = Ancienne_conso
    Bilan_avant[1, 1] = 0
    Bilan_avant[0, 2] = Bilan_avant[1, 0] + Bilan_avant[1, 1]

    Bilan_avant[1, 3] = Ancienne_conso*10
    Bilan_avant[1, 4] = 0
    Bilan_avant[1, 5] = Bilan_avant[1, 3] + Bilan_avant[1, 4]

    Bilan_avant[1, 6] = Ancienne_conso*10
    Bilan_avant[1, 7] = 0
    Bilan_avant[1, 8] = Bilan_avant[1, 3] + Bilan_avant[1, 4]

    Bilan_avant[2, 0] = Ancienne_conso * rqt0.emission
    Bilan_avant[2, 1] = L_carburant*prix_L_essence
    Bilan_avant[2, 2] = Bilan_avant[2, 2] + Bilan_avant[2, 2]

    Bilan_avant[2, 3] = Bilan_avant[2, 0]*10
    Bilan_avant[2, 4] = Bilan_avant[2, 1]*10
    Bilan_avant[2, 5] = Bilan_avant[2, 3] + Bilan_avant[2, 4]

    Bilan_avant[2, 6] = Bilan_avant[2, 3]*2
    Bilan_avant[2, 7] = Bilan_avant[2, 4]*2
    Bilan_avant[2, 8] = Bilan_avant[2, 6] + Bilan_avant[2, 7]

    return Bilan_avant
