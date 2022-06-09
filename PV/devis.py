from .models import *


def Modules(client, batiment, centrale, toiture, territ):

    l = []
    rqt_taxe = Taxe.objects.get(territ=territ)
    rqt0 = Catalogue_GT.objects.filter(
        tailles=centrale).filter(toiture=toiture)[0]
    panneau = rqt0.Panneau.all()

    for i in panneau:
        nb_module = int(centrale.taille/(i.Puissance_modulaire_kW))
        a = Modules_factu_ModulesPV(ModulesPV=i, client=client, batiment=batiment, qt=nb_module, cout_unitaire=i.Cout, cout_unitaire_transport=(rqt_taxe.transport_2*i.Cout)/100,
                                    cout_total=nb_module*i.Cout, cout_total_transport=nb_module*(rqt_taxe.transport_2*i.Cout)/100, marge=(nb_module*i.Cout * rqt0.Marge),
                                    prix=nb_module*i.Cout+nb_module *
                                    (rqt_taxe.transport_2*i.Cout)/100 +
                                    (nb_module*i.Cout * rqt0.Marge),
                                    prix_unitaire=(nb_module*i.Cout+nb_module*(rqt_taxe.transport_2*i.Cout)/100+(nb_module*i.Cout * rqt0.Marge))/nb_module)

        a.save()
        l.append(a)

    return l


def Fixation(centrale, batterie):
    l = []

    return l


def Lestage(centrale, batterie):
    l = []

    return l


def Onduleur(centrale, batterie):
    l = []

    return l


def Monito(centrale, batterie):
    l = []

    return l


def Batterie(centrale, batterie):
    l = []

    return l


def Extension(centrale, batterie):
    l = []

    return l


def Cables(centrale, batterie):
    l = []

    return l


def Cheminement(centrale, batterie):
    l = []

    return l


def Tableaux(centrale, batterie):
    l = []

    return l


def PosePV(centrale, batterie):
    l = []

    return l


def Controle(centrale, batterie):
    l = []

    return l


def Ingénieurie(centrale, batterie):
    l = []

    return l
