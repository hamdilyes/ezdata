import numpy as np
from .models import Emisission_CO2, Hyp_cout_mobilite, EZ_DRIVE
from .MDE import Variables_mde
from .Input import *

Load_Input()

### Variables statiques ###
### Données d'entrée à récupérer ###

## Calcul tableau cout vehicule thermique année par année sur 20 ans ##


def Vehicule_thermique_annuel(NbreVS, NbkmanVS, NbreVU, NbkmanVU):
    Cout_vehicule_thermique_annuel = np.ones((5, 20))
    # [0,0]= cout vehicule l'année 1
    # [1,0]= prix carburant au litre l'année 1
    # [2,0]= cout total carburant sur l'année 1
    # [3,0]= litres carburant sur l'année 1
    # [4,0]= cout total sur l'année 1
    Cout_vehicule_thermique_annuel[0, 0] = 12 * (
        Prix_vehicule_thermique * NbreVS + Prix_utililaire_thermique * NbreVU)
    Cout_vehicule_thermique_annuel[1, 0] = Prix_carburant_initial
    Cout_vehicule_thermique_annuel[2, 0] = (NbreVS * NbkmanVS * Consommation_vehicule_thermique + NbreVU * NbkmanVU * Consommation_utilitaire_thermique) / 100 * \
        Cout_vehicule_thermique_annuel[1, 0]
    Cout_vehicule_thermique_annuel[3, 0] = Cout_vehicule_thermique_annuel[2,
                                                                          0] / Cout_vehicule_thermique_annuel[1, 0]
    Cout_vehicule_thermique_annuel[4, 0] = Cout_vehicule_thermique_annuel[0,
                                                                          0] + Cout_vehicule_thermique_annuel[2, 0]

    for i in range(1, 20):
        Cout_vehicule_thermique_annuel[0, i] = 12 * (
            Prix_vehicule_thermique * NbreVS + Prix_utililaire_thermique * NbreVU)
        Cout_vehicule_thermique_annuel[1, i] = Cout_vehicule_thermique_annuel[1, i - 1] * (
            1 + Augmentation_prix_carburant / 100)
        Cout_vehicule_thermique_annuel[2, i] = (NbreVS * NbkmanVS * Consommation_vehicule_thermique + NbreVU * NbkmanVU * Consommation_utilitaire_thermique) / 100 * \
            Cout_vehicule_thermique_annuel[1, i]
        Cout_vehicule_thermique_annuel[3, i] = Cout_vehicule_thermique_annuel[2,
                                                                              i] / Cout_vehicule_thermique_annuel[1, i]
        Cout_vehicule_thermique_annuel[4, i] = Cout_vehicule_thermique_annuel[0,
                                                                              i] + Cout_vehicule_thermique_annuel[2, i]
    return Cout_vehicule_thermique_annuel

### Calcul tableau cout vehicule electrique année par année sur 20 ans ###


def Vehicule_electrique_annuel(NbreVS, NbkmanVS, NbreVU, NbkmanVU, NbrekWhfacture, Recurrencefacture, Montantfacture, Surfacetoiture, Nbreetages):

    Prix_electricite = Variables_mde(
        NbrekWhfacture, Recurrencefacture, Montantfacture, Surfacetoiture, Nbreetages)[4]

    Cout_vehicule_electrique_annuel = np.ones((4, 20))
    # [0,0]= cout vehicule l'année 1
    # [1,0]= prix kWh d'electricité l'année 1
    # [2,0]= cout total électricité sur l'année 1
    # [3,0]= cout total sur l'année 1
    Cout_vehicule_electrique_annuel[0, 0] = 12 * (
        Prix_vehicule_electrique * NbreVS + Prix_utililaire_electrique * NbreVU)
    Cout_vehicule_electrique_annuel[1, 0] = Prix_electricite
    Cout_vehicule_electrique_annuel[2, 0] = (NbreVS * NbkmanVS * Consommation_vehicule_electrique + NbreVU * NbkmanVU * Consommation_utilitaire_electrique) / 100 * \
        Cout_vehicule_electrique_annuel[1, 0]
    Cout_vehicule_electrique_annuel[3, 0] = Cout_vehicule_electrique_annuel[0,
                                                                            0] + Cout_vehicule_electrique_annuel[2, 0]

    for i in range(1, 20):
        Cout_vehicule_electrique_annuel[0, i] = 12 * (
            Prix_vehicule_electrique * NbreVS + Prix_utililaire_electrique * NbreVU)
        Cout_vehicule_electrique_annuel[1, i] = Cout_vehicule_electrique_annuel[1, i - 1] * (
            1 + Augmentation_prix_electricite / 100)
        Cout_vehicule_electrique_annuel[2, i] = (
            NbreVS * NbkmanVS * Consommation_vehicule_electrique + NbreVU * NbkmanVU * Consommation_utilitaire_electrique) / 100 * \
            Cout_vehicule_electrique_annuel[1, i]
        Cout_vehicule_electrique_annuel[3, i] = Cout_vehicule_electrique_annuel[0,
                                                                                i] + Cout_vehicule_electrique_annuel[2, i]
    return Cout_vehicule_electrique_annuel

