from django.utils.encoding import smart_str
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy, reverse
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView

from django.shortcuts import render, redirect
from django.contrib import messages

from PV.models import Enseigne
from .forms import *
from PV.models import *
from .forms import *
from PV.forms import *

import xlwt
import csv

# Students name
NAME = ['Riya', 'Suzzane', 'George', 'Zoya', 'Smith', 'Henry']
# QUIZ Subject
SUBJECT = ['CHE', 'PHY', 'CHE', 'BIO', 'ENG', 'ENG']


def psg(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse('text/csv')
    response['Content-Disposition'] = 'attachment; filename=quiz.csv'
# Create the CSV writer using the HttpResponse as the "file"
    writer = csv.writer(response)
    writer.writerow(['Student Name', 'Quiz Subject'])
    for (name, sub) in zip(NAME, SUBJECT):
        writer.writerow([name, sub])

    return response


# Create your views here.


def home(request):
    return render(request, 'users/templates/home.html')


class SignUp(CreateView):
    form_class = UserForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


@login_required
def updateuser(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)

        if user_form.is_valid():
            user_form.save()
            url = reverse('projets')
            return HttpResponseRedirect(url)
    else:
        user_form = UpdateUserForm(instance=request.user)

    return render(request, 'registration/updateprofile.html', {'user_form': user_form})


@login_required
def profile(request, id_projet):
    user = request.user
    nom_entreprise = user.entite
    email = user.email

    projet_defaut = Projet.objects.get(name='-')

    projet = Projet.objects.get(pk=id_projet)
    if not projet == projet_defaut:
        projet_name = projet.name
    else:
        projet_name = 'Sites seuls'

    results_ok = {}

    if Enseigne.objects.filter(projet=projet).exists():
        rqt1 = Enseigne.objects.filter(projet=projet)
        enseignes = [e for e in rqt1]
        nb_enseignes = len(enseignes)

        for e in enseignes:
            results_ok[e.id] = False
            if Batiment.objects.filter(enseigne=e).exists():
                rqt2 = Batiment.objects.filter(enseigne=e)[0]
                rqt3 = CentraleBatiment.objects.filter(batiment=rqt2)
                if rqt3.exists():
                    results_ok[e.id] = True

    else:
        enseignes = []
        nb_enseignes = 0

    return render(request, 'users/templates/profile.html', {'enseignes': enseignes, 'nom_entreprise': nom_entreprise, 'email': email, 'nb_enseignes': nb_enseignes, 'results_ok': results_ok, 'projet_name': projet_name, 'id_projet': id_projet})


@login_required
def projets(request):
    user = request.user
    nom_entreprise = user.entite
    email = user.email

    if Projet.objects.filter(user=user).exists():
        rqt1 = Projet.objects.filter(user=user)
        projets = [e for e in rqt1 if e.name != '-']
        nb_projets = len(projets)

    else:
        projets = []
        nb_projets = 0

    nb_sites = 0
    for p in projets:
        nb_sites += p.nb_enseignes

    projet_defaut = Projet.objects.get(name='-')

    return render(request, 'users/templates/profile-projets.html', {'projet_defaut': projet_defaut, 'nb_sites': nb_sites, 'projets': projets, 'nom_entreprise': nom_entreprise, 'email': email, 'nb_projets': nb_projets})


def addproject(request):
    global formP

    user = request.user
    nom_entreprise = user.entite

    if request.method == 'POST':

        form_projet = ProjetForm(data=request.POST)

        form_projet_valid = form_projet.is_valid()

        if 'next' in request.POST:
            if form_projet_valid:
                projet = form_projet.save(commit=False)
                projet.user = user

                form_projet.save()

                id_projet = projet.id

                url = reverse('profile', kwargs={'id_projet': id_projet})
                return HttpResponseRedirect(url)

            else:
                messages.error(request, "Error")
                print(form_projet.errors)

        if 'Précédent' in request.POST:
            url = reverse('projets')
            return HttpResponseRedirect(url)

    else:
        formP = ProjetForm()

    return render(request, 'wizard-create-project.html', {'formP': formP, 'nom_entreprise': nom_entreprise})


# def export_csv(request):
#     # Students name
#     NAME = ['Riya', 'Suzzane', 'George', 'Zoya', 'Smith', 'Henry']
#     # QUIZ Subject
#     SUBJECT = ['CHE', 'PHY', 'CHE', 'BIO', 'ENG', 'ENG']

#     # Create the HttpResponse object with the appropriate CSV header.
#     response = HttpResponse()
#     response['Content-Disposition'] = 'attachment; filename=quiz.csv'
#     # Create the CSV writer using the HttpResponse as the "file"
#     writer = csv.writer(response)
#     writer.writerow(['Student Name', 'Quiz Subject'])
#     for (name, sub) in zip(NAME, SUBJECT):
#         writer.writerow([name, sub])

#     return response
