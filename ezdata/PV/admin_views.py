from django.template import RequestContext
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.apps import apps

from django.forms import formset_factory


import django.contrib.admin
from .models import *
from .facturation import total_HA
from .forms import *
from .solutions import solution, solution_GT, calcul_taux_centraleGT

from .custom_centrale import calcul_taux_centraleGT_custom, surface_range
from .dimens_centrale import courbe_de_charges
import numpy as np
from django.contrib import messages
from .devis import *

# A changer dynamiquement
panneau = 'SUNERG X-HALF CUT 375Wc'

# Hypthèses : A ajouter dans une base de données
Rendement_batteries_Lithium = 0.95
Decharge_maximale_batteries_Lithium = 0.8
Perte1 = 0.05  # %


def find_nearest_idx(array, value):
    # Stack Overflow
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx


def find_nearest(array, value):
    # Stack Overflow
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]


@staff_member_required
def dimens_centrale_admin(request, id):
    site = 1

    # Tailles standards de batteries et de centrales issues de Tailles_standards

    rqt_centrales = Tailles_Standards.objects.filter(
        catag='Centrale').values_list('taille')
    vals_centrale = np.array(rqt_centrales).flatten().tolist()

    rqt_batteries = Tailles_Standards.objects.filter(
        catag='Batterie').values_list('taille')
    vals_batterie = np.array(rqt_batteries).flatten().tolist()

    etat_batterie = False
    etat_AutoProd = False
    etat_AutoConso = True
    etat_entre_deux = False
    etat_revente = False

    # Note : Il faut conserver les etats des checkbox a chaque lancement de simulation : DONC creation de variables d'états

 # Infos conso client

    # rqt0 --> Objet : client
    rqt0 = Client.objects.get(pk=id)

    # rqt1 --> Objet : Enseigne

    rqt1 = Enseigne.objects.get(client=rqt0)

    nb = rqt1.nb_sites

    range_nb = range(nb)

    # rqt2 --> Objet : Bâtiment

    rqt2 = Batiment.objects.filter(enseigne=rqt1).filter(num_sites=site)[0]

    # Pour plusieurs sites : différents résultats

    # Resultats pour 1 Bâtiment
    rqt3 = Localisation.objects.get(batiment=rqt2)
    territ = rqt3.territ

    rqt4 = Profil.objects.get(batiment=rqt2)
    profil = rqt4.type_profil

    rqt5 = Toiture.objects.get(batiment=rqt2)
    surface = rqt5.surface
    toiture = rqt5.toiture

    rqt6 = EDF.objects.get(batiment=rqt2)
    puissance = rqt6.puissance
    Nb_kW = rqt6.nb_kW
    ref = rqt6.reference

    if ref == 'Bimestrielle':
        conso_perso = ((Nb_kW * 6) / 365) * 7
    if ref == 'Mensuelle':
        conso_perso = ((Nb_kW * 12) / 365) * 7
    if ref == 'Annuelle':
        conso_perso = ((Nb_kW) / 365) * 7

    rqt7 = Electrification.objects.get(souscription=rqt6)
    installation = rqt7.installation

    centrale_outil = solution_GT(panneau, conso_perso, profil, territ, surface,
                                 installation, puissance, etat_batterie, etat_AutoProd, etat_entre_deux)[0]
    surface_outil = solution_GT(panneau, conso_perso, profil, territ, surface,
                                installation, puissance, etat_batterie, etat_AutoProd, etat_entre_deux)[2]
    batterie_outil = solution_GT(panneau, conso_perso, profil, territ, surface,
                                 installation, puissance, etat_batterie, etat_AutoProd, etat_entre_deux)[4]

    print(centrale_outil)

    # Donner des valeurs initiales pour les variables avant de les modifier dans le POST
    centrale_custom = find_nearest(vals_centrale, centrale_outil)
    batterie_custom = find_nearest(vals_batterie, batterie_outil)
    print(centrale_custom)
    surface_custom = surface_outil

    taux_autoconso = calcul_taux_centraleGT_custom(
        centrale_outil, batterie_outil, panneau, conso_perso, profil, territ, surface, installation, puissance, True)[1]
    taux_autoprod = calcul_taux_centraleGT_custom(
        centrale_outil, batterie_outil, panneau, conso_perso, profil, territ, surface, installation, puissance, True)[2]

    index_batterie = 0

    index_centrale = find_nearest_idx(vals_centrale, centrale_outil)

 # GRAPHIQUES :
 # Courbes de charges
 # Jour Ouvré
    surface_batterie = np.zeros((24, 1), float)
    surface_batterie_weekend = np.zeros((24, 1), float)
    ouvre_batterie = np.zeros((24, 1), float)
    weekend_batterie = np.zeros((24, 1), float)

    coeffs_ouvre = courbe_de_charges(conso_perso, profil)[0] / 1000
    # Pour afficher les courbes dans le bon format

    out = np.array(coeffs_ouvre).flatten().tolist()

    tab = calcul_taux_centraleGT(panneau, conso_perso, profil, territ, surface,
                                 installation, puissance, etat_batterie, etat_AutoProd, etat_entre_deux)[0]

    result1 = tab[:, 1] / 1000
    out1 = np.array(result1).flatten().tolist()

    surface_graph = np.zeros((24, 1), float)
    for i in range(24):
        surface_graph[i] = min(result1[i], coeffs_ouvre[i])
    surface_graph = surface_graph.flatten().tolist()

    # Weekend

    coeffs_ouvre1 = courbe_de_charges(conso_perso, profil)[1] / 1000
    # Pour afficher les courbes dans le bon format

    out2 = np.array(coeffs_ouvre1).flatten().tolist()
    surface_graph1 = np.zeros((24, 1), float)
    for i in range(24):
        surface_graph1[i] = min(result1[i], coeffs_ouvre1[i])
    surface_graph1 = surface_graph1.flatten().tolist()

    conso_reseau = np.zeros((24, 1), float)

    conso_reseau_weekend = np.zeros((24, 1), float)

    form = Dimens_Centrale(data=request.POST)

    # Determiner l'heure du coucher de soleil en fonction du territoire :
    coucher_soleil = int(territ.h_soleil + territ.h_ensol)

    if request.method == "POST":
        # Compteur permettant d'arreter le stockage de la batterie lorsqu'elle est rempli : idéalement : sans decharge
        compteur_ideal = 0

        # Compteur de l'état réelle de la batterie en prenant en considération le rendement
        compteur_reel = 0

        index_batterie = request.POST.get('Batteries')
        index_centrale = request.POST.get('Centrale')

        if 'Site' in request.POST:
            site = request.POST.get('site')

        rqt2 = Batiment.objects.filter(enseigne=rqt1).filter(num_sites=site)[0]

        # Pour plusieurs sites : différents résultats

        # Resultats pour 1 Bâtiment
        rqt3 = Localisation.objects.get(batiment=rqt2)
        territ = rqt3.territ

        rqt4 = Profil.objects.get(batiment=rqt2)
        profil = rqt4.type_profil

        rqt5 = Toiture.objects.get(batiment=rqt2)
        surface = rqt5.surface
        toiture = rqt5.toiture

        rqt6 = EDF.objects.get(batiment=rqt2)
        puissance = rqt6.puissance
        Nb_kW = rqt6.nb_kW
        ref = rqt6.reference

        if ref == 'Bimestrielle':
            conso_perso = ((Nb_kW * 6) / 365) * 7
        if ref == 'Mensuelle':
            conso_perso = ((Nb_kW * 12) / 365) * 7
        if ref == 'Annuelle':
            conso_perso = ((Nb_kW) / 365) * 7

        rqt7 = Electrification.objects.get(souscription=rqt6)
        installation = rqt7.installation

        if "Auto_Prod" in request.POST:
            # Checkbox was checked
            etat_AutoProd = True
            etat_AutoConso = False
            etat_entre_deux = False

        if "Auto_Conso" in request.POST:
            # Checkbox was checked
            etat_AutoProd = False
            etat_AutoConso = True
            etat_entre_deux = False
        if "Entre_les_deux" in request.POST:
            # Checkbox was checked
            etat_AutoProd = False
            etat_AutoConso = False
            etat_entre_deux = True
        if "choix_batterie" in request.POST:
            # Checkbox was checked
            etat_batterie = True
        if index_batterie == None:
            index_batterie = 0

        centrale_custom = vals_centrale[int(index_centrale)]
        batterie_custom = vals_batterie[int(index_batterie)]

        centrale_outil = solution_GT(panneau, conso_perso, profil, territ, surface, installation, puissance, etat_batterie, etat_AutoProd,
                                     etat_entre_deux)[0]
        surface_outil = solution_GT(panneau, conso_perso, profil, territ, surface, installation, puissance, etat_batterie, etat_AutoProd,
                                    etat_entre_deux)[2]
        batterie_outil = solution_GT(panneau, conso_perso, profil, territ, surface, installation, puissance, etat_batterie, etat_AutoProd,
                                     etat_entre_deux)[4]

        taux_autoconso = calcul_taux_centraleGT_custom(
            centrale_custom, batterie_custom, panneau, conso_perso, profil, territ, surface, installation, puissance, etat_batterie)[1]
        taux_autoprod = calcul_taux_centraleGT_custom(
            centrale_custom, batterie_custom, panneau, conso_perso, profil, territ, surface, installation, puissance, etat_batterie)[2]
        surface_custom = surface_range(centrale_custom, panneau)

        # GRAPHIQUES :
        # Courbes de charges
        # Jour Ouvré

        coeffs_ouvre = courbe_de_charges(conso_perso, profil)[0] / 1000
        # Pour afficher les courbes dans le bon format

        # Points de la courbe de charge : Consommation du bâtiment
        out = np.array(coeffs_ouvre).flatten().tolist()

        # Production de la centrale PV
        tab = calcul_taux_centraleGT_custom(centrale_custom, batterie_custom, panneau, conso_perso, profil, territ,
                                            surface, installation, puissance, etat_batterie)[0]
        result1 = tab[:, 1] / 1000
        out1 = np.array(result1).flatten().tolist()

        # Energie auto-consommé

        surface_graph = np.zeros((24, 1), float)

        for i in range(24):
            surface_graph[i] = min(result1[i], coeffs_ouvre[i])
        surface_graph = surface_graph.flatten().tolist()

        # Weekend

        coeffs_ouvre1 = courbe_de_charges(conso_perso, profil)[1] / 1000
      # Pour afficher les courbes dans le bon format

        out2 = np.array(coeffs_ouvre1).flatten().tolist()
        surface_graph1 = np.zeros((24, 1), float)
        for i in range(24):
            surface_graph1[i] = min(result1[i], coeffs_ouvre1[i])
        surface_graph1 = surface_graph1.flatten().tolist()

        # 2 options :
        # Utilisation de batteries :
        if etat_batterie:
            residu = np.zeros((24, 1), float)
            for i in range(24):
                residu[i] = result1[i] - surface_graph[i]
            total_residu = np.sum(residu)

            # Compater le résidu avec la capacité de la batterie
            if total_residu > batterie_custom:
                total_residu = batterie_custom

            # Apres le chargement de la batterie en journéee
            for i in range(coucher_soleil, 24):
                if compteur_ideal < total_residu:
                    if result1[i] < 0.001:  # Si la production de la centrale est inférieur à 1Wc
                        surface_batterie[i] = coeffs_ouvre[i] * \
                            Rendement_batteries_Lithium

                        # La batterie ne peut pas fournir plus que la moitie de sa capacité en instantanée
                        if surface_batterie[i] >= batterie_custom / 2:
                            surface_batterie[i] = (
                                batterie_custom / 2) * Rendement_batteries_Lithium
                            compteur_ideal = compteur_ideal + \
                                surface_batterie[i]

                        if surface_batterie[i] < batterie_custom / 2:
                            compteur_ideal = compteur_ideal + coeffs_ouvre[i]

                        compteur_reel = compteur_reel + surface_batterie[i]

            # Dechargement avant le lever de soleil
            for i in range(0, coucher_soleil):
                if compteur_ideal < total_residu:
                    if result1[i] < 0.001:  # Si la production de la centrale est inférieur à 1Wc
                        surface_batterie[i] = coeffs_ouvre[i] * \
                            Rendement_batteries_Lithium

                        # La batterie ne peut pas fournir plus que la moitie de sa capacité en instantanée
                        if surface_batterie[i] >= batterie_custom / 2:
                            surface_batterie[i] = batterie_custom / 2
                        compteur_ideal = compteur_ideal + coeffs_ouvre[i]

                        compteur_reel = compteur_reel + surface_batterie[i]

            surface_batterie = surface_batterie.flatten().tolist()

            # Weekend

            residu_weekend = np.zeros((24, 1), float)
            for i in range(24):
                residu_weekend[i] = result1[i] - surface_graph1[i]
            total_residu_weekend = np.sum(residu_weekend)

            # Compater le résidu avec la capacité de la batterie
            if total_residu_weekend > batterie_custom:
                total_residu_weekend = batterie_custom

            # Apres le chargement de la batterie en journéee
            for i in range(coucher_soleil, 24):
                if compteur_ideal < total_residu_weekend:
                    if result1[i] < 0.001:  # Si la production de la centrale est inférieur à 1Wc
                        surface_batterie_weekend[i] = coeffs_ouvre1[i] * \
                            Rendement_batteries_Lithium

                        # La batterie ne peut pas fournir plus que la moitie de sa capacité en instantanée
                        if surface_batterie_weekend[i] >= batterie_custom / 2:
                            surface_batterie_weekend[i] = (
                                batterie_custom / 2) * Rendement_batteries_Lithium
                            compteur_ideal = compteur_ideal + \
                                surface_batterie_weekend[i]

                        if surface_batterie_weekend[i] < batterie_custom / 2:
                            compteur_ideal = compteur_ideal + coeffs_ouvre1[i]

                        compteur_reel = compteur_reel + \
                            surface_batterie_weekend[i]

            # Dechargement avant le lever de soleil
            for i in range(0, coucher_soleil):
                if compteur_ideal < total_residu_weekend:
                    if result1[i] < 0.001:  # Si la production de la centrale est inférieur à 1Wc
                        surface_batterie_weekend[i] = coeffs_ouvre1[i] * \
                            Rendement_batteries_Lithium

                        # La batterie ne peut pas fournir plus que la moitie de sa capacité en instantanée
                        if surface_batterie_weekend[i] >= batterie_custom / 2:
                            surface_batterie_weekend[i] = batterie_custom / 2
                        compteur_ideal = compteur_ideal + coeffs_ouvre1[i]

                        compteur_reel = compteur_reel + \
                            surface_batterie_weekend[i]

            surface_batterie_weekend = surface_batterie_weekend.flatten().tolist()

            # Graphiques :

            # Stockage batterie jour ouvré

            ouvre_nuageux = tab[:, 8]
            print(ouvre_nuageux)

            ouvre_soleil = tab[:, 9]
            print(ouvre_soleil)

            weekend_nuageux = tab[:, 10]
            print(weekend_nuageux)

            weekend_soleil = tab[:, 11]
            print(weekend_soleil)

            for i in range(24):
                ouvre_batterie[i] = (ouvre_nuageux[i]+ouvre_soleil[i])/2
                weekend_batterie[i] = (weekend_nuageux[i]+weekend_soleil[i])/2

            ouvre_batterie = ouvre_batterie.flatten().tolist()
            weekend_batterie = weekend_batterie.flatten().tolist()

            # Stockage batterie weekend

            # Ce qui reste à récuperer sur le réseau
        for i in range(24):
            conso_reseau[i] = coeffs_ouvre[i] - \
                surface_graph[i] - surface_batterie[i]
            conso_reseau_weekend[i] = coeffs_ouvre1[i] - \
                surface_graph1[i] - surface_batterie_weekend[i]
            if conso_reseau[i] < 0:
                conso_reseau[i] = 0
            if conso_reseau_weekend[i] < 0:
                conso_reseau_weekend[i] = 0

        conso_reseau = conso_reseau.flatten().tolist()
        conso_reseau_weekend = conso_reseau_weekend.flatten().tolist()


