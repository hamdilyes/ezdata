from .models import *
from .solutions import *
from .mobilite import *
from .MDE import *
import numpy_financial as npf
from .catalogue import *

# gains sans loyer de revente de surplus


def update_esco(invest, taille, cout, reduc_esco_10, reduc_esco_20, surplus, auto_conso, prod_pv_an, tab_prix_elec):
    # renouvellement onduleur à l'année 11 : 0.1 €/kWc
    prix_onduleur = 0.1*taille/1000  # k€

    # taux d'autoconsommation
    taux_autoconso = auto_conso

    # production PV annuelle
    prod_pv_an = prod_pv_an

    # cout élec esco
    cout_esco = [0]*20
    for i in range(20):
        if i < 10:
            cout_esco[i] = cout[i]*(1-reduc_esco_10/100)
        else:
            cout_esco[i] = cout[i]*(1-reduc_esco_20/100)

    # capital dû
    cap_du = [0]*20
    cap_du[0] = invest*80/100/1000  # k€
    # facture EDF avec Autoconso
    new_facture = [0]*20
    new_facture[0] = cout[0]-tab_prix_elec[0]*taux_autoconso*prod_pv_an  # €
    # amortissement annuel
    amorti = [0]*20
    amorti[0] = invest/1000  # k€
    # annuités
    annuite = -npf.pmt(1.6/100, 20, invest*80/100/1000)  # k€
    taux_amorti = [0]*20
    taux_amorti[0] = max(1/20, 1/20*2.25)
    annuite_amorti = [0]*20
    annuite_amorti[0] = amorti[0]*taux_amorti[0]  # k€

    for i in range(1, 20):
        cap_du[i] = cap_du[i-1]-(annuite-cap_du[i-1]*1.6/100)
        new_facture[i] = cout[i]-tab_prix_elec[i]*taux_autoconso*prod_pv_an

        amorti[i] = amorti[i-1]-annuite_amorti[i-1]
        taux_amorti[i] = max(1/(20-i), 1/20*2.25)
        annuite_amorti[i] = amorti[i]*taux_amorti[i]

    # k€
    calcul_tri_van = [0]*21
    calcul_tri_van[0] += -invest/1000*20/100
    calcul_tri_van[11] += -prix_onduleur

    # numéros de ligne dans onglet "Economics" de la Préconfig sous Excel
    # 25, 30, 72, 87, 89, fonction VPM
    for i in range(1, 21):
        v_25 = (surplus/20*65/100+cout_esco[i-1]-new_facture[i-1])/1000  # k€
        v_30 = taille*18/1000  # k€
        v_72 = cap_du[i-1]*1.6/100  # k€
        v_89 = annuite_amorti[i-1]  # k€
        calcul_tri_van[i] += v_25-v_30+annuite-26.5/100 * \
            max((v_25-v_30-v_72-v_89), 0)

    tri_financier = npf.irr(calcul_tri_van)*100  # %
    van_5 = npf.npv(5/100, [calcul_tri_van[0]] +
                    calcul_tri_van)-calcul_tri_van[0]  # k€

    v_25 = (surplus/20*65/100+cout_esco[0]-new_facture[0])/1000  # k€
    v_30 = taille*18/1000  # k€

    taux_1 = np.abs((v_25-v_30)/annuite)
    taux_2 = np.abs(v_25/(v_30+annuite))

    return tri_financier, taux_1, taux_2, cout_esco


def esco(surface, NbrekWhfacture, Recurrencefacture, Montantfacture, Nbreetages, type, invest, taille, surplus, auto_conso, autoprod, prod_pv_an):
    reduc_esco_10 = int(autoprod)-1
    reduc_esco_20 = int(autoprod)-1
    cout = [0]*20

    # kWh/an
    conso_an = Variables_mde(
        NbrekWhfacture, Recurrencefacture, Montantfacture, surface, Nbreetages)[2]

    # prix élec €/kWh par an de 1 à 20
    tab_prix_elec = Coeffs_mde(
        NbrekWhfacture, Recurrencefacture, Montantfacture, surface, Nbreetages, type)[2]

    # cout élec sans esco
    for i in range(20):
        cout[i] = conso_an*tab_prix_elec[i]

    # choix des taux de réduction esco
    # tri > 7 %
    # taux > 1.15
    r1, r2 = 1, 1
    tri_financier, taux_1, taux_2 = update_esco(
        invest, taille, cout, reduc_esco_10, reduc_esco_20, surplus, auto_conso, prod_pv_an, tab_prix_elec)[:3]

    while taux_1 > 1.15 or taux_2 > 1.15:
        if r1 < autoprod-1:
            r1 += 1
            reduc_esco_10 = r1
            tri_financier, taux_1, taux_2 = update_esco(
                invest, taille, cout, reduc_esco_10, reduc_esco_20, surplus, auto_conso, prod_pv_an, tab_prix_elec)[:3]
        else:
            break

    r2 = r1
    reduc_esco_20 = r2
    tri_financier, taux_1, taux_2 = update_esco(
        invest, taille, cout, reduc_esco_10, reduc_esco_20, surplus, auto_conso, prod_pv_an, tab_prix_elec)[:3]

    while tri_financier < 7 and r1 > 1 and r2 > 1:
        r2 -= 1
        reduc_esco_20 = r2
        tri_financier, taux_1, taux_2 = update_esco(
            invest, taille, cout, reduc_esco_10, reduc_esco_20, surplus, auto_conso, prod_pv_an, tab_prix_elec)[:3]
        if tri_financier < 7 and r1 > 1 and r2 > 1:
            r1 -= 1
            reduc_esco_10 = r1
            tri_financier, taux_1, taux_2 = update_esco(
                invest, taille, cout, reduc_esco_10, reduc_esco_20, surplus, auto_conso, prod_pv_an, tab_prix_elec)[:3]

    print("TRI", tri_financier, "TAUX", taux_1, taux_2,
          "REDUC", reduc_esco_10, reduc_esco_20)

    cout_esco = update_esco(invest, taille, cout, reduc_esco_10,
                            reduc_esco_20, surplus, auto_conso, prod_pv_an, tab_prix_elec)[3]
    # gains esco
    gains = sum([cout[i]-cout_esco[i] for i in range(20)])

    # le client reçoit 35% de la revente de surplus
    gains += surplus*35/100

    return gains, reduc_esco_10, reduc_esco_20
