# coding=utf-8
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.db import transaction
from django.contrib import messages

from .catalogue import *
from .custom_centrale import *

from .solutions import *
from .forms import *
from .models import *

from .dimens_centrale import *
import numpy as np
from .facturation import *
from .MDE import *
from .mobilite import *
from .models import *
from .Bilan_final import *
from .catalogue import *

from .gps import *

# importing the necessary libraries
from django.template.loader import get_template
from xhtml2pdf import pisa

from django.contrib.auth.decorators import login_required

import xlwt

# Creating a class based view

from django.template.defaulttags import register


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


def render_pdf_view(request, id_enseigne, templatepath, nsite):

    template_path = templatepath

    site = nsite

    if templatepath == 'rapport_pdf.html':

        rqt2 = Enseigne.objects.get(id=id_enseigne)
        rqt1 = rqt2.user
        name = rqt2.name

        nom_entreprise = rqt1.entite
        mail = rqt1.email
        nb_sites = rqt2.nb_sites
        nb = range(1, int(nb_sites)+1)

        Economique_mde_multi, Economique_pv_multi, Economique_mobilite_multi, Total_Economique_multi, Environnement_mde_multi, Environnement_pv_multi, Environnement_mobilite_multi, Total_Environnement_multi, Energie_mde_multi, Energie_pv_multi, Total_Energie_multi, coeff_un_multi, coeff_deux_multi, coeff_trois_multi, emission_sans_action_multi = data_multi_sites(
            id_enseigne)

        taille = {}
        nbr_modules = {}
        surface_totale = {}
        n_solution = {}
        conso_reseau = {}
        conso_reseau_weekend = {}
        surface = {}
        auto_conso = {}
        auto_prod = {}

        test, p1, p2, p3, p4 = {}, {}, {}, {}, {}

        Economique_mde, Economique_pv, Economique_mobilite, Total_Economique, Environnement_mde, Environnement_pv, Environnement_mobilite, Total_Environnement, Energie_mde, Energie_pv, Total_Energie, coeff_un, coeff_deux, coeff_trois, emission_sans_action = {
        }, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}

        Bilan_Economique, Bilan_Energetique, Bilan_Environnemental, invest, emission_avant, emission_apres = {}, {}, {}, {}, {}, {}

        Bilan_Economique_mobilite, Bilan_Environnemental_mobilite = {}, {}

        for site in nb:

            taille[site], nbr_modules[site], surface_totale[site], n_solution[site], conso_reseau[site], conso_reseau_weekend[
                site], surface[site], auto_conso[site], auto_prod[site] = data_results_site(id_enseigne, site)

            test[site], p1[site], p2[site], p3[site], p4[site] = data_factu_site(
                id_enseigne, site)

            Economique_mde[site], Economique_pv[site], Economique_mobilite[site], Total_Economique[site], Environnement_mde[site], Environnement_pv[site], Environnement_mobilite[site], Total_Environnement[
                site], Energie_mde[site], Energie_pv[site], Total_Energie[site], coeff_un[site], coeff_deux[site], coeff_trois[site], emission_sans_action[site] = data_bilan_site(id_enseigne, site)

            Bilan_Economique[site], Bilan_Energetique[site], Bilan_Environnemental[site], invest[site], emission_avant[site], emission_apres[site] = data_mde_site(
                id_enseigne, site)

            Bilan_Economique_mobilite[site], Bilan_Environnemental_mobilite[site] = data_mobilite_site(
                id_enseigne, site)

        context = {'name': name, 'nom_entreprise': nom_entreprise, 'mail': mail, 'id_enseigne': id_enseigne,
                   'nb': nb, 'nb_sites': nb_sites,
                   'taille': taille, 'nb_modules': nbr_modules, 'surface': surface_totale,
                   'n': n_solution, 'EDF': conso_reseau, 'EDF_1': conso_reseau_weekend,
                   'surface1': surface, 'autoconso': auto_conso, 'autoprod': auto_prod,
                   'module': test, 'totalHA': p1, 'totalTransport': p2,
                   'totalMarge': p3, 'totalPrix': p4,
                   'un': Economique_mde, 'deux': Economique_pv, 'trois': Economique_mobilite,
                   'quatre': Total_Economique, 'cinq': Environnement_mde, 'six': Environnement_pv,
                   'sept': Environnement_mobilite, 'huit': Total_Environnement, 'neuf': Energie_mde,
                   'dix': Energie_pv, 'onze': Total_Energie, 'Reduction_MDE': coeff_un,
                   'Reduction_PV': coeff_deux, 'Reduction_Mobilite': coeff_trois, 'Emission_20ans': emission_sans_action,
                   'un_multi': Economique_mde_multi, 'deux_multi': Economique_pv_multi, 'trois_multi': Economique_mobilite_multi,
                   'quatre_multi': Total_Economique_multi, 'cinq_multi': Environnement_mde_multi, 'six_multi': Environnement_pv_multi,
                   'sept_multi': Environnement_mobilite_multi, 'huit_multi': Total_Environnement_multi, 'neuf_multi': Energie_mde_multi,
                   'dix_multi': Energie_pv_multi, 'onze_multi': Total_Energie_multi, 'Reduction_MDE_multi': coeff_un_multi,
                   'Reduction_PV_multi': coeff_deux_multi, 'Reduction_Mobilite_multi': coeff_trois_multi, 'Emission_20ans_multi': emission_sans_action_multi,
                   'bilan1': Bilan_Economique, 'bilan2': Bilan_Energetique, 'bilan3': Bilan_Environnemental, 'Investissement': invest,
                   'emissions_avant': emission_avant, 'emission_apres': emission_apres,
                   'bilan1_mobilite': Bilan_Economique_mobilite, 'bilan3_mobilite': Bilan_Environnemental_mobilite}

    elif templatepath == 'dashboard_2_pdf.html':
        site, range_nb, taille, nbr_modules, surface_totale, n_solution, out, out1, surface_graph, conso_reseau, out2, surface_graph1, conso_reseau_weekend, surface, auto_conso, auto_prod = data_results(
            id_enseigne, nsite)
        rqt2 = Enseigne.objects.get(id=id_enseigne)
        rqt1 = rqt2.user
        nom_entreprise = rqt1.entite
        mail = rqt1.email
        context = {'nom_entreprise': nom_entreprise, 'mail': mail, 'id_enseigne': id_enseigne, 'site': site, 'nb': range_nb, 'taille': taille, 'nb_modules': nbr_modules, 'surface': surface_totale, 'n': n_solution,
                   'graph1': out, 'graph2': out1, 'graph3': surface_graph, 'EDF': conso_reseau, 'graph4': out2,
                   'graph5': surface_graph1, 'EDF_1': conso_reseau_weekend, 'surface1': surface, 'autoconso': auto_conso,
                   'autoprod': auto_prod}
    elif templatepath == 'factu_pdf.html':
        site, range_nb, test, p1, p2, p3, p4 = data_factu(id_enseigne, nsite)
        rqt2 = Enseigne.objects.get(id=id_enseigne)
        rqt1 = rqt2.user
        nom_entreprise = rqt1.entite
        mail = rqt1.email
        context = {'nom_entreprise': nom_entreprise, 'mail': mail, 'id_enseigne': id_enseigne, 'site': site, 'nb': range_nb, 'module': test,
                   'totalHA': p1, 'totalTransport': p2, 'totalMarge': p3, 'totalPrix': p4}

    id = id_enseigne

    s = '-site-'+str(site)

    response = HttpResponse(content_type='application/pdf')
    if not templatepath == 'rapport_pdf.html':
        filename = 'Préconfiguration-'+templatepath[:-9]+'-'+str(id)+s+'.pdf'
    else:
        filename = 'Préconfiguration-'+str(id)+'.pdf'

    response['Content-Disposition'] = 'attachment; filename="%s"' % filename
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)
    if not pisa_status.err:
        return response
    else:
        return None


Batteries = False

run_once = 0
global id_enseigne


# à changer en fonction des choix de GreenTech
etat_AutoProd = False
etat_AutoConso = True
etat_entre_deux = False
etat_batterie = False
etat_revente = False


def welcome(request):
    return render(request, 'welcome.html')