### Calcul tableau investissment bornes ###


def Tableau_Bornes(Presenceparking, Nb_pdc_choisi, Accessibilite_parking, Optionborne, NbreVS, NbreVU, NbkmanVS, NbkmanVU):
    Investissement_bornes = np.zeros(4)
    # [0] = Investissement tous les 5 ans
    # [1] = Prix mensuel
    # [2] = Cout total sur 5 ans
    # [3] = Gains bornes publiques par an
    Nb_borne_double = 0
    Nb_borne_simple = 0

    if Presenceparking == 'Oui':
        if Optionborne == 'Oui':
            Nb_borne_double = Nb_pdc_choisi // 2
            Nb_borne_simple = Nb_pdc_choisi % 2

    if Optionborne == 'Oui':
        if Accessibilite_parking == "Public":
            Investissement_bornes[
                0] = Nb_borne_double * Investissement_initial_borne_double_PUBLIC + Nb_borne_simple * Investissement_initial_borne_simple_PUBLIC
            Investissement_bornes[
                1] = Nb_borne_double * Prix_borne_double_PUBLIC + Nb_borne_simple * Prix_borne_simple_PUBLIC
        else:
            Investissement_bornes[
                0] = Nb_borne_double * Investissement_initial_borne_double_PRIVATE + Nb_borne_simple * Investissement_initial_borne_simple_PRIVATE
            Investissement_bornes[
                1] = Nb_borne_double * Prix_borne_double_PRIVATE + Nb_borne_simple * Prix_borne_simple_PRIVATE

    Investissement_bornes[2] = Investissement_bornes[0] + \
        Investissement_bornes[1] * 12 * 5

    if Optionborne == 'Oui' and Accessibilite_parking == "Public":
        Investissement_bornes[3] = Benefice_revente_elec * \
            Estim_conso_borne * 365 * Nb_pdc_choisi

    ### Calcul des abonnements EZdrive si pas d'option borne ###

    Abonnement_EZ_Drive_salarie = 0
    Abonnement_EZ_Drive_utilitaire = 0

    if Optionborne == 'Non':
        if (NbkmanVS / 12) < 150:
            Abonnement_EZ_Drive_salarie = NbreVS * Abonnement_EZ_Drive_150km
        if (NbkmanVS / 12) < 300:
            Abonnement_EZ_Drive_salarie = NbreVS * Abonnement_EZ_Drive_300km
        if (NbkmanVS / 12) >= 300:
            Abonnement_EZ_Drive_salarie = NbreVS * Abonnement_EZ_Drive_600km

        if (NbkmanVU / 12) < 150:
            Abonnement_EZ_Drive_utilitaire = NbreVU * Abonnement_EZ_Drive_150km
        if (NbkmanVU / 12) < 300:
            Abonnement_EZ_Drive_utilitaire = NbreVU * Abonnement_EZ_Drive_300km
        if (NbkmanVU / 12) >= 300:
            Abonnement_EZ_Drive_utilitaire = NbreVU * Abonnement_EZ_Drive_600km

    ### Calcul du tableau bornes année par année sur 20 ans ###

    Bornes = np.zeros((3, 20))
    # [0,i]= Cout des bornes sur l'année i
    # [1,i]= Gains des bornes l'année i
    # [2,i]= Cout abonnements ezdrive l'année i
    for i in range(20):
        Bornes[0, i] = Investissement_bornes[1] * 12
        if i % 5 == 0:
            Bornes[0, i] += Investissement_bornes[0]
        Bornes[1, i] = Investissement_bornes[3]
        Bornes[2, i] = (Abonnement_EZ_Drive_salarie +
                        Abonnement_EZ_Drive_utilitaire) * 12
    return Bornes

### Calcul du différentiel de cout entre vehicule thermique et electrique année par année sur 20 ans ###


