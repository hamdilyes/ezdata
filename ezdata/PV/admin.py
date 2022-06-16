from sre_constants import CATEGORY_UNI_NOT_LINEBREAK
from unicodedata import name
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.http import HttpResponse

from django.shortcuts import render, redirect
from .models import *
from import_export.admin import ImportExportModelAdmin
from .facturation import total_prix
from django.urls import reverse
from django.utils.safestring import mark_safe

# Créer les urls de l'admin + les vues spécifiques


# class MyAdminSite(AdminSite):

#     def get_urls(self):
#         from django.urls import path
#         urls = super().get_urls()
#         urls += [
#             path('resume', self.admin_view(self.my_view), name='resume'),

#         ]
#         return urls

#     def my_view(self, request):
#         return HttpResponse("Hello!")


# admin_site = MyAdminSite(name='myadmin')


class ItemQuantiteInline(admin.StackedInline):
    model = ItemQuantite
    extra = 0


class EnseigneInline(admin.StackedInline):
    model = Enseigne
    extra = 0


class BatimentInline(admin.StackedInline):
    model = Batiment
    extra = 0


class LocalisationInline(admin.StackedInline):
    model = Localisation
    max_num = 0


class ProfilInline(admin.StackedInline):
    model = Profil
    max_num = 0


class ToitureInline(admin.StackedInline):
    model = Toiture
    max_num = 0


class EDFInline(admin.StackedInline):
    model = EDF
    max_num = 0


class MobiliteInline(admin.StackedInline):
    model = Mobilite
    max_num = 0