@login_required
def test(request):
    # global formA
    global formB

    nom_entreprise = request.user.entite
    email = request.user.email

    if request.method == 'POST':
        # form_client = ClientForm(data=request.POST)

        form_enseigne = EnseigneForm(data=request.POST)

        # form_client_valid = form_client.is_valid()
        form_enseigne_valid = form_enseigne.is_valid()

        # Verification de la validité des données
        # if (form_client_valid and form_enseigne_valid):
        if form_enseigne_valid:

            # instance = form_client.save()

            # if Client.objects.filter(mail=request.user.email).exists():
            #     instance = Client.objects.get(mail=request.user.email)
            # else:
            #     instance = Client(
            #         nom_entreprise=nom_entreprise, mail=request.user.email)
            #     instance.save()

            instance = request.user

            instance1 = form_enseigne.save(commit=False)

            # instance1.client = instance
            instance1.user = instance

            form_enseigne.save()

            # Enregistrer toutes les infos du client pour les utiliser dans les autres vues
            # request.session['nom_entreprise'] = form_client.cleaned_data['nom_entreprise']
            # nom = request.session['nom_entreprise']

            # rqt0 --> Objet : client
            # rqt0 = Client.objects.get(nom_entreprise=nom)

            id_enseigne = instance1.id

            url = reverse('batiments', kwargs={'id_enseigne': id_enseigne})

            return HttpResponseRedirect(url)
        else:
            messages.error(request, "Error")
            print(form_enseigne.errors)

    else:
        # formA = ClientForm()
        formB = EnseigneForm()

    return render(request, 'wizard-create-profile.html', {'formB': formB, 'nom_entreprise': nom_entreprise, 'email': email})


@login_required
def test_exists(request, id_enseigne):
    global formB
    global nb_sites

    nom_entreprise = request.user.entite
    email = request.user.email

    rqt = Enseigne.objects.get(id=id_enseigne)
    old_nb = rqt.nb_sites

    nb_sites = old_nb

    formB = EnseigneForm(instance=rqt)

    if request.method == 'POST':
        if 'next' in request.POST:
            form_enseigne = EnseigneForm(data=request.POST, instance=rqt)

            form_enseigne_valid = form_enseigne.is_valid()

            if form_enseigne_valid:
                # if Client.objects.filter(mail=request.user.email).exists():
                #     instance = Client.objects.get(mail=request.user.email)
                # else:
                #     instance = Client(
                #         nom_entreprise=nom_entreprise, mail=request.user.email)
                #     instance.save()

                instance = request.user

                instance1 = form_enseigne.save(commit=False)

                instance1.user = instance

                form_enseigne.save()

                id_enseigne = instance1.id

                # suppression des sites à cause de la mise à jour du nombre de sites
                rqt = Enseigne.objects.get(id=id_enseigne)
                nb = rqt.nb_sites
                for i in range(1, old_nb+1):
                    if i not in range(1, nb+1):
                        Batiment.objects.filter(enseigne=rqt).filter(
                            num_sites=i).delete()

                url = reverse('batiments', kwargs={'id_enseigne': id_enseigne})

                return HttpResponseRedirect(url)
            else:
                messages.error(request, "Error")
                print(form_enseigne.errors)

        if 'Précédent' in request.POST:
            url = reverse('profile')

            return HttpResponseRedirect(url)

    return render(request, 'wizard-create-profile.html', {'formB': formB, 'nom_entreprise': nom_entreprise, 'email': email, 'nb_sites': nb_sites})


@login_required
def batiments(request, id_enseigne):
    global formC
    global formE
    global formF
    global formG
    global site

    global sites_ok

    etat_next = False

    etat_form = False

    rqt1 = Enseigne.objects.get(id=id_enseigne)

    nb = rqt1.nb_sites

    range_nb = range(nb)

    if request.method == "POST":

        if 'Site' in request.POST:
            site = request.POST.get('site')

            etat_form = True

            # Modification d'un formulaire
        if Batiment.objects.filter(enseigne=rqt1).filter(num_sites=site).exists():

            rqt5 = Batiment.objects.filter(
                enseigne=rqt1).filter(num_sites=site)

            bat = rqt5[0]
            formG = BatimentForm(instance=bat)

            rqt6 = Localisation.objects.get(batiment=bat)

            rqt7 = Profil.objects.get(batiment=bat)
            rqt8 = Toiture.objects.get(batiment=bat)

            formC = LocalisationForm(instance=rqt6)
            formE = ProfilForm(instance=rqt7)
            formF = ToitureForm(instance=rqt8)

            if 'Enregistrer' in request.POST:

                print('enregistrement')

                form_loca = LocalisationForm(data=request.POST, instance=rqt6)
                form_profil = ProfilForm(data=request.POST, instance=rqt7)
                form_batiment = BatimentForm(data=request.POST, instance=bat)
                form_toiture = ToitureForm(data=request.POST, instance=rqt8)

                form_loca_valid = form_loca.is_valid()
                form_profil_valid = form_profil.is_valid()
                form_batiment_valid = form_batiment.is_valid()
                form_toiture_valid = form_toiture.is_valid()

                # Verification de la validité des données
                if (form_batiment_valid and form_loca_valid and form_profil_valid and form_toiture_valid):

                    instance2 = form_batiment.save(commit=False)
                    instance2.num_sites = site

                    form_batiment.save()

                    form_loca.save()
                    form_profil.save()
                    form_toiture.save()

                    etat_form = False
                    print('enregistré')

                    if site not in sites_ok:
                        sites_ok.append(site)

                    if len(sites_ok) == nb:
                        etat_next = True

                else:
                    messages.error(request, "Error")
                    print(form_loca.errors)
                    print(form_profil.errors)
                    print(form_batiment.errors)
                    print(form_toiture.errors)

        if not Batiment.objects.filter(enseigne=rqt1).filter(num_sites=site).exists():

            formC = LocalisationForm()
            formE = ProfilForm()
            formF = ToitureForm()
            formG = BatimentForm()

            if 'Enregistrer' in request.POST:

                form_loca = LocalisationForm(data=request.POST)
                form_profil = ProfilForm(data=request.POST)
                form_batiment = BatimentForm(data=request.POST)
                form_toiture = ToitureForm(data=request.POST)

                form_loca_valid = form_loca.is_valid()
                form_profil_valid = form_profil.is_valid()
                form_batiment_valid = form_batiment.is_valid()
                form_toiture_valid = form_toiture.is_valid()

                # Verification de la validité des données
                if (form_batiment_valid and form_loca_valid and form_profil_valid and form_toiture_valid):

                    instance2 = form_batiment.save(commit=False)
                    instance3 = form_loca.save(commit=False)
                    instance5 = form_profil.save(commit=False)
                    instance6 = form_toiture.save(commit=False)

                    instance2.enseigne = rqt1
                    instance2.num_sites = site

                    instance3.batiment = instance2
                    instance5.batiment = instance2
                    instance6.batiment = instance2

                    form_batiment.save()
                    form_loca.save()
                    form_profil.save()
                    form_toiture.save()

                    print('saved')

                    etat_form = False

                    if site not in sites_ok:
                        sites_ok.append(site)

                    if len(sites_ok) == nb:
                        etat_next = True

               # id_batiment= form_batiment.id

                # Reinitialiser les formulaires

                else:
                    messages.error(request, "Error")
                    print(form_loca.errors)
                    print(form_profil.errors)
                    print(form_batiment.errors)
                    print(form_toiture.errors)

        if 'Next' in request.POST:

            bat = Batiment.objects.get(enseigne=rqt1, num_sites=site)
            pro = Profil.objects.get(batiment=bat)
            pro_type = Profil_types.objects.get(type_profil='Personnalisé')

            url = reverse('energie', kwargs={'id_enseigne': id_enseigne})

            if pro.type_profil == pro_type:
                url = reverse('personnalise', kwargs={
                              'id_enseigne': id_enseigne})

            return HttpResponseRedirect(url)

        if 'Précédent' in request.POST:
            url = reverse('clients_exists', kwargs={
                          'id_enseigne': id_enseigne})

            return HttpResponseRedirect(url)

    else:

        formC = LocalisationForm()
        formE = ProfilForm()
        formF = ToitureForm()
        formG = BatimentForm()

        site = 1
        sites_ok = []

    return render(request, 'wizard-create-batiments.html', {'id_enseigne': id_enseigne, 'site': site, 'nb': range_nb, 'etat_form': etat_form, 'etat_next': etat_next, 'formC': formC,
                                                            'formE': formE, 'formF': formF, 'formG': formG})


