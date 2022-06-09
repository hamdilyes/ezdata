from .models import Hyp_cout_mobilite, EZ_DRIVE, Emisission_CO2


def Load_Input():
    ### Variables statiques ###
    global Prix_vehicule_electrique
    global Prix_vehicule_thermique
    global Prix_utililaire_electrique
    global Prix_utililaire_thermique
    global Prix_electricite
    global Prix_carburant_initial
    global Augmentation_prix_electricite
    global Augmentation_prix_carburant
    global Consommation_vehicule_electrique
    global Consommation_vehicule_thermique
    global Consommation_utilitaire_electrique
    global Consommation_utilitaire_thermique
    global Prix_borne_simple_PRIVATE
    global Prix_borne_double_PRIVATE
    global Prix_borne_simple_PUBLIC
    global Prix_borne_double_PUBLIC
    global Investissement_initial_borne_simple_PRIVATE
    global Investissement_initial_borne_simple_PUBLIC
    global Investissement_initial_borne_double_PRIVATE
    global Investissement_initial_borne_double_PUBLIC
    global Benefice_revente_elec
    global Estim_conso_borne
    global Abonnement_EZ_Drive_150km
    global Abonnement_EZ_Drive_300km
    global Abonnement_EZ_Drive_600km
    global emission_L_essence
    global kwh_L_essence

    rqt0 = Hyp_cout_mobilite.objects.get(
        model="Prix véhicule + maintenance Electrique")  # €/mois
    Prix_vehicule_electrique = rqt0.valeur

    rqt1 = Hyp_cout_mobilite.objects.get(
        model="Prix véhicule + maintenance Thermique")  # €/mois
    Prix_vehicule_thermique = rqt1.valeur

    rqt2 = Hyp_cout_mobilite.objects.get(
        model="Prix véhicule utililaire + maintenance Electrique")  # €/mois
    Prix_utililaire_electrique = rqt2.valeur

    rqt3 = Hyp_cout_mobilite.objects.get(
        model="Prix véhicule utilitaire + maintenance Thermique")  # €/mois
    Prix_utililaire_thermique = rqt3.valeur

    rqt4 = Hyp_cout_mobilite.objects.get(model="Prix électricité")  # €/mois
    Prix_electricite = rqt4.valeur

    rqt5 = Hyp_cout_mobilite.objects.get(
        model="Prix carburant initial")  # €/mois
    Prix_carburant_initial = rqt5.valeur

    rqt6 = Hyp_cout_mobilite.objects.get(
        model="Augmentation prix électricité")  # €/mois
    Augmentation_prix_electricite = rqt6.valeur

    rqt7 = Hyp_cout_mobilite.objects.get(
        model="Augmentation prix carburant")  # €/mois
    Augmentation_prix_carburant = rqt7.valeur

    rqt8 = Hyp_cout_mobilite.objects.get(
        model="Consommation véhicule Electrique")  # kWh/100km
    Consommation_vehicule_electrique = rqt8.valeur

    rqt9 = Hyp_cout_mobilite.objects.get(
        model="Consommation véhicule Thermique")  # L/100km
    Consommation_vehicule_thermique = rqt9.valeur

    rqt10 = Hyp_cout_mobilite.objects.get(
        model="Consommation utilitaire Electrique")  # kWh/100km
    Consommation_utilitaire_electrique = rqt10.valeur

    rqt11 = Hyp_cout_mobilite.objects.get(
        model="Consommation utilitaire Thermique")  # L/100km
    Consommation_utilitaire_thermique = rqt11.valeur

    rqt12 = EZ_DRIVE.objects.get(model="Prix borne simple PRIVATE")  # €/mois
    Prix_borne_simple_PRIVATE = rqt12.valeur

    rqt13 = EZ_DRIVE.objects.get(model="Prix borne double PRIVATE")  # €/mois
    Prix_borne_double_PRIVATE = rqt13.valeur

    rqt14 = EZ_DRIVE.objects.get(model="Prix borne simple PUBLIC")  # €/mois
    Prix_borne_simple_PUBLIC = rqt14.valeur

    rqt15 = EZ_DRIVE.objects.get(model="Prix borne double PUBLIC")  # €/mois
    Prix_borne_double_PUBLIC = rqt15.valeur

    Investissement_initial_borne_simple_PRIVATE = rqt12.invest  # €
    Investissement_initial_borne_simple_PUBLIC = rqt14.invest  # €
    Investissement_initial_borne_double_PRIVATE = rqt13.invest  # €
    Investissement_initial_borne_double_PUBLIC = rqt15.invest  # €

    rqt16 = EZ_DRIVE.objects.get(
        model="Bénéfice revente électricité borne PUBLIC")  # €/KWh
    Benefice_revente_elec = rqt16.valeur

    rqt17 = EZ_DRIVE.objects.get(
        model="Estimation conso extérieur borne PUBLIC")  # €/mois
    Estim_conso_borne = rqt17.valeur

    rqt18 = EZ_DRIVE.objects.get(model="Abonnement EZ-Drive 150km")  # €/mois
    Abonnement_EZ_Drive_150km = rqt18.valeur

    rqt19 = EZ_DRIVE.objects.get(model="Abonnement EZ-Drive 300km")  # €/mois
    Abonnement_EZ_Drive_300km = rqt19.valeur

    rqt20 = EZ_DRIVE.objects.get(model="Abonnement EZ-Drive 600km")  # €/mois
    Abonnement_EZ_Drive_600km = rqt20.valeur

    rqt21 = Emisission_CO2.objects.get(territ="Litre d'essence")  # kg CO2/L
    emission_L_essence = rqt21.emission

    rqt22 = Hyp_cout_mobilite.objects.get(
        model="Equivalence en kWh litre d'essence")  # kWh/L
    kwh_L_essence = rqt22.valeur