class ClientAdmin(admin.ModelAdmin):
    list_display = ("id", "nom_entreprise",
                    "get_enseigne_list", "created_date")

    change_form_template = 'admin/change_form_clients.html'

    def get_enseigne_list(self, obj):
        rqt1 = Enseigne.objects.filter(client=obj)
        l = []
        for e in rqt1:
            l.append(e.id)
        return l
    # Allows column order sorting
    get_enseigne_list.admin_order_field = 'Client_Enseigne'
    get_enseigne_list.short_description = 'Liste des enseignes'  # Renames column head

    def get_batiment(self, obj):

        rqt1 = Enseigne.objects.filter(client=obj)

        # rqt2 --> Objet : Bâtiment

        rqt2 = Batiment.objects.filter(enseigne=rqt1)

        return rqt2.nb_batiment

    get_batiment.admin_order_field = 'Client_Enseigne'  # Allows column order sorting
    get_batiment.short_description = 'Nombre de bâtiments'  # Renames column head

    def get_enseigne_secteur(self, obj):

        rqt1 = Enseigne.objects.filter(client=obj)

        # rqt2 --> Objet : Bâtiment

        return rqt1.secteur

    # Allows column order sorting
    get_enseigne_secteur.admin_order_field = 'Client_Enseigne'
    get_enseigne_secteur.short_description = 'Secteur'  # Renames column head

    def get_enseigne_sites(self, obj):

        rqt1 = Enseigne.objects.filter(client=obj)

        # rqt2 --> Objet : Bâtiment

        return rqt1.nb_sites

    # Allows column order sorting
    get_enseigne_sites.admin_order_field = 'Client_Enseigne'
    get_enseigne_sites.short_description = 'Nombre de sites'  # Renames column head

    def get_factu(self, obj):

        rqt1 = Enseigne.objects.filter(client=obj)

        # rqt2 --> Objet : Bâtiment

        rqt2 = Batiment.objects.filter(enseigne=rqt1).filter(num_sites=1)
        rqt3 = Modules_factu.objects.filter(client=obj)

        return total_prix(obj, rqt2)

    get_factu.admin_order_field = 'Client_factu'  # Allows column order sorting
    # Renames column head
    get_factu.short_description = 'Prix Centrale (unique)'

    # Pour mettre tous les champs du formulaire sur la même page, il faut creer des liens spéciaux pour toutes les tabulations...
    # Puis sur la vue, on ajoute tous ces nouveaux champs

    def id(self, client):
        rqt1 = Client.objects.get(id=client)
        id_client = rqt1.id
        return id_client

    def client_link(self, client):
        rqt1 = Client.objects.get(id=client)
        url = reverse("admin:PV_client_change", args=[rqt1.id])
        link = '<a href="%s">%s</a>' % (url, 'Profil Client')
        return mark_safe(link)

    # def enseigne_link(self, client):
    #     rqt1 = Enseigne.objects.get(client=client)

    #     url = reverse("admin:PV_enseigne_change", args=[rqt1.id])
    #     link = '<a href="%s">%s</a>' % (url, 'Enseigne')
    #     return mark_safe(link)

    # def site(self, client):
    #     rqt1 = Enseigne.objects.get(client=client)
    #     return rqt1.nb_sites

    def range(self, client):
        site = self.site(client)

        return range(site)

    # def batiment_link(self, client):
    #     rqt1 = Enseigne.objects.filter(client=client)
    #     site = rqt1.nb_sites

    #     l = []
    #     for i in range(site):
    #         print(i)
    #         rqt2 = Batiment.objects.filter(enseigne=rqt1)[i]
    #         print(rqt2)
    #         url = reverse("admin:PV_batiment_change", args=[rqt2.id])
    #         link = '<a href="%s">%s</a>' % (url, 'Bâtiment : ')
    #         l.append(mark_safe(link))

    #     print(l)
    #     return l

    # def localisation_link(self, client):
    #     rqt1 = Enseigne.objects.get(client=client)
    #     site = rqt1.nb_sites

    #     l = []
    #     for i in range(site):
    #         print(i)
    #         rqt2 = Batiment.objects.filter(enseigne=rqt1)[i]
    #         rqt3 = Localisation.objects.get(batiment=rqt2)

    #         url = reverse("admin:PV_localisation_change", args=[rqt3.id])
    #         link = '<a href="%s">%s</a>' % (url, 'Localisation : ')
    #         l.append(mark_safe(link))

    #     print(l)
    #     return l

    # def profil_link(self, client):
    #     rqt1 = Enseigne.objects.get(client=client)
    #     site = rqt1.nb_sites

    #     l = []
    #     for i in range(site):
    #         print(i)
    #         rqt2 = Batiment.objects.filter(enseigne=rqt1)[i]
    #         rqt3 = Profil.objects.get(batiment=rqt2)

    #         url = reverse("admin:PV_profil_change", args=[rqt3.id])
    #         link = '<a href="%s">%s</a>' % (url, 'Profil')
    #         l.append(mark_safe(link))

    #     print(l)
    #     return l

    # def toiture_link(self, client):
    #     rqt1 = Enseigne.objects.get(client=client)
    #     site = rqt1.nb_sites

    #     l = []
    #     for i in range(site):
    #         print(i)
    #         rqt2 = Batiment.objects.filter(enseigne=rqt1)[i]
    #         rqt3 = Toiture.objects.get(batiment=rqt2)

    #         url = reverse("admin:PV_toiture_change", args=[rqt3.id])
    #         link = '<a href="%s">%s</a>' % (url, 'Toiture : ')
    #         l.append(mark_safe(link))

    #     print(l)
    #     return l

    # def edf_link(self, client):
    #     rqt1 = Enseigne.objects.get(client=client)
    #     site = rqt1.nb_sites

    #     l = []
    #     for i in range(site):
    #         print(i)
    #         rqt2 = Batiment.objects.filter(enseigne=rqt1)[i]
    #         rqt3 = EDF.objects.get(batiment=rqt2)

    #         url = reverse("admin:PV_edf_change", args=[rqt3.id])
    #         link = '<a href="%s">%s</a>' % (url, 'EDF')
    #         l.append(mark_safe(link))

    #     print(l)
    #     return l

    # def souscription_link(self, client):
    #     rqt1 = Enseigne.objects.get(client=client)
    #     site = rqt1.nb_sites

    #     l = []
    #     for i in range(site):
    #         print(i)
    #         rqt2 = Batiment.objects.filter(enseigne=rqt1)[i]
    #         rqt3 = EDF.objects.get(batiment=rqt2)
    #         rqt4 = Electrification.objects.get(souscription=rqt3)

    #         url = reverse("admin:PV_electrification_change", args=[rqt4.id])
    #         link = '<a href="%s">%s</a>' % (url, 'Souscription')
    #         l.append(mark_safe(link))

    #     print(l)
    #     return l

    # def mobilite_link(self, client):
    #     rqt1 = Enseigne.objects.get(client=client)
    #     site = rqt1.nb_sites

    #     l = []
    #     for i in range(site):
    #         print(i)
    #         rqt2 = Batiment.objects.filter(enseigne=rqt1)[i]
    #         rqt3 = Mobilite.objects.get(batiment=rqt2)

    #         url = reverse("admin:PV_mobilite_change", args=[rqt3.id])
    #         link = '<a href="%s">%s</a>' % (url, 'Mobilité : ')
    #         l.append(mark_safe(link))

    #     print(l)
    #     return l

    def change_view(self, request, object_id,  form_url='', extra_context=None):
        if 'Site' in request.POST:
            site = request.POST.get('site')
        else:
            site = 1
        extra_context = extra_context or {}
        extra_context['id_client'] = self.id(object_id)
        # extra_context['site'] = self.site(object_id)
        # extra_context['nb'] = self.range(object_id)
        extra_context['lien_client'] = self.client_link(object_id)
        # extra_context['lien_enseigne'] = self.enseigne_link(object_id)
        # extra_context['lien_batiment'] = self.batiment_link(object_id)
        # extra_context['lien_localisation'] = self.localisation_link(object_id)
        # extra_context['lien_profil'] = self.profil_link(object_id)
        # extra_context['lien_toiture'] = self.toiture_link(object_id)
        # extra_context['lien_edf'] = self.edf_link(object_id)
        # extra_context['lien_souscription'] = self.souscription_link(object_id)
        # extra_context['lien_mobilite'] = self.mobilite_link(object_id)

        return super().change_view(request, object_id, form_url, extra_context=extra_context)