@login_required
def personnalise(request, id_enseigne):
    global formC

    rqt1 = Enseigne.objects.get(pk=id_enseigne)
    site = 1
    bat = Batiment.objects.get(enseigne=rqt1, num_sites=site)
    projet = rqt1.projet

    if request.method == "POST":
        formC = CourbeChargePersoForm()

        if 'Suivant' in request.POST:

            formCo = CourbeChargePersoForm(data=request.POST)
            name = formCo['name'].value()
            type = formCo['type'].value()

            if CourbeChargePerso.objects.filter(
                    projet=projet, name=name, type=type).exists():
                CourbeChargePerso.objects.filter(
                    projet=projet, name=name, type=type).delete()

            if formCo.is_valid():
                courbe1 = formCo.save(commit=False)
                courbe1.projet = projet
                formCo.save()

                if not ProfilTypesPerso.objects.filter(type_profil=name).exists():
                    if type == 'Ouvré':
                        perso = ProfilTypesPerso(type_profil=name)
                        perso.save()

            else:
                messages.error(request, 'Error')
                print(formCo.errors)

        # if 'Suivant' in request.POST:
            url = reverse('profilperso', kwargs={'id_enseigne': id_enseigne})
            return HttpResponseRedirect(url)

        if 'Précédent' in request.POST:
            url = reverse('batiments', kwargs={
                'id_enseigne': id_enseigne})
            return HttpResponseRedirect(url)

    else:
        formC = CourbeChargePersoForm()

    courbe = CourbeDeCharge.objects.get(
        profil=Profil_types.objects.get(type_profil='Tertiaire'), type='Ouvré')
    graph = courbe.coeffs[1:]

    return render(request, 'wizard-personnalise.html', {'graph': graph, 'id_enseigne': id_enseigne, 'formC': formC, 'projet': projet})


@login_required
def profilperso(request, id_enseigne):
    global formP1

    rqt1 = Enseigne.objects.get(pk=id_enseigne)
    site = 1
    bat = Batiment.objects.get(enseigne=rqt1, num_sites=site)
    projet = rqt1.projet

    if request.method == "POST":
        formP1 = ProfilPersoForm()

        if 'Suivant' in request.POST:
            formPr1 = ProfilPersoForm(data=request.POST)

            ProfilPerso.objects.filter(batiment=bat).delete()

            if formPr1.is_valid():
                prof1 = formPr1.save(commit=False)

                prof1.batiment = bat

                formPr1.save()

                url = reverse('energie', kwargs={'id_enseigne': id_enseigne})
                return HttpResponseRedirect(url)

            else:
                messages.error(request, 'Error')
                print(formPr1.errors)

        if 'Précédent' in request.POST:
            url = reverse('personnalise', kwargs={
                'id_enseigne': id_enseigne})
            return HttpResponseRedirect(url)

    else:
        formP1 = ProfilPersoForm()

    return render(request, 'wizard-choix-perso.html', {'id_enseigne': id_enseigne, 'formP1': formP1, 'projet': projet})


@login_required
def energie(request, id_enseigne):
    global formD
    global formH
    global site
    global bat
    global sites_ok

    etat_next = False

    etat_form = False

    rqt1 = Enseigne.objects.get(id=id_enseigne)

    nb = rqt1.nb_sites

    range_nb = range(nb)

    if request.method == 'POST':

        if 'Site' in request.POST:
            site = request.POST.get('site')

            etat_form = True

            rqt2 = Batiment.objects.filter(
                enseigne=rqt1).filter(num_sites=site)
            bat = rqt2[0]

        else:
            site = 1

            etat_form = True

            rqt2 = Batiment.objects.filter(
                enseigne=rqt1).filter(num_sites=site)
            bat = rqt2[0]

        if EDF.objects.filter(batiment=bat).exists():

            print('exists')

            rqt3 = EDF.objects.get(batiment=bat)

            rqt4 = Electrification.objects.get(souscription=rqt3)

            formD = ElectrificationForm(instance=rqt4)

            formH = SouscriptionForm(instance=rqt3)

            if 'Enregistrer' in request.POST:

                print('enregistrement')

                form_elec = ElectrificationForm(
                    data=request.POST, instance=rqt4)
                form_edf = SouscriptionForm(data=request.POST, instance=rqt3)

                form_elec_valid = form_elec.is_valid()
                form_EDF_valid = form_edf.is_valid()

                # Verification de la validité des données
                if (form_elec_valid and form_EDF_valid):

                    form_edf.save()
                    form_elec.save()

                    etat_form = False
                    print('enregistré')

                    if site not in sites_ok:
                        sites_ok.append(site)

                    if len(sites_ok) == nb:
                        etat_next = True

                else:
                    messages.error(request, "Error")
                    print(form_elec.errors)
                    print(form_edf.errors)

        if not EDF.objects.filter(batiment=bat).exists():

            print("n'existe pas")

            formD = ElectrificationForm()
            formH = SouscriptionForm()

            if 'Enregistrer' in request.POST:

                form_elec = ElectrificationForm(data=request.POST)
                form_edf = SouscriptionForm(data=request.POST)

                form_elec_valid = form_elec.is_valid()
                form_EDF_valid = form_edf.is_valid()

                # Verification de la validité des données
                if (form_elec_valid and form_EDF_valid):

                    instance2 = bat
                    instance4 = form_elec.save(commit=False)
                    instance7 = form_edf.save(commit=False)

                    instance4.batiment = instance2
                    instance7.batiment = instance2

                    instance4.souscription = instance7

                    form_edf.save()
                    form_elec.save()

                    print('saved')

                    etat_form = False

                    if site not in sites_ok:
                        sites_ok.append(site)

                    if len(sites_ok) == nb:
                        etat_next = True

                # id_batiment= form_batiment.id

                # Reinitialiser les formulaires

                else:

                    messages.error(request, "Error")

                    print(form_elec.errors)
                    print(form_edf.errors)

        if 'Next' in request.POST:
            url = reverse('mobilite', kwargs={'id_enseigne': id_enseigne})

            return HttpResponseRedirect(url)

        if 'Précédent' in request.POST:
            url = reverse('batiments', kwargs={'id_enseigne': id_enseigne})

            return HttpResponseRedirect(url)

    else:

        formD = ElectrificationForm()
        formH = SouscriptionForm()

        site = 1
        sites_ok = []

    return render(request, 'wizard-create-energie.html', {'id_enseigne': id_enseigne, 'site': site, 'nb': range_nb, 'etat_form': etat_form, 'etat_next': etat_next, 'formD': formD, 'formH': formH})


@login_required
def mobilite(request, id_enseigne):
    global formI
    global site
    global bat
    global sites_ok

    etat_next = False

    etat_form = False

    rqt1 = Enseigne.objects.get(id=id_enseigne)

    nb = rqt1.nb_sites

    range_nb = range(nb)

    if request.method == 'POST':

        if 'Site' in request.POST:
            site = request.POST.get('site')

            etat_form = True

            rqt2 = Batiment.objects.filter(
                enseigne=rqt1, num_sites=site)
            bat = rqt2[0]

        else:
            site = 1

            etat_form = True

            rqt2 = Batiment.objects.filter(
                enseigne=rqt1).filter(num_sites=site)
            bat = rqt2[0]

        if Mobilite.objects.filter(batiment=bat).exists():

            rqt3 = Mobilite.objects.get(batiment=bat)

            formI = MobiliteForm(instance=rqt3)

            if 'Enregistrer' in request.POST:

                print('enregistrement')

                form_mobilite = MobiliteForm(data=request.POST, instance=rqt3)

                form_mobilite_valid = form_mobilite.is_valid()

                # Verification de la validité des données
                if (form_mobilite_valid):

                    form_mobilite.save()

                    etat_form = False

                    print(sites_ok)

                    if site not in sites_ok:
                        sites_ok.append(site)

                    if len(sites_ok) == nb:
                        etat_next = True

                else:
                    messages.error(request, "Error")
                    print(form_mobilite.errors)

        if not Mobilite.objects.filter(batiment=bat).exists():

            print(site)
            print("n'existe pas")

            formI = MobiliteForm()

            if 'Enregistrer' in request.POST:

                form_mobilite = MobiliteForm(data=request.POST)

                form_mobilite_valid = form_mobilite.is_valid()

                # Verification de la validité des données
                if (form_mobilite_valid):

                    instance8 = form_mobilite.save(commit=False)

                    instance8.batiment = bat

                    form_mobilite.save()

                    etat_form = False

                    if site not in sites_ok:
                        sites_ok.append(site)

                    if len(sites_ok) == nb:
                        etat_next = True

                # id_batiment= form_batiment.id

                # Reinitialiser les formulaires

                else:

                    messages.error(request, "Error")

                    print(form_mobilite.errors)

        if 'Next' in request.POST:
            url = reverse('results', kwargs={'id_enseigne': id_enseigne})

            return HttpResponseRedirect(url)

        if 'Précédent' in request.POST:
            url = reverse('energie', kwargs={'id_enseigne': id_enseigne})

            return HttpResponseRedirect(url)

    else:

        formI = MobiliteForm()

        site = 1

        sites_ok = []

    return render(request, 'wizard-create-mobilite.html', {'id_enseigne': id_enseigne, 'site': site, 'nb': range_nb, 'etat_form': etat_form, 'etat_next': etat_next, 'formI': formI})


