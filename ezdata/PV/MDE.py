from .models import Emisission_CO2, BDDBat, Hyp_cout_mobilite
from .Input import *

Load_Input()

Taux_invest = 0.1  # Pourcentage des économies sur 20 ans qui finance la MDE


# NbrekWhfacture = 40000  # Donnée à prendre dans les inputs clients
# Recurrencefacture = 'Mensuelle'  # Donnée à prendre dans les inputs clients
# Montantfacture = 8000  # Donnée à prendre dans les inputs clients
# Nbreetages = 1  # Donnée à prendre dans les inputs clients

def Variables_mde(NbrekWhfacture, Recurrencefacture, Montantfacture, Surfacetoiture, Nbreetages):

    if Recurrencefacture == 'Mensuelle':
        Mois = 12

    if Recurrencefacture == 'Bimestrielle':
        Mois = 6

    if Recurrencefacture == 'Annuelle':
        Mois = 1

    NbrekWhannuel = NbrekWhfacture * Mois
    Montantannuel = Montantfacture * Mois

    Consokwhman = NbrekWhannuel / (Surfacetoiture * Nbreetages)  # kWh/m²/an
    Consoeuroan = Montantannuel / (Surfacetoiture * Nbreetages)  # euros/m²/an

    # A aller chercher dans Inputs (dans cet onglet, le prix est déterminé soit en fonction de la facture si on l'a, soit en fonction du secteur si on a pas d'infos sur la facture)
    Prix_elec = Montantannuel / NbrekWhannuel
    return Consokwhman, Consoeuroan, NbrekWhannuel, Montantannuel, Prix_elec


def Reduction(type, Consokwhman):
    rqt0 = BDDBat.objects.get(type=type)

    if Consokwhman < rqt0.moy_euros_avant:
        Reduc = 0.05
    if Consokwhman > rqt0.moy_euros_avant:
        Reduc_possible = -1 * rqt0.gain
        # print (Reduc_possible)
        # On veut que la réduction soit entrée automatiquement par l'outil et ne plus avoir besoin d'opé comme actuellement

        if 0.10 < Reduc_possible < 0.15:
            Reduc = 0.06
        if 0.15 <= Reduc_possible < 0.20:
            Reduc = 0.07
        if 0.20 <= Reduc_possible < 0.25:
            Reduc = 0.08
        if 0.25 <= Reduc_possible < 0.30:
            Reduc = 0.09
        if Reduc_possible >= 0.30:
            Reduc = 0.1
    return Reduc
# print (type_bat)

# Tableau de consommation d'électricité annuelle :


def Coeffs_mde(NbrekWhfacture, Recurrencefacture, Montantfacture, Surfacetoiture, Nbreetages, type):
    rqt6 = Hyp_cout_mobilite.objects.get(
        model="Augmentation prix électricité")  # €/mois
    Augmentation_prix_electricite = rqt6.valeur

    NbrekWhannuel = Variables_mde(
        NbrekWhfacture, Recurrencefacture, Montantfacture, Surfacetoiture, Nbreetages)[2]
    Consokwhman = Variables_mde(
        NbrekWhfacture, Recurrencefacture, Montantfacture, Surfacetoiture, Nbreetages)[0]
    Reduc = Reduction(type, Consokwhman)
    Prix_elec = Variables_mde(
        NbrekWhfacture, Recurrencefacture, Montantfacture, Surfacetoiture, Nbreetages)[4]

    Ancienne_conso = [NbrekWhannuel] * 20
    Ancienne_conso_coeff = [0] * 20
    # print (Ancienne_conso)

    Conso_reduite = [NbrekWhannuel * (1 - Reduc)] * 20

    Conso_reduite_coeff = [0] * 20
    # print (Conso_reduite)

    Tab_prix_elec = [0] * 20
    Tab_prix_elec[0] = Prix_elec
    for i in range(1, 20):
        Prix_elec = Prix_elec * (1 + Augmentation_prix_electricite / 100)
        Tab_prix_elec[i] = Prix_elec
        Ancienne_conso_coeff[i] = Ancienne_conso[i]*Tab_prix_elec[i]
        Conso_reduite_coeff[i] = Conso_reduite[i]*Tab_prix_elec[i]

        # print (Tab_prix_elec)

    Difference = [0] * 20
    for i in range(20):
        Difference[i] = (Ancienne_conso[i] - Conso_reduite[i]
                         ) * Tab_prix_elec[i]

    #tableau_conso_MDE = [Ancienne_conso, Conso_reduite, Tab_prix_elec, Difference]
    return Ancienne_conso_coeff, Conso_reduite_coeff, Tab_prix_elec, Difference, Ancienne_conso, Conso_reduite

# Bilan : Economies réalisables MDE


def Economies(NbrekWhfacture, Recurrencefacture, Montantfacture, Surfacetoiture, Nbreetages, type, territ):
    Ancienne_conso = Coeffs_mde(
        NbrekWhfacture, Recurrencefacture, Montantfacture, Surfacetoiture, Nbreetages, type)[4]
    Conso_reduite = Coeffs_mde(NbrekWhfacture, Recurrencefacture,
                               Montantfacture, Surfacetoiture, Nbreetages, type)[5]
    Difference = Coeffs_mde(NbrekWhfacture, Recurrencefacture,
                            Montantfacture, Surfacetoiture, Nbreetages, type)[3]

    Bilan_Economique = [0] * 3
    Bilan_Economique[0] = round(Difference[0], 2)
    Bilan_Economique[1] = 0

    for k in range(10):
        Bilan_Economique[1] += Difference[k]
    Bilan_Economique[1] = round(Bilan_Economique[1], 2)
    Bilan_Economique[2] = round(sum(Difference), 2)

    Bilan_Energétique = [0] * 3
    Bilan_Energétique[0] = Ancienne_conso[0] - Conso_reduite[0]
    Bilan_Energétique[1] = Bilan_Energétique[0] * 10
    Bilan_Energétique[2] = Bilan_Energétique[0] * 20

    # A aller chercher dans INPUT et dépend du territoire
    rqt = Emisission_CO2.objects.get(territ=territ)
    hyp_emissions_CO2 = rqt.emission

    Bilan_Environnemental = [0] * 3
    Bilan_Environnemental[0] = Bilan_Energétique[0] * hyp_emissions_CO2
    Bilan_Environnemental[1] = Bilan_Energétique[1] * hyp_emissions_CO2
    Bilan_Environnemental[2] = Bilan_Energétique[2] * hyp_emissions_CO2

    for liste in [Bilan_Environnemental, Bilan_Energétique, Bilan_Economique]:
        for i in range(len(liste)):
            liste[i] = round(liste[i], 2)

    #Bilan_Eco_MDE = [Bilan_Economique, Bilan_Energétique, Bilan_Environnemental]
    return Bilan_Economique, Bilan_Energétique, Bilan_Environnemental

    # Investissement MDE


def Invest(NbrekWhfacture, Recurrencefacture, Montantfacture, Surfacetoiture, Nbreetages, type, territ):
    Bilan_Economique = Economies(NbrekWhfacture, Recurrencefacture,
                                 Montantfacture, Surfacetoiture, Nbreetages, type, territ)[0]
    invest = Taux_invest * Bilan_Economique[2]

    return invest