def Differenciel(NbreVS, NbkmanVS, NbreVU, NbkmanVU, Presenceparking, Nb_pdc_choisi, Accessibilite_parking, Optionborne, NbrekWhfacture, Recurrencefacture, Montantfacture, Surfacetoiture, Nbreetages):

    Differenciel_bornes = np.zeros((3, 20))  # Thermique - electrique
    Cout_vehicule_thermique_annuel = Vehicule_thermique_annuel(
        NbreVS, NbkmanVS, NbreVU, NbkmanVU)
    Cout_vehicule_electrique_annuel = Vehicule_electrique_annuel(
        NbreVS, NbkmanVS, NbreVU, NbkmanVU, NbrekWhfacture, Recurrencefacture, Montantfacture, Surfacetoiture, Nbreetages)

    Bornes = Tableau_Bornes(Presenceparking, Nb_pdc_choisi, Accessibilite_parking,
                            Optionborne, NbreVS, NbreVU, NbkmanVS, NbkmanVU)
    # [0,i]=Delta vehicules
    # [1,i]=Delta carburant
    # [2,i]=Delta total
    for i in range(20):
        Differenciel_bornes[0, i] = Cout_vehicule_thermique_annuel[0,
                                                                   i] - Cout_vehicule_electrique_annuel[0, i]
        Differenciel_bornes[1, i] = Cout_vehicule_thermique_annuel[2,
                                                                   i] - Cout_vehicule_electrique_annuel[2, i]
        Differenciel_bornes[2, i] = Cout_vehicule_thermique_annuel[4, i] - Cout_vehicule_electrique_annuel[3, i] - Bornes[
            0, i] + Bornes[1, i] - Bornes[2, i]
    return Differenciel_bornes

    ### Bilan des economies réalisables sur la mobilité ###


def Economies_mobilite(territ, NbreVS, NbkmanVS, NbreVU, NbkmanVU, Presenceparking, Nb_pdc_choisi,
                       Accessibilite_parking, Optionborne, NbrekWhfacture, Recurrencefacture, Montantfacture,
                       Surfacetoiture, Nbreetages):

    rqt99 = Emisission_CO2.objects.get(territ=territ)
    Emission_CO2 = rqt99.emission
    Differenciel_bornes = Differenciel(NbreVS, NbkmanVS, NbreVU, NbkmanVU, Presenceparking, Nb_pdc_choisi, Accessibilite_parking,
                                       Optionborne, NbrekWhfacture, Recurrencefacture, Montantfacture, Surfacetoiture, Nbreetages)

    Bilan_mobilité = np.zeros((2, 3))
    # [0,0]=Economique sur 1 an en euros
    # [0,1]=Economique sur 10 ans
    # [0,2]=Economique sur 20 ans
    # [1,0]=Environnemental sur 1 an en kg de CO2
    # [1,1]=Environnemental sur 10 ans
    # [1,2]=Environnemental sur 20 ans

    Bilan_mobilité[0, 0] = round(Differenciel_bornes[2, 0], 2)
    Bilan_mobilité[0, 1] = round(sum(Differenciel_bornes[2, :10]), 2)
    Bilan_mobilité[0, 2] = round(sum(Differenciel_bornes[2, :]), 2)

    Bilan_mobilité[1, 0] = round((NbkmanVS * NbreVS * Consommation_vehicule_thermique + NbreVU * NbkmanVU * Consommation_utilitaire_thermique) / 100 *
                                 emission_L_essence - ((NbkmanVS * NbreVS * Consommation_vehicule_electrique + NbreVU * NbkmanVU * Consommation_utilitaire_electrique) / 100 *
                                                       Emission_CO2), 2)
    Bilan_mobilité[1, 1] = round(Bilan_mobilité[1, 0] * 10, 2)
    Bilan_mobilité[1, 2] = round(Bilan_mobilité[1, 0] * 20, 2)

    Bilan_economique = Bilan_mobilité[0, :]
    Bilan_enviro = Bilan_mobilité[1, :]

    # moyenne annuelle sur 20 ans vs pris la première année
    eco_avant_mob = Vehicule_thermique_annuel(
        NbreVS, NbkmanVS, NbreVU, NbkmanVU)[4, :].sum()/20

    env_avant_mob = (NbkmanVS * NbreVS * Consommation_vehicule_thermique + NbreVU *
                     NbkmanVU * Consommation_utilitaire_thermique) / 100 * emission_L_essence

    cons_avant_mob = (NbkmanVS * NbreVS * Consommation_vehicule_thermique + NbreVU *
                      NbkmanVU * Consommation_utilitaire_thermique) / 100 * kwh_L_essence

    cons_apres_mob = (NbkmanVS * NbreVS * Consommation_vehicule_electrique + NbreVU *
                      NbkmanVU * Consommation_utilitaire_electrique) / 100

    Bilan_energ = cons_avant_mob - cons_apres_mob

    return Bilan_economique, Bilan_enviro, eco_avant_mob, env_avant_mob, cons_avant_mob, Bilan_energ