@login_required
def results_catalogue(request, id_enseigne):
    global site

    site = 1

    rqt1 = Enseigne.objects.get(id=id_enseigne)
    nb = rqt1.nb_sites
    projet = rqt1.projet

    if not ExportSite.objects.filter(enseigne=rqt1).exists():
        exportsite = ExportSite(
            projet=projet, enseigne=rqt1, sitename=rqt1.name)
        exportsite.save()

    else:
        exportsite = ExportSite.objects.get(enseigne=rqt1)

    range_nb = range(nb)

    # Mise à jour de la valeur du site

    rqt2 = Batiment.objects.filter(enseigne=rqt1).filter(num_sites=site)[0]

    # rqt2 --> Objet : Bâtiment

    # Pour plusieurs sites : différents résultats

    # Resultats pour 1 Bâtiment
    rqt3 = Localisation.objects.get(batiment=rqt2)
    territ = rqt3.territ

    rqt4 = Profil.objects.get(batiment=rqt2)
    profil = rqt4.type_profil
    personnalise = Profil_types.objects.get(type_profil='Personnalisé')
    perso = False
    if profil == personnalise:
        perso = True
        profil = ProfilPerso.objects.get(batiment=rqt2).profil

    rqt5 = Toiture.objects.get(batiment=rqt2)
    surface1 = rqt5.surface

    rqt6 = EDF.objects.get(batiment=rqt2)
    puissance = rqt6.puissance
    Nb_kW = rqt6.nb_kW
    ref = rqt6.reference

    rqt7 = Electrification.objects.get(souscription=rqt6)
    installation = rqt7.installation

    if ref == 'Bimestrielle':
        conso_perso = ((Nb_kW * 6) / 365) * 7
    if ref == 'Mensuelle':
        conso_perso = ((Nb_kW * 12) / 365) * 7
    if ref == 'Annuelle':
        conso_perso = ((Nb_kW) / 365) * 7

    sol = solution_catalogue(conso_perso, profil, perso, territ, surface1,
                             installation, puissance, etat_batterie, etat_AutoProd, etat_entre_deux)

    if CentraleBatiment.objects.filter(batiment=rqt2).exists():
        cb = CentraleBatiment.objects.get(batiment=rqt2)
        if SolutionBatiment.objects.filter(centrale_batiment=cb).exists():
            x = SolutionBatiment.objects.get(centrale_batiment=cb)
            sol = x.solution

    if 'Plus' in request.POST:
        sol = change(sol, plus=True)

    if "Moins" in request.POST:
        sol = change(sol, plus=False)

    if "Reset" in request.POST:
        sol = solution_catalogue(conso_perso, profil, perso, territ, surface1,
                                 installation, puissance, etat_batterie, etat_AutoProd, etat_entre_deux)

    CentraleBatiment.objects.filter(batiment=rqt2).delete()
    cb = CentraleBatiment(batiment=rqt2)
    cb.save()
    SolutionBatiment.objects.filter(centrale_batiment=cb).delete()
    x = SolutionBatiment(centrale_batiment=cb, solution=sol)
    x.save()

    choices = FacturationItem.objects.filter(type="Module photovoltaïque")
    choices = [x for x in choices]
    modulepv_qt = ItemQuantite.objects.get(
        catalogue_solution=sol, facturation_item__in=choices)
    modulepv = modulepv_qt.facturation_item
    panneau_name = modulepv.article
    panneau_qt = modulepv_qt.quantite

    panneau = ModulesPV.objects.get(Nom=panneau_name)
    taille = sol.taille
    exportsite.taille_pv = taille
    nbr_modules = panneau_qt
    surface_totale = nbr_modules*panneau.Surface_Panneau_m2

    # JOUR OUVRE

    coeffs_ouvre = courbe_de_charges(conso_perso, profil, perso)[0] / 1000
    # Pour afficher les courbes dans le bon format

    out = np.array(coeffs_ouvre).flatten().tolist()
    tab = calcul_taux_centraleGT_catalogue(conso_perso, profil, perso, territ, surface1,
                                           installation, puissance, etat_batterie, etat_AutoProd, etat_entre_deux, id_enseigne)[0]

    result1 = tab[:, 1] / 1000
    out1 = np.array(result1).flatten().tolist()

    surface_graph = np.zeros((24, 1), float)
    for i in range(24):
        surface_graph[i] = min(result1[i], coeffs_ouvre[i])
    surface_graph = surface_graph.flatten().tolist()

    # WEEKEND

    coeffs_ouvre1 = courbe_de_charges(conso_perso, profil, perso)[1] / 1000
    # Pour afficher les courbes dans le bon format

    out2 = np.array(coeffs_ouvre1).flatten().tolist()
    surface_graph1 = np.zeros((24, 1), float)
    for i in range(24):
        surface_graph1[i] = min(result1[i], coeffs_ouvre1[i])
    surface_graph1 = surface_graph1.flatten().tolist()

    # CONSO RESEAU

    conso_reseau = np.zeros((24, 1), float)
    conso_reseau_weekend = np.zeros((24, 1), float)

    for i in range(24):
        conso_reseau[i] = coeffs_ouvre[i] - surface_graph[i]
        conso_reseau_weekend[i] = coeffs_ouvre1[i] - surface_graph1[i]
        if conso_reseau[i] < 0:
            conso_reseau[i] = 0
        if conso_reseau_weekend[i] < 0:
            conso_reseau_weekend[i] = 0

    conso_reseau = conso_reseau.flatten().tolist()
    conso_reseau_weekend = conso_reseau_weekend.flatten().tolist()

    surface_totale = round(surface_totale, 2)
    auto_conso = calcul_taux_centraleGT_catalogue(conso_perso, profil, perso, territ, surface1,
                                                  installation, puissance, etat_batterie, etat_AutoProd, etat_entre_deux, id_enseigne)[1]
    auto_conso = round(auto_conso, 2)
    auto_prod = calcul_taux_centraleGT_catalogue(conso_perso, profil, perso, territ, surface1,
                                                 installation, puissance, etat_batterie, etat_AutoProd, etat_entre_deux, id_enseigne)[2]
    auto_prod = round(auto_prod, 2)

    alerte_kVA = taille > puissance

    alerte_surface = surface_totale > surface1

    gt = round(dimensionnement_potentiel_centrale_autoconso(
        conso_perso, profil, perso, territ), 2)

    exportsite.save()

    if 'Précédent' in request.POST:
        url = reverse('mobilite', kwargs={'id_enseigne': id_enseigne})

        return HttpResponseRedirect(url)

    return render(request, 'dashboard_2.html',
                  {'alerte_surface': alerte_surface, 'puissance': puissance, 'alerte_kVA': alerte_kVA, 'gt': gt, 'id_enseigne': id_enseigne, 'site': site, 'nb': range_nb, 'taille': taille, 'nb_modules': nbr_modules, 'surface': surface_totale,
                   'graph1': out, 'graph2': out1, 'graph3': surface_graph, 'EDF': conso_reseau, 'graph4': out2,
                   'graph5': surface_graph1, 'EDF_1': conso_reseau_weekend, 'surface1': surface1, 'autoconso': auto_conso,
                   'autoprod': auto_prod})