# Pas de batteries

    centrale_outil = round(centrale_outil, 2)
    batterie_outil = round(batterie_outil, 2)
    surface_outil = round(surface_outil, 2)
    taux_autoconso = round(taux_autoconso, 2)
    taux_autoprod = round(taux_autoprod, 2)
    surface_custom = round(surface_custom, 2)
    surface = round(surface * 0.96, 2)

# Aller chercher l'id du modèle Catalogue pour faire le devis !!!
    id_catalogue = Catalogue_GT.objects.filter(
        tailles=centrale_custom).filter(toiture=toiture).values('id')

    if 'Submit' in request.POST:
        url = reverse('devis', kwargs={
                      'id_client': id, 'standard_centrale': centrale_custom, 'standard_batterie': batterie_custom})

        return HttpResponseRedirect(url)

    return render(request, 'admin/commerciaux/dimens_centrale.html', {'id_client': id, 'site': site, 'nb': range_nb, 'form': form, 'centrale_GT': centrale_outil, 'batteries_GT': batterie_outil, 'surface_GT': surface_outil,
                                                                      'curseur_batterie': index_batterie, 'curseur_centrale': index_centrale, 'standard_centrale': centrale_custom, 'standard_batterie': batterie_custom,
                                                                      'etat_AutoProd': etat_AutoProd, 'etat_AutoConso': etat_AutoConso, 'etat_entre_deux': etat_entre_deux,
                                                                      'etat_batterie': etat_batterie, 'etat_revente':  etat_revente, 'Taux_Autoconso': taux_autoconso, 'Taux_Autoprod': taux_autoprod, 'Toiture': surface, 'Surface_Custom': surface_custom,
                                                                      'graph1': out, 'graph2': out1, 'graph3': surface_graph, 'graph4': surface_batterie, 'EDF': conso_reseau,
                                                                      'graph5': out2, 'graph6': surface_graph1, 'graph7': surface_batterie_weekend, 'EDF_1': conso_reseau_weekend,
                                                                      'stockage_ouvre': ouvre_batterie, 'stockage_weekend': weekend_batterie, 'id_catalogue': id_catalogue})