# # admin.site.register(Client,  ClientAdmin)


class EnseigneAdmin(admin.ModelAdmin):
    list_display = ('name', "get_user", "id", "secteur")

    change_form_template = 'admin/change_form_enseignes.html'

    def get_user(self, obj):
        return obj.user
    get_user.admin_order_field = 'User_Enseigne'  # Allows column order sorting
    get_user.short_description = 'User'  # Renames column head

    def get_name(self, id):
        rqt1 = Enseigne.objects.get(pk=id)
        return rqt1.name

    def user_link(self, id):
        rqt1 = Enseigne.objects.get(pk=id)
        rqt2 = rqt1.user

        url = reverse("admin:PV_enseigne_change", args=[rqt2.id])
        link = '<a href="%s">%s</a>' % (url, 'User')
        return mark_safe(link)

    def sites_link(self, id):
        rqt1 = Enseigne.objects.get(pk=id)
        rqt2 = Batiment.objects.filter(enseigne=rqt1)
        l = []
        for bat in rqt2:
            url = reverse("admin:PV_batiment_change", args=[bat.id])
            link = '<a href="%s">%s</a>' % (url, 'Site - '+str(bat.num_sites))
            l.append(mark_safe(link))
        return l

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['name'] = self.get_name(object_id)
        extra_context['lien_client'] = self.user_link(object_id)
        extra_context['lien_sites'] = self.sites_link(object_id)

        return super().change_view(request, object_id, form_url, extra_context=extra_context)


# admin.site.register(Enseigne, EnseigneAdmin)