@login_required
def factu_catalogue(request, id_enseigne):
    global site

    site = 1

    rqt1 = Enseigne.objects.get(id=id_enseigne)
    nb = rqt1.nb_sites
    projet = rqt1.projet

    if not ExportSite.objects.filter(enseigne=rqt1).exists():
        exportsite = ExportSite(
            projet=projet, enseigne=rqt1, sitename=rqt1.name)
        exportsite.save()

    else:
        exportsite = ExportSite.objects.get(enseigne=rqt1)

    range_nb = range(nb)

    rqt2 = Batiment.objects.filter(enseigne=rqt1, num_sites=site)[0]

    # Pour plusieurs sites : différents résultats

    # Resultats pour 1 Bâtiment
    rqt3 = Localisation.objects.get(batiment=rqt2)
    territ = rqt3.territ

    rqt4 = Profil.objects.get(batiment=rqt2)
    profil = rqt4.type_profil
    personnalise = Profil_types.objects.get(type_profil='Personnalisé')
    perso = False
    if profil == personnalise:
        perso = True
        profil = ProfilPerso.objects.get(batiment=rqt2).profil

    rqt5 = Toiture.objects.get(batiment=rqt2)
    surface = rqt5.surface
    toiture = rqt5.toiture

    rqt6 = EDF.objects.get(batiment=rqt2)
    puissance = rqt6.puissance
    Nb_kW = rqt6.nb_kW
    ref = rqt6.reference

    rqt7 = Electrification.objects.get(souscription=rqt6)
    installation = rqt7.installation

    if ref == 'Bimestrielle':
        conso_perso = ((Nb_kW * 6) / 365) * 7
    if ref == 'Mensuelle':
        conso_perso = ((Nb_kW * 12) / 365) * 7
    if ref == 'Annuelle':
        conso_perso = ((Nb_kW) / 365) * 7

    sol = solution_catalogue(conso_perso, profil, perso, territ, surface,
                             installation, puissance, etat_batterie, etat_AutoProd, etat_entre_deux)
    if CentraleBatiment.objects.filter(batiment=rqt2).exists():
        cb = CentraleBatiment.objects.get(batiment=rqt2)
        if SolutionBatiment.objects.filter(centrale_batiment=cb).exists():
            x = SolutionBatiment.objects.get(centrale_batiment=cb)
            sol = x.solution

    choices = FacturationItem.objects.filter(type="Module photovoltaïque")
    choices = [x for x in choices]
    modulepv_qt = ItemQuantite.objects.get(
        catalogue_solution=sol, facturation_item__in=choices)
    modulepv = modulepv_qt.facturation_item
    panneau_name = modulepv.article
    panneau_qt = modulepv_qt.quantite

    panneau = ModulesPV.objects.get(Nom=panneau_name)
    taille = sol.taille
    nbr_modules = panneau_qt
    surface_totale = nbr_modules*panneau.Surface_Panneau_m2

    # méthode avec Modules_factu avant catalogue implémenté
    # Modules_factu.objects.filter(batiment=rqt2).delete()
    # test = facturation_catalogue(
    #     taille, toiture, territ, installation, nbr_modules, rqt2)
    # test = Modules_factu.objects.filter(batiment=rqt2)

    # nouvelle facturation avec catalogue
    test = ItemQuantite.objects.filter(catalogue_solution=sol)

    p1 = sum([x.cout_HA for x in test])
    p2 = sum([x.cout_transport for x in test])
    p3 = sum([x.marge for x in test])
    p4 = sum([x.prix for x in test])

    p1 = round(p1, 2)
    p2 = round(p2, 2)
    p3 = round(p3, 2)
    p4 = round(p4, 2)

    exportsite.invest_pv = p4

    exportsite.save()

    if 'Précédent' in request.POST:
        url = reverse('mobilite', kwargs={'id_enseigne': id_enseigne})

        return HttpResponseRedirect(url)

    return render(request, 'factu_catalogue.html', {'id_enseigne': id_enseigne, 'site': site, 'nb': range_nb, 'elements': test, 'totalHA': p1, 'totalTransport': p2, 'totalMarge': p3, 'totalPrix': p4})


@login_required
def mde(request, id_enseigne):
    global site

    site = 1

    rqt1 = Enseigne.objects.get(id=id_enseigne)

    nb = rqt1.nb_sites

    range_nb = range(nb)

    # Mise à jour de la valeur du site

    rqt2 = Batiment.objects.filter(enseigne=rqt1).filter(num_sites=site)[0]

    Nbreetages = rqt2.nb_etages
    type = rqt2.type_batiment

    # Pour plusieurs sites : différents résultats

    # Resultats pour 1 Bâtiment
    rqt3 = Localisation.objects.get(batiment=rqt2)
    territ = rqt3.territ

    rqt5 = Toiture.objects.get(batiment=rqt2)
    Surfacetoiture = rqt5.surface

    rqt6 = EDF.objects.get(batiment=rqt2)
    NbrekWhfacture = rqt6.nb_kW
    Recurrencefacture = rqt6.reference
    Montantfacture = rqt6.facture

    ancienne_conso = Coeffs_mde(
        NbrekWhfacture, Recurrencefacture, Montantfacture, Surfacetoiture, Nbreetages, type)[0]
    conso_reduite = Coeffs_mde(NbrekWhfacture, Recurrencefacture,
                               Montantfacture, Surfacetoiture, Nbreetages, type)[1]

    difference = Coeffs_mde(NbrekWhfacture, Recurrencefacture,
                            Montantfacture, Surfacetoiture, Nbreetages, type)[3]

    Bilan_Economique = Economies(NbrekWhfacture, Recurrencefacture,
                                 Montantfacture, Surfacetoiture, Nbreetages, type, territ)[0]
    Bilan_Energetique = Economies(NbrekWhfacture, Recurrencefacture,
                                  Montantfacture, Surfacetoiture, Nbreetages, type, territ)[1]
    Bilan_Environnemental = Economies(
        NbrekWhfacture, Recurrencefacture, Montantfacture, Surfacetoiture, Nbreetages, type, territ)[2]

    invest = Invest(NbrekWhfacture, Recurrencefacture,
                    Montantfacture, Surfacetoiture, Nbreetages, type, territ)

    # Calculs pour Emission C02 des Bâtiments
    rqt0 = Emisission_CO2.objects.get(territ=territ)
    emission_coeff = rqt0.emission

    emission_avant_1an = NbrekWhfacture*emission_coeff
    emission_avant_10ans = emission_avant_1an*10
    emission_avant_20ans = emission_avant_10ans*2
    emission_avant = [emission_avant_1an,
                      emission_avant_10ans, emission_avant_20ans]

    emission_apres_1an = emission_avant_1an-Bilan_Environnemental[0]
    emission_apres_10ans = emission_avant_10ans-Bilan_Environnemental[1]
    emission_apres_20ans = emission_avant_20ans - Bilan_Environnemental[2]
    emission_apres = [emission_apres_1an,
                      emission_apres_10ans, emission_apres_20ans]

    if 'Précédent' in request.POST:
        url = reverse('mobilite', kwargs={'id_enseigne': id_enseigne})

        return HttpResponseRedirect(url)

    return render(request, 'mde.html', {'id_enseigne': id_enseigne, 'site': site, 'nb': range_nb, 'courbe1': ancienne_conso, 'courbe2': conso_reduite, 'area': difference,
                                        'bilan1': Bilan_Economique, 'bilan2': Bilan_Energetique, 'bilan3': Bilan_Environnemental, 'Investissement': invest,
                                        'emissions_avant': emission_avant, 'emission_apres': emission_apres})


@login_required
def mobi(request, id_enseigne):
    global site

    site = 1

    rqt1 = Enseigne.objects.get(id=id_enseigne)

    nb = rqt1.nb_sites

    range_nb = range(nb)

    # Mise à jour de la valeur du site

    rqt2 = Batiment.objects.filter(enseigne=rqt1).filter(num_sites=site)[0]

    Nbreetages = rqt2.nb_etages
    type = rqt2.type_batiment

    # Pour plusieurs sites : différents résultats

    # Resultats pour 1 Bâtiment
    rqt3 = Localisation.objects.get(batiment=rqt2)
    territ = rqt3.territ

    rqt4 = Mobilite.objects.get(batiment=rqt2)
    NbreVS = rqt4.vehicule_fonction
    NbkmanVS = rqt4.km_an_vehicule_fonction
    NbreVU = rqt4.vehicule_utilitaire
    NbkmanVU = rqt4.km_an_vehicule_utilitaire
    Presenceparking = rqt4.parking
    Nb_pdc_choisi = rqt4.pt_de_charge
    Accessibilite_parking = rqt4.acces
    Optionborne = rqt4.borne

    rqt5 = EDF.objects.get(batiment=rqt2)
    NbrekWhfacture = rqt5.nb_kW
    Recurrencefacture = rqt5.reference
    Montantfacture = rqt5.facture

    rqt6 = Toiture.objects.get(batiment=rqt2)
    Surfacetoiture = rqt6.surface