def devis(request, id, centrale, batterie):
    global formA
    site = 1

    # rqt0 --> Objet : client
    rqt0 = Client.objects.get(pk=id)

    # rqt1 --> Objet : Enseigne

    rqt1 = Enseigne.objects.get(client=rqt0)

    nb = rqt1.nb_sites

    range_nb = range(nb)

    # rqt2 --> Objet : Bâtiment

    centrale_devis = Tailles_Standards.objects.filter(
        taille=centrale).filter(catag='Centrale')[0]
    batterie_devis = Tailles_Standards.objects.filter(
        taille=batterie).filter(catag='Batterie')

    # rqt2 = Batiment.objects.filter(enseigne=rqt1).filter(num_sites=site)[0]

    formset_panneau = formset_factory(Invoice_ModulesPV)

    if request.method == "POST":
        if 'Site' in request.POST:
            site = request.POST.get('site')

        rqt2 = Batiment.objects.filter(
            enseigne=rqt1).filter(num_sites=site)[0]

        rqt5 = Toiture.objects.get(batiment=rqt2)
        toiture = rqt5.toiture

        rqt6 = Localisation.objects.get(batiment=rqt2)
        territ = rqt6.territ

        # Recuperer une liste de Modules PV facturés
        panneaux = Modules(rqt0, rqt2, centrale_devis, toiture, territ)

        if 'Enregistrer' in request.POST:
            forms_panneau = formset_panneau(request.POST, request.FILES)

            forms_panneau_isvalid = forms_panneau.is_valid()

            if (forms_panneau_isvalid):
                forms_panneau.save()

            else:
                messages.error(request, "Error")
                print(forms_panneau.errors)

    else:
        # rqt2 = Batiment.objects.filter(
        #     enseigne=rqt1).filter(num_sites=site)[0]

        # rqt5 = Toiture.objects.get(batiment=rqt2)
        # toiture = rqt5.toiture

        # rqt6 = Localisation.objects.get(batiment=rqt2)
        # territ = rqt6.territ

        # # Recuperer une liste de Modules PV facturés
        # panneaux = Modules(rqt0, rqt2, centrale_devis, toiture, territ)

        forms_panneau = formset_panneau()

    return render(request, 'admin/change_form_factu.html', {'id_client': id, 'standard_centrale': centrale, 'standard_batterie': batterie, 'Panneaux': forms_panneau})