class BatimentAdmin(admin.ModelAdmin):
    list_display = ("id", "get_enseigne", "get_profil")

    change_form_template = 'admin/change_form_batiments.html'

    def get_enseigne(self, obj):
        return obj.enseigne.name

    get_enseigne.admin_order_field = 'Batiment_Enseigne'  # Allows column order sorting
    get_enseigne.short_description = 'Enseigne'  # Renames column head

    def get_profil(self, obj):
        rqt1 = Profil.objects.get(batiment=obj)
        return rqt1.type_profil

    get_profil.admin_order_field = 'batiment_profil'  # Allows column order sorting
    get_profil.short_description = 'Profil'  # Renames column head

    # # # # # # # # # #

    def get_name(self, id):
        bat = Batiment.objects.get(pk=id)
        ens = bat.enseigne
        name = ens.name
        return name

    def get_num_site(self, id):
        bat = Batiment.objects.get(pk=id)
        n = bat.num_sites
        return n

    def user_link(self, id):
        bat = Batiment.objects.get(pk=id)
        ens = bat.enseigne
        user = ens.user

        url = reverse("admin:PV_enseigne_change", args=[user.id])
        link = '<a href="%s">%s</a>' % (url, str(user.entite))
        return mark_safe(link)

    def enseigne_link(self, id):
        bat = Batiment.objects.get(pk=id)
        ens = bat.enseigne

        url = reverse("admin:PV_enseigne_change", args=[ens.id])
        link = '<a href="%s">%s</a>' % (url, str(ens.name))
        return mark_safe(link)

    def localisation_link(self, id):
        bat = Batiment.objects.get(pk=id)
        rqt3 = Localisation.objects.get(batiment=bat)

        url = reverse("admin:PV_localisation_change", args=[rqt3.id])
        link = '<a href="%s">%s</a>' % (url, 'Localisation')
        return mark_safe(link)

    def profil_link(self, id):
        bat = Batiment.objects.get(pk=id)
        rqt3 = Profil.objects.get(batiment=bat)

        url = reverse("admin:PV_profil_change", args=[rqt3.id])
        link = '<a href="%s">%s</a>' % (url, 'Profil')
        return mark_safe(link)

    def toiture_link(self, id):
        bat = Batiment.objects.get(pk=id)
        rqt3 = Toiture.objects.get(batiment=bat)

        url = reverse("admin:PV_toiture_change", args=[rqt3.id])
        link = '<a href="%s">%s</a>' % (url, 'Toiture')
        return mark_safe(link)

    def edf_link(self, id):
        bat = Batiment.objects.get(pk=id)
        rqt3 = EDF.objects.get(batiment=bat)

        url = reverse("admin:PV_edf_change", args=[rqt3.id])
        link = '<a href="%s">%s</a>' % (url, 'EDF')
        return mark_safe(link)

    def souscription_link(self, id):
        bat = Batiment.objects.get(pk=id)
        rqt3 = EDF.objects.get(batiment=bat)
        rqt4 = Electrification.objects.get(souscription=rqt3)

        url = reverse("admin:PV_electrification_change", args=[rqt4.id])
        link = '<a href="%s">%s</a>' % (url, 'Souscription')
        return mark_safe(link)

    def mobilite_link(self, id):
        bat = Batiment.objects.get(pk=id)
        rqt3 = Mobilite.objects.get(batiment=bat)

        url = reverse("admin:PV_mobilite_change", args=[rqt3.id])
        link = '<a href="%s">%s</a>' % (url, 'Mobilité')
        return mark_safe(link)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}

        extra_context['name'] = self.get_name(object_id)
        extra_context['num_site'] = self.get_num_site(object_id)

        extra_context['lien_client'] = self.user_link(object_id)
        extra_context['lien_enseigne'] = self.enseigne_link(object_id)
        extra_context['lien_mobilite'] = self.mobilite_link(object_id)
        extra_context['lien_souscription'] = self.souscription_link(object_id)
        extra_context['lien_edf'] = self.edf_link(object_id)
        extra_context['lien_toiture'] = self.toiture_link(object_id)
        extra_context['lien_profil'] = self.profil_link(object_id)
        extra_context['lien_localisation'] = self.localisation_link(object_id)

        return super().change_view(request, object_id, form_url, extra_context=extra_context)