# 1er graph : Economies en changant de voiture : passage du thermique a l'eletrique
    courbe1 = Vehicule_thermique_annuel(NbreVS, NbkmanVS, NbreVU, NbkmanVU)[4]
    courbe1 = courbe1.flatten().tolist()

    courbe2 = Vehicule_electrique_annuel(NbreVS, NbkmanVS, NbreVU, NbkmanVU, NbrekWhfacture,
                                         Recurrencefacture, Montantfacture, Surfacetoiture, Nbreetages)[3]

    courbe2_abo = Tableau_Bornes(Presenceparking, Nb_pdc_choisi, Accessibilite_parking,
                                 Optionborne, NbreVS, NbreVU, NbkmanVS, NbkmanVU)[2]

    courbe2_coeffs = courbe2 + courbe2_abo
    courbe2_coeffs = courbe2_coeffs.flatten().tolist()

    courbe4 = Differenciel(NbreVS, NbkmanVS, NbreVU, NbkmanVU, Presenceparking, Nb_pdc_choisi, Accessibilite_parking,
                           Optionborne, NbrekWhfacture, Recurrencefacture, Montantfacture, Surfacetoiture, Nbreetages)
    Bilan_Economique_mobilite = Economies_mobilite(territ, NbreVS, NbkmanVS, NbreVU, NbkmanVU, Presenceparking, Nb_pdc_choisi,
                                                   Accessibilite_parking, Optionborne, NbrekWhfacture, Recurrencefacture, Montantfacture,
                                                   Surfacetoiture, Nbreetages)[0]
    Bilan_Environnemental_mobilite = Economies_mobilite(territ, NbreVS, NbkmanVS, NbreVU, NbkmanVU, Presenceparking, Nb_pdc_choisi,
                                                        Accessibilite_parking, Optionborne, NbrekWhfacture, Recurrencefacture, Montantfacture,
                                                        Surfacetoiture, Nbreetages)[1]
    if 'Précédent' in request.POST:
        url = reverse('mobilite', kwargs={'id_enseigne': id_enseigne})

        return HttpResponseRedirect(url)

    return render(request, 'mobilite.html', {'id_enseigne': id_enseigne, 'site': site, 'nb': range_nb, 'courbe1': courbe1, 'courbe2': courbe2_coeffs,
                                             'bilan1': Bilan_Economique_mobilite, 'bilan3': Bilan_Environnemental_mobilite})


@login_required
def bilan_catalogue(request, id_enseigne):
    global conso_perso
    global site

    site = 1

    rqt1 = Enseigne.objects.get(id=id_enseigne)
    nb = rqt1.nb_sites

    projet = rqt1.projet

    if not ExportSite.objects.filter(enseigne=rqt1).exists():
        exportsite = ExportSite(
            projet=projet, enseigne=rqt1, sitename=rqt1.name)
        exportsite.save()

    else:
        exportsite = ExportSite.objects.get(enseigne=rqt1)

    range_nb = range(nb)

    # Mise à jour de la valeur du site

    rqt2 = Batiment.objects.filter(enseigne=rqt1).filter(num_sites=site)[0]

    Nbreetages = rqt2.nb_etages
    type = rqt2.type_batiment
    Nb_batiment = rqt2.nb_batiment

    # Pour plusieurs sites : différents résultats

    # Resultats pour 1 Bâtiment
    rqt3 = Localisation.objects.get(batiment=rqt2)
    territ = rqt3.territ

    rqt4 = Mobilite.objects.get(batiment=rqt2)
    NbreVS = rqt4.vehicule_fonction
    NbkmanVS = rqt4.km_an_vehicule_fonction
    NbreVU = rqt4.vehicule_utilitaire
    NbkmanVU = rqt4.km_an_vehicule_utilitaire
    Presenceparking = rqt4.parking
    Nb_pdc_choisi = rqt4.pt_de_charge
    Accessibilite_parking = rqt4.acces
    Optionborne = rqt4.borne

    rqt5 = EDF.objects.get(batiment=rqt2)
    NbrekWhfacture = rqt5.nb_kW
    Recurrencefacture = rqt5.reference
    Montantfacture = rqt5.facture
    puissance = rqt5.puissance

    rqt6 = Toiture.objects.get(batiment=rqt2)
    surface = rqt6.surface

    rqt7 = Profil.objects.get(batiment=rqt2)
    profil = rqt7.type_profil
    personnalise = Profil_types.objects.get(type_profil='Personnalisé')
    perso = False
    if profil == personnalise:
        perso = True
        profil = ProfilPerso.objects.get(batiment=rqt2).profil

    rqt8 = Electrification.objects.get(souscription=rqt5)
    installation = rqt8.installation

    if Recurrencefacture == 'Bimestrielle':
        conso_perso = ((NbrekWhfacture * 6) / 365) * 7
    if Recurrencefacture == 'Mensuelle':
        conso_perso = ((NbrekWhfacture * 12) / 365) * 7
    if Recurrencefacture == 'Annuelle':
        conso_perso = ((NbrekWhfacture) / 365) * 7

    rqt0 = Emisission_CO2.objects.get(territ=territ)
    Emission_CO2 = rqt0.emission

    Economies_mde = Economies(NbrekWhfacture, Recurrencefacture,
                              Montantfacture, surface, Nbreetages, type, territ)
    Economies_PV = Economies_pv_catalogue(conso_perso, profil, perso, territ, surface, installation, puissance, NbrekWhfacture,
                                          Recurrencefacture, Montantfacture, Nbreetages, type, etat_batterie, etat_AutoProd, etat_entre_deux, id_enseigne)
    Economies_Mobilite = Economies_mobilite(territ, NbreVS, NbkmanVS, NbreVU, NbkmanVU, Presenceparking, Nb_pdc_choisi,
                                            Accessibilite_parking, Optionborne, NbrekWhfacture, Recurrencefacture, Montantfacture, surface, Nbreetages)

    Bilan_avant = Bilan1_catalogue(conso_perso, profil, perso, territ, surface, installation, puissance, NbrekWhfacture, Recurrencefacture,
                                   Montantfacture, Nbreetages, type, NbreVS, NbkmanVS, NbreVU, NbkmanVU, id_enseigne)

    # Bilan_apres = Bilan2(panneau, conso_perso, profil, territ, surface, installation, puissance, NbrekWhfacture, Recurrencefacture,
    #                      Montantfacture, Nbreetages, type, NbreVS, NbkmanVS, NbreVU, NbkmanVU, Presenceparking,
    #                      Nb_pdc_choisi, Accessibilite_parking, Optionborne, Nb_batiment, etat_batterie, etat_AutoProd, etat_entre_deux)

    Economique_mde = round(Economies_mde[0][2]/20*Nb_batiment, 2)
    Economique_pv = round(Economies_PV[0][2]/20*Nb_batiment, 2)
    Economique_mobilite = round((Economies_Mobilite[0][2]/20), 2)
    exportsite.eco_mde = round(Economique_mde*20, 2)
    exportsite.eco_pv = round(Economique_pv*20, 2)
    Total_Economique = round(
        Economique_mde+Economique_pv+Economique_mobilite, 2)

    Environnement_mde = round(Economies_mde[2][2]/20*Nb_batiment, 2)
    Environnement_pv = round(Economies_PV[2][2]/20*Nb_batiment, 2)
    Environnement_mobilite = round(Economies_Mobilite[1][2]/20, 2)
    exportsite.env_mde = round(Environnement_mde*20, 2)
    exportsite.env_pv = round(Environnement_pv*20, 2)
    exportsite.env_mob = round(Environnement_mobilite*20, 2)
    Total_Environnement = round(
        Environnement_mde+Environnement_pv+Environnement_mobilite, 2)

    Energie_mde = round(Environnement_mde/Emission_CO2/1000, 2)
    Energie_pv = 0  # même consommation, c'est la production qui change
    Energie_mobilite = round(Economies_Mobilite[5]/1000, 2)
    Total_Energie = round(Energie_mde+Energie_pv+Energie_mobilite, 2)

    Investissement_mde = Invest(
        NbrekWhfacture, Recurrencefacture, Montantfacture, surface, Nbreetages, type, territ)
    exportsite.invest_mde = round(Investissement_mde, 2)
    Investissement_mde = Investissement_mde/20

    gains_ve = round(Economies_Mobilite[6], 2)
    gains_bornes = round(Economies_Mobilite[7], 2)
    exportsite.gains_ve = gains_ve
    exportsite.revenus_bornes = gains_bornes

    coeff_un = round(Economies_mde[2][2]*Nb_batiment, 1)
    coeff_deux = round(Economies_PV[2][2]*Nb_batiment, 1)
    coeff_trois = round(Economies_Mobilite[1][2], 1)
    emission_sans_action = (
        Bilan_avant[2][8]-(coeff_un+coeff_deux+coeff_trois))
    total = coeff_un+coeff_deux+coeff_trois+emission_sans_action

    coeff_un = (coeff_un / total) * 100
    coeff_deux = (coeff_deux / total) * 100
    coeff_trois = (coeff_trois / total) * 100
    emission_sans_action = (emission_sans_action/total)*100

    coeff_un = round(coeff_un[0], 2)
    coeff_deux = round(coeff_deux[0], 2)
    coeff_trois = round(coeff_trois[0], 2)
    emission_sans_action = round(emission_sans_action[0], 2)

    # print(coeff_un, coeff_deux, coeff_trois, emission_sans_action)

    # conso annuelle élec avant action
    NbrekWhannuel = Variables_mde(
        NbrekWhfacture, Recurrencefacture, Montantfacture, surface, Nbreetages)[2]

    # comparer la consommation envisagée avec la conso actuelle

    # mobilité et électricité
    eco_avant_mob = round(Economies_Mobilite[2], 2)
    eco_avant_elec = round(sum(Economies_PV[3])/20*Nb_batiment, 2)
    exportsite.factu_mob_20 = round(eco_avant_mob*20, 2)
    exportsite.factu_elec_20 = round(eco_avant_elec*20, 2)

    env_avant_mob = Economies_Mobilite[3]
    env_avant_elec = NbrekWhannuel*Emission_CO2*Nb_batiment

    cons_avant_mob = Economies_Mobilite[4]/1000  # MWh
    cons_avant_elec = NbrekWhannuel/1000*Nb_batiment  # MWh

    # consommation actuelle annuelle moyennée sur 20 ans
    # avant
    eco_avant = eco_avant_mob + eco_avant_elec
    eco_avant = round(eco_avant, 2)
    exportsite.factu_tot_20 = round(eco_avant*20, 2)

    env_avant = env_avant_mob + env_avant_elec
    env_avant = round(env_avant, 2)
    exportsite.emission_20 = round(env_avant*20, 2)

    cons_avant = cons_avant_mob + cons_avant_elec
    cons_avant = round(cons_avant, 2)

    # après
    eco_apres = eco_avant - Total_Economique
    eco_apres = round(eco_apres, 2)

    env_apres = env_avant - Total_Environnement
    env_apres = round(env_apres, 2)

    cons_apres = cons_avant - Total_Energie
    cons_apres = round(cons_apres, 2)

    # % d'économies
    eco_p = (eco_avant-eco_apres)/eco_avant*100
    eco_p = round(eco_p, 2)

    env_p = (env_avant-env_apres)/env_avant*100
    env_p = round(env_p, 2)
    exportsite.reduc_co2 = env_p

    cons_p = (cons_avant-cons_apres)/cons_avant*100
    cons_p = round(cons_p, 2)

    # gains revente de surplus moyenne annuelle sur 20 ans
    revente_surplus_moy = Economies_pv_catalogue(conso_perso, profil, perso, territ, surface, installation, puissance, NbrekWhfacture, Recurrencefacture, Montantfacture, Nbreetages, type, False, False,
                                                 False, id_enseigne)[4]

    exportsite.revenus_surplus = round(revente_surplus_moy*20, 2)

    exportsite.eco = exportsite.eco_mde+exportsite.eco_pv + \
        exportsite.gains_ve+exportsite.revenus_bornes

    exportsite.save()

    if 'Précédent' in request.POST:
        url = reverse('mobilite', kwargs={'id_enseigne': id_enseigne})

        return HttpResponseRedirect(url)

    if 'multi-sites' in request.POST:
        url = reverse('multi-sites', kwargs={'id_enseigne': id_enseigne})

        return HttpResponseRedirect(url)

    return render(request, 'bilan.html', {'id_enseigne': id_enseigne, 'site': site, 'nb': range_nb, 'un': Economique_mde, 'deux': Economique_pv, 'trois': Economique_mobilite, 'quatre': Total_Economique,
                                          'cinq': Environnement_mde, 'six': Environnement_pv, 'sept': Environnement_mobilite, 'huit': Total_Environnement,
                                          'neuf': Energie_mde, 'dix': Energie_mobilite, 'onze': Total_Energie,
                                          'Reduction_MDE': coeff_un, 'Reduction_PV': coeff_deux, 'Reduction_Mobilite': coeff_trois, 'Emission_20ans': emission_sans_action,
                                          'eco_avant': eco_avant, 'eco_apres': eco_apres,
                                          'env_avant': env_avant, 'env_apres': env_apres,
                                          'cons_avant': cons_avant, 'cons_apres': cons_apres,
                                          'eco_p': eco_p, 'env_p': env_p, 'cons_p': cons_p,
                                          'revente_surplus_moy': revente_surplus_moy})


@login_required
def multi_sites_catalogue(request, id_projet):
    global conso_perso
    projet = Projet.objects.get(id=id_projet)

    site = 1

    # Mise à jour de la valeur du site

    Economique_mde = 0
    Economique_pv = 0
    Economique_mobilite = 0
    Environnement_mde = 0
    Environnement_pv = 0
    Environnement_mobilite = 0
    Energie_mde = 0
    Energie_pv = 0
    Energie_mobilite = 0

    Investissement_mde_tot = 0

    coeff_un_sum = 0
    coeff_deux_sum = 0
    coeff_trois_sum = 0
    emission_sans_action_sum = 0

    eco_avant_mob = 0
    eco_avant_elec = 0

    env_avant_mob = 0
    env_avant_elec = 0

    cons_avant_mob = 0
    cons_avant_elec = 0

    for rqt1 in Enseigne.objects.filter(projet=projet):
        rqt2 = Batiment.objects.filter(enseigne=rqt1).filter(num_sites=site)[0]

        id_enseigne = rqt1.id

        Nbreetages = rqt2.nb_etages
        type = rqt2.type_batiment
        Nb_batiment = rqt2.nb_batiment

        # Pour plusieurs sites : différents résultats

        # Resultats pour 1 Bâtiment
        rqt3 = Localisation.objects.get(batiment=rqt2)
        territ = rqt3.territ

        rqt4 = Mobilite.objects.get(batiment=rqt2)
        NbreVS = rqt4.vehicule_fonction
        NbkmanVS = rqt4.km_an_vehicule_fonction
        NbreVU = rqt4.vehicule_utilitaire
        NbkmanVU = rqt4.km_an_vehicule_utilitaire
        Presenceparking = rqt4.parking
        Nb_pdc_choisi = rqt4.pt_de_charge
        Accessibilite_parking = rqt4.acces
        Optionborne = rqt4.borne

        rqt5 = EDF.objects.get(batiment=rqt2)
        NbrekWhfacture = rqt5.nb_kW
        Recurrencefacture = rqt5.reference
        Montantfacture = rqt5.facture
        puissance = rqt5.puissance

        rqt6 = Toiture.objects.get(batiment=rqt2)
        surface = rqt6.surface

        rqt7 = Profil.objects.get(batiment=rqt2)
        profil = rqt7.type_profil
        personnalise = Profil_types.objects.get(type_profil='Personnalisé')
        perso = False
        if profil == personnalise:
            perso = True
            profil = ProfilPerso.objects.get(batiment=rqt2).profil

        rqt8 = Electrification.objects.get(souscription=rqt5)
        installation = rqt8.installation

        if Recurrencefacture == 'Bimestrielle':
            conso_perso = ((NbrekWhfacture * 6) / 365) * 7
        if Recurrencefacture == 'Mensuelle':
            conso_perso = ((NbrekWhfacture * 12) / 365) * 7
        if Recurrencefacture == 'Annuelle':
            conso_perso = ((NbrekWhfacture) / 365) * 7

        rqt9 = Emisission_CO2.objects.get(territ=territ)
        Emission_CO2 = rqt9.emission

        Economies_mde = Economies(NbrekWhfacture, Recurrencefacture,
                                  Montantfacture, surface, Nbreetages, type, territ)
        Economies_PV = Economies_pv_catalogue(conso_perso, profil, perso, territ, surface, installation, puissance, NbrekWhfacture,
                                              Recurrencefacture, Montantfacture, Nbreetages, type, etat_batterie, etat_AutoProd, etat_entre_deux, id_enseigne)
        Economies_Mobilite = Economies_mobilite(territ, NbreVS, NbkmanVS, NbreVU, NbkmanVU, Presenceparking, Nb_pdc_choisi,
                                                Accessibilite_parking, Optionborne, NbrekWhfacture, Recurrencefacture, Montantfacture, surface, Nbreetages)

        Bilan_avant = Bilan1_catalogue(conso_perso, profil, perso, territ, surface, installation, puissance, NbrekWhfacture, Recurrencefacture,
                                       Montantfacture, Nbreetages, type, NbreVS, NbkmanVS, NbreVU, NbkmanVU, id_enseigne)

        # Bilan_apres = Bilan2(panneau, conso_perso, profil, territ, surface, installation, puissance, NbrekWhfacture, Recurrencefacture,
        #                      Montantfacture, Nbreetages, type, NbreVS, NbkmanVS, NbreVU, NbkmanVU, Presenceparking,
        #                      Nb_pdc_choisi, Accessibilite_parking, Optionborne, Nb_batiment, etat_batterie, etat_AutoProd, etat_entre_deux)

        # sommes pour multi-sites

        Economique_mde += round(Economies_mde[0][2]/20*Nb_batiment, 2)
        Economique_pv += round(Economies_PV[0][2]/20*Nb_batiment, 2)
        Economique_mobilite += round(Economies_Mobilite[0][2]/20, 2)
        Total_Economique = round(
            Economique_mde+Economique_pv+Economique_mobilite, 2)

        Economique_mde = round(Economique_mde, 2)
        Economique_pv = round(Economique_pv, 2)
        Economique_mobilite = round(Economique_mobilite, 2)

        Environnement_mde += round(Economies_mde[2][2]/20*Nb_batiment, 2)
        Environnement_pv += round(Economies_PV[2][2]/20*Nb_batiment, 2)
        Environnement_mobilite += round(Economies_Mobilite[1][2]/20, 2)
        Total_Environnement = round(
            Environnement_mde+Environnement_pv+Environnement_mobilite, 2)

        Environnement_mde = round(Environnement_mde, 2)
        Environnement_pv = round(Environnement_pv, 2)
        Environnement_mobilite = round(Environnement_mobilite, 2)

        Energie_mde += round(Environnement_mde/Emission_CO2/1000, 2)
        Energie_pv += 0
        Energie_mobilite += round(Economies_Mobilite[5]/1000, 2)
        Total_Energie = round(Energie_mde+Energie_pv+Energie_mobilite, 2)

        Energie_mde = round(Energie_mde, 2)
        Energie_pv = round(Energie_pv, 2)
        Energie_mobilite = round(Energie_mobilite, 2)

        Investissement_mde_tot += Invest(
            NbrekWhfacture, Recurrencefacture, Montantfacture, surface, Nbreetages, type, territ)
        Investissement_mde = Investissement_mde_tot/20

        coeff_un_sum += round(Economies_mde[2][2]*Nb_batiment, 2)
        coeff_deux_sum += round(Economies_PV[2][2]*Nb_batiment, 2)
        coeff_trois_sum += round(Economies_Mobilite[1][2], 2)
        emission_sans_action_sum += Bilan_avant[2][8] - \
            (coeff_un_sum+coeff_deux_sum+coeff_trois_sum)
        total = coeff_un_sum+coeff_deux_sum + \
            coeff_trois_sum+emission_sans_action_sum[0]

        coeff_un = (coeff_un_sum / total) * 100
        coeff_deux = (coeff_deux_sum / total) * 100
        coeff_trois = (coeff_trois_sum / total) * 100
        emission_sans_action = (emission_sans_action_sum[0]/total)*100

        coeff_un = round(coeff_un, 2)
        coeff_deux = round(coeff_deux, 2)
        coeff_trois = round(coeff_trois, 2)
        emission_sans_action = round(emission_sans_action, 2)

        # conso annuelle élec avant action
        NbrekWhannuel = Variables_mde(
            NbrekWhfacture, Recurrencefacture, Montantfacture, surface, Nbreetages)[2]

        # comparer la consommation envisagée avec la conso actuelle

        # mobilité et électricité
        eco_avant_mob += Economies_Mobilite[2]
        eco_avant_elec += sum(Economies_PV[3])/20*Nb_batiment

        env_avant_mob += Economies_Mobilite[3]
        env_avant_elec += NbrekWhannuel*Emission_CO2*Nb_batiment

        cons_avant_mob += Economies_Mobilite[4]/1000  # MWh
        cons_avant_elec += NbrekWhannuel/1000*Nb_batiment  # MWh

        # consommation actuelle annuelle moyennée sur 20 ans
        # avant
        eco_avant = eco_avant_mob + eco_avant_elec
        eco_avant = round(eco_avant, 2)

        env_avant = env_avant_mob + env_avant_elec
        env_avant = round(env_avant, 2)

        cons_avant = cons_avant_mob + cons_avant_elec
        cons_avant = round(cons_avant, 2)

        # après
        eco_apres = eco_avant - Total_Economique
        eco_apres = round(eco_apres, 2)

        env_apres = env_avant - Total_Environnement
        env_apres = round(env_apres, 2)

        cons_apres = cons_avant - Total_Energie
        cons_apres = round(cons_apres, 2)

        # % d'économies
        eco_p = (eco_avant-eco_apres)/eco_avant*100
        eco_p = round(eco_p, 2)

        env_p = (env_avant-env_apres)/env_avant*100
        env_p = round(env_p, 2)

        cons_p = (cons_avant-cons_apres)/cons_avant*100
        cons_p = round(cons_p, 2)

    return render(request, 'multi_sites.html', {'site': site, 'un': Economique_mde, 'deux': Economique_pv, 'trois': Economique_mobilite, 'quatre': Total_Economique,
                                                'cinq': Environnement_mde, 'six': Environnement_pv, 'sept': Environnement_mobilite, 'huit': Total_Environnement,
                                                'neuf': Energie_mde, 'dix': Energie_mobilite, 'onze': Total_Energie,
                                                'Reduction_MDE': coeff_un, 'Reduction_PV': coeff_deux, 'Reduction_Mobilite': coeff_trois, 'Emission_20ans': emission_sans_action,
                                                'eco_avant': eco_avant, 'eco_apres': eco_apres,
                                                'env_avant': env_avant, 'env_apres': env_apres,
                                                'cons_avant': cons_avant, 'cons_apres': cons_apres,
                                                'eco_p': eco_p, 'env_p': env_p, 'cons_p': cons_p})