# admin.site.register(Batiment, BatimentAdmin)


class LocalisationAdmin(admin.ModelAdmin):

    change_form_template = 'admin/change_form_coeffs.html'


# admin.site.register(Localisation, LocalisationAdmin)


class ProfilAdmin(admin.ModelAdmin):

    change_form_template = 'admin/change_form_coeffs.html'


# admin.site.register(Profil, ProfilAdmin)


class ToitureAdmin(admin.ModelAdmin):

    change_form_template = 'admin/change_form_coeffs.html'


# admin.site.register(Toiture, ToitureAdmin)


class EDFAdmin(admin.ModelAdmin):

    change_form_template = 'admin/change_form_coeffs.html'


# admin.site.register(EDF, EDFAdmin)


class ElectrificationAdmin(admin.ModelAdmin):

    change_form_template = 'admin/change_form_coeffs.html'


# admin.site.register(Electrification, ElectrificationAdmin)


class MobiliteAdmin(admin.ModelAdmin):

    change_form_template = 'admin/change_form_coeffs.html'


# admin.site.register(Mobilite, MobiliteAdmin)

# admin.site.register(Taxe)


# # admin.site.register(BDD)

# @admin.register(BDD)

class BDDAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["N", "Onduleur_1", "Batterie_1", "Nombre_Batterie_1", "Onduleur_2", "Batterie_2", "Nombre_Batterie_2", "Onduleur_3",
                    "Module_batterie_1", "Module_batterie_2", "Electrical_installation", "Nb_modules_min", "Puissance_centrale_max", "Capacit_batterie",
                    "Prix_total_achat"]


# admin.site.register(BDD, BDDAdmin)


class OnduleursAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["model", "nom_francais", "nom_anglais",
                    "cout",	"install", "tension", "puissance_dc", "puissance_ac"]

    change_form_template = 'admin/change_form_coeffs.html'


# admin.site.register(Onduleurs, OnduleursAdmin)


class ModulesPVAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["Nom", "Puissance_modulaire_kW",
                    "Surface_Panneau_m2", "Cout"]


class MonitoringAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["model", "nom_francais",
                    "nom_anglais", "cout", "puissance_max"]


class Main_doeuvreAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["model", "nom_francais", "nom_anglais", "cout"]


class BatterieAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["model", "nom_francais",
                    "nom_anglais", "cout", "capacite", "puissance"]


class Extensions_BatteriesAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["model", "nom_francais",
                    "nom_anglais", "cout", "capacite", "puissance"]


class TableauxAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["model", "nom_francais", "nom_anglais", "cout"]


class CablesAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["model", "nom_francais", "nom_anglais", "cout"]


class CheminementAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["model", "nom_francais", "nom_anglais", "cout"]


class DiversAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["model", "nom_francais", "nom_anglais", "cout"]


class IngeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["model", "nom_francais", "nom_anglais", "cout"]


class StructureAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["model", "nom_francais", "nom_anglais", "cout"]


class BDDBatAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["type", "moy_kWh_avant", "moy_kWh_apres", "moy_euros_avant",
                    "moy_euros_apres", "cout_kWh_avant", "cout_kWh_apres", "gain"]


class Emisission_CO2Admin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["territ", "emission"]


class Hyp_cout_mobiliteAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["model", "valeur", "unite"]


class EZ_DRIVEAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["model", "valeur", "unite", "invest"]


class Coeffs_OuvresAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["get_profil", "heure", "coeff"]
    list_filter = ('profil', 'heure')

    change_form_template = 'admin/change_form_coeffs.html'

    def get_profil(self, obj):
        return obj.profil

    get_profil.admin_order_field = 'profil'  # Allows column order sorting
    get_profil.short_description = 'Profil'  # Renames column head


# admin.site.register(Coeffs_Ouvres, Coeffs_OuvresAdmin)


class Coeffs_WeekendAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["get_profil", "heure", "coeff"]

    change_form_template = 'admin/change_form_coeffs.html'

    def get_profil(self, obj):
        return obj.profil

    get_profil.admin_order_field = 'Profil_Weekend'  # Allows column order sorting
    get_profil.short_description = 'Profil'  # Renames column head


# admin.site.register(Coeffs_Weekend, Coeffs_WeekendAdmin)


class Coeffs_Ouvres(admin.StackedInline):
    model = Coeffs_Ouvres
    extra = 23


class Coeffs_Weekend(admin.StackedInline):
    model = Coeffs_Weekend
    extra = 23


class Profil_typesAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    change_form_template = 'admin/change_form_coeffs.html'


class Tailles_StandardAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    change_form_template = 'admin/change_form_coeffs.html'

##################################################################################


class CatalogueSolutionAdmin(admin.ModelAdmin):
    list_display = ("solution", 'get_nb_elements', 'taille')

    change_form_template = 'admin/change_form_cataloguesolution.html'

    def solution(self, obj):
        return obj
    # Allows column order sorting
    solution.admin_order_field = ''
    # Renames column head
    solution.short_description = 'Solution'

    def get_solution(self, id):
        sol = CatalogueSolution.objects.get(pk=id)
        return sol

    def get_nb_elements(self, obj):
        rqt = ItemQuantite.objects.filter(catalogue_solution=obj)
        nb = 0
        for _ in rqt:
            nb += 1
        return nb
    # Allows column order sorting
    get_nb_elements.admin_order_field = ''
    # Renames column head
    get_nb_elements.short_description = "Nombre d'éléments du chiffrage"

    # Pour mettre tous les champs du formulaire sur la même page, il faut creer des liens spéciaux pour toutes les tabulations...
    # Puis sur la vue, on ajoute tous ces nouveaux champs

    def solution_link(self, id):
        url = reverse("admin:PV_cataloguesolution_change", args=[id])
        link = '<a href="%s">%s</a>' % (url, 'Solution')
        return mark_safe(link)

    def add_element_link(self, id):
        url = reverse("admin:PV_itemquantite_add", args=[])
        link = '<a href="%s">%s</a>' % (url, "Ajouter élément")
        return mark_safe(link)

    def elements_link(self, id):
        obj = CatalogueSolution.objects.get(pk=id)
        rqt = ItemQuantite.objects.filter(catalogue_solution=obj)

        l = []
        for el in rqt:
            url = reverse("admin:PV_itemquantite_change", args=[el.id])
            link = '<a href="%s">%s</a>' % (url, str(el.facturation_item.type))
            l.append(mark_safe(link))

        return l

    def change_view(self, request, object_id,  form_url='', extra_context=None):
        extra_context = extra_context or {}

        extra_context['solution'] = self.get_solution(object_id)
        extra_context['lien_solution'] = self.solution_link(object_id)
        extra_context['lien_elements'] = self.elements_link(object_id)
        extra_context['lien_add_element'] = self.add_element_link(object_id)

        return super().change_view(request, object_id, form_url, extra_context=extra_context)


class FacturationItemAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('type', 'article', 'cout_HA_unit')
    change_form_template = 'admin/change_form_coeffs.html'


class ItemQuantiteAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ("solution", 'item', 'quantite')

    change_form_template = 'admin/change_form_itemquantite.html'

    def solution(self, obj):
        sol = obj.catalogue_solution
        return sol
    # Allows column order sorting
    solution.admin_order_field = ''
    # Renames column head
    solution.short_description = 'Solution'

    def item(self, obj):
        item = obj.facturation_item
        return item
    # Allows column order sorting
    item.admin_order_field = ''
    # Renames column head
    item.short_description = "Elément"

    def get_item(self, id):
        obj = ItemQuantite.objects.get(pk=id)
        item = obj.facturation_item
        return item

    def get_element_type(self, id):
        obj = ItemQuantite.objects.get(pk=id)
        item = obj.facturation_item
        t = item.type
        return t

    def qt(self, obj):
        qt = obj.quantite
        return qt
    # Allows column order sorting
    qt.admin_order_field = ''
    # Renames column head
    qt.short_description = "Quantité"

    # Pour mettre tous les champs du formulaire sur la même page, il faut creer des liens spéciaux pour toutes les tabulations...
    # Puis sur la vue, on ajoute tous ces nouveaux champs

    def solution_link(self, id):
        obj = ItemQuantite.objects.get(pk=id)
        sol = obj.catalogue_solution
        sol_id = sol.id
        url = reverse("admin:PV_cataloguesolution_change", args=[sol_id])
        link = '<a href="%s">%s</a>' % (url, 'Solution')
        return mark_safe(link)

    def add_element_link(self, id):
        url = reverse("admin:PV_itemquantite_add", args=[])
        link = '<a href="%s">%s</a>' % (url, "Ajouter élément")
        return mark_safe(link)

    def elements_link(self, id):
        obj = ItemQuantite.objects.get(pk=id)
        sol = obj.catalogue_solution
        rqt = ItemQuantite.objects.filter(catalogue_solution=sol)

        l = []
        for el in rqt:
            url = reverse("admin:PV_itemquantite_change", args=[el.id])
            link = '<a href="%s">%s</a>' % (url, str(el.facturation_item.type))
            l.append(mark_safe(link))

        return l

    def change_view(self, request, object_id,  form_url='', extra_context=None):
        extra_context = extra_context or {}

        extra_context['item'] = self.get_item(object_id)
        extra_context['element_type'] = self.get_element_type(object_id)
        extra_context['lien_solution'] = self.solution_link(object_id)
        extra_context['lien_elements'] = self.elements_link(object_id)
        extra_context['lien_add_element'] = self.add_element_link(object_id)

        return super().change_view(request, object_id, form_url, extra_context=extra_context)


class CourbeDeChargeAdmin(admin.ModelAdmin):
    list_display = ('profil', 'type')
    change_form_template = 'admin/change_form_coeffs.html'


class ProjetAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']
    change_form_template = 'admin/change_form_coeffs.html'


##########################################################################################


admin.site.register(CourbeDeCharge, CourbeDeChargeAdmin)
admin.site.register(Profil_types, Profil_typesAdmin)

admin.site.register(CatalogueSolution, CatalogueSolutionAdmin)
admin.site.register(FacturationItem, FacturationItemAdmin)
admin.site.register(ItemQuantite, ItemQuantiteAdmin)

admin.site.register(Ensolleilement)
admin.site.register(ModulesPV, ModulesPVAdmin)

admin.site.register(Projet, ProjetAdmin)
admin.site.register(Enseigne, EnseigneAdmin)

# # # # #

admin.site.register(CourbeChargePerso)
admin.site.register(ProfilPerso)

# # # # #

# # admin.site.register(Main_doeuvre, Main_doeuvreAdmin)
# # admin.site.register(Tableaux, TableauxAdmin)
# # admin.site.register(Cables, CablesAdmin)
# # admin.site.register(Cheminement, CheminementAdmin)
# # admin.site.register(Divers, DiversAdmin)
# # admin.site.register(Inge, IngeAdmin)
# # admin.site.register(Structure, StructureAdmin)
# # admin.site.register(BDDBat, BDDBatAdmin)
# # admin.site.register(Emisission_CO2, Emisission_CO2Admin)
# # admin.site.register(Hyp_cout_mobilite, Hyp_cout_mobiliteAdmin)
# admin. site.register(EZ_DRIVE, EZ_DRIVEAdmin)

# # admin.site.register(Monitoring, MonitoringAdmin)
# # admin.site.register(Tailles_Standards, Tailles_StandardAdmin)
# # admin.site.register(Batteries, BatterieAdmin)
# # admin.site.register(Extensions_Batteries, Extensions_BatteriesAdmin)