def export_xls(request, id_projet):
    # content-type of response
    response = HttpResponse(content_type='application/ms-excel')

    projet = Projet.objects.get(pk=id_projet)
    filename = str(projet.name)+'.xls'

    # decide file name
    response['Content-Disposition'] = 'attachment; filename="%s"' % filename

    # creating workbook
    wb = xlwt.Workbook(encoding='utf-8')

    # adding sheet
    ws = wb.add_sheet("Multisite")

    # Sheet header, first row
    row_num = 0

    al = xlwt.Alignment()
    al.horz = xlwt.Alignment.HORZ_CENTER
    al.vert = xlwt.Alignment.VERT_CENTER

    font_style = xlwt.XFStyle()
    # headers are bold
    font_style.font.bold = False
    font_style.alignment = al

    # column header names, you can use your own headers here
    columns = ['Nom du site', 'Investissement MDE (€)',
               'Economies MDE (€)', 'Economies MDE (kg CO2)', 'Investissement PV (€)', 'Puissance Centrale (kWc)', 'Economies PV (€)', 'Revenus Revente Surplus (€)', 'Economies PV (kg CO2)', 'Gains avec ESCO (€)', 'Réduction ESCO A1-A10 (%)', 'Réduction ESCO A11-A20 (%)', 'Gains sans ESCO (€)', 'Gains transition VE (€)', 'Revenus bornes (€)', 'Economies Mobilité (kg CO2)', 'Réductions CO2 (%)', 'Economies (€)', 'Facture Electrique sur 20 ans (€)', 'Facture Mobilité sur 20 ans (€)', 'Facture totale sur 20 ans (€)', 'Emissions de CO2 sur 20 ans (kg CO2)']

    nb_cols = len(columns)

    # write column headers in sheet
    for col_num in range(nb_cols):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    al = xlwt.Alignment()
    al.horz = xlwt.Alignment.HORZ_CENTER
    al.vert = xlwt.Alignment.VERT_CENTER

    font_style = xlwt.XFStyle()
    font_style.alignment = al

    sites = ExportSite.objects.filter(projet=projet)

    data = [s.export for s in sites]

    for my_row in data:
        row_num = row_num + 1
        for i in range(nb_cols):
            ws.write(row_num, i, my_row[i], font_style)

    wb.save(response)
    return response
