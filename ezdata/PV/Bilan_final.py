from .mobilite import Economies_mobilite
from .MDE import Economies
from .solutions import Economies_pv
from .mobilite import Vehicule_thermique_annuel
from .MDE import Variables_mde, Economies
from .models import Emisission_CO2
import numpy as np
from .Input import *

Load_Input()

def Bilan1(panneau,conso_perso, profil, territ, surface, installation, puissance, NbrekWhfacture, Recurrencefacture,
                     Montantfacture, Nbreetages, type, NbreVS, NbkmanVS, NbreVU, NbkmanVU,nb_batiment,etat_batterie, etat_AutoProd,etat_entre_deux):
    rqt0= Emisission_CO2.objects.get(territ=territ)
    rqt1 = Emisission_CO2.objects.get(territ="Litre d'essence")
    prix_L_essence = rqt1.emission

    #Creation du tableau e l'onglet Bilan 1 Bât
    #Bilan_avant [0,0]: Economique : MDE/PV sur 1 an
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

    #Tous ce qui est util :
    Inaction = Economies_pv(panneau, conso_perso, profil, territ, surface, installation, puissance, NbrekWhfacture, Recurrencefacture,
                     Montantfacture, Nbreetages, type,etat_batterie, etat_AutoProd,etat_entre_deux)[3]

    Mobilite_1an= Vehicule_thermique_annuel(NbreVS, NbkmanVS, NbreVU, NbkmanVU)[4]

    Ancienne_conso= Variables_mde(NbrekWhfacture,Recurrencefacture,Montantfacture, surface,Nbreetages )[2]
    L_carburant= Vehicule_thermique_annuel(NbreVS, NbkmanVS, NbreVU, NbkmanVU)[3]


    Bilan_avant = np.zeros((3, 9), float)
    Bilan_avant[0,0] = Inaction[0]*nb_batiment
    Bilan_avant[0,1] = Mobilite_1an[0]
    Bilan_avant[0,2] =  Bilan_avant[0,0]  + Bilan_avant[0,1]


    Bilan_avant[0,3] = sum(Inaction[0:9])*nb_batiment
    Bilan_avant[0,4] = sum(Mobilite_1an[0:9])
    Bilan_avant[0,5] = Bilan_avant[0,3] + Bilan_avant[0,4]

    Bilan_avant[0, 6] = sum(Inaction[0:19])*nb_batiment
    Bilan_avant[0, 7] = sum(Mobilite_1an[0:19])
    Bilan_avant[0, 8] = Bilan_avant[0, 6] + Bilan_avant[0, 7]

    Bilan_avant[1, 0] = Ancienne_conso*nb_batiment
    Bilan_avant[1, 1] = 0
    Bilan_avant[1, 2] = Bilan_avant[1, 0] + Bilan_avant[1, 1]

    Bilan_avant[1, 3] = Ancienne_conso*10*nb_batiment
    Bilan_avant[1, 4] = 0
    Bilan_avant[1, 5] = Bilan_avant[1, 3] + Bilan_avant[1, 4]

    Bilan_avant[1, 6] = Bilan_avant[1, 3]*2
    Bilan_avant[1, 7] = 0
    Bilan_avant[1, 8] = Bilan_avant[1, 6] + Bilan_avant[1, 7]

    Bilan_avant[2, 0] =  Bilan_avant[1, 0]* rqt0.emission
    Bilan_avant[2, 1] = L_carburant[0] *prix_L_essence
    Bilan_avant[2, 2] = Bilan_avant[2, 0] + Bilan_avant[2, 1]

    Bilan_avant[2, 3] = Bilan_avant[1, 3]* rqt0.emission
    Bilan_avant[2, 4] = Bilan_avant[2, 1]*10
    Bilan_avant[2, 5] = Bilan_avant[2, 3] + Bilan_avant[2, 4]

    Bilan_avant[2, 6] = Bilan_avant[1, 6]*rqt0.emission
    Bilan_avant[2, 7] = Bilan_avant[2, 4]*2
    Bilan_avant[2, 8] = Bilan_avant[2, 6] + Bilan_avant[2, 7]



    return Bilan_avant


def  Bilan2(panneau, conso_perso, profil, territ, surface, installation, puissance, NbrekWhfacture, Recurrencefacture,
                     Montantfacture, Nbreetages, type, NbreVS, NbkmanVS, NbreVU, NbkmanVU,Presenceparking, Nb_pdc_choisi, Accessibilite_parking, Optionborne,nb_batiment,etat_batterie, etat_AutoProd,etat_entre_deux):

    Bilan_avant= Bilan1(panneau, conso_perso, profil, territ, surface, installation, puissance, NbrekWhfacture, Recurrencefacture,
                     Montantfacture, Nbreetages, type, NbreVS, NbkmanVS, NbreVU, NbkmanVU,nb_batiment,etat_batterie, etat_AutoProd,etat_entre_deux)

    Bilan_apres = np.zeros((3, 9), float)

    Economies_MDE = Economies(NbrekWhfacture, Recurrencefacture, Montantfacture, surface, Nbreetages, type, territ)
    Economies_PV=  Economies_pv(panneau, conso_perso, profil, territ, surface,installation, puissance,NbrekWhfacture,Recurrencefacture,Montantfacture,Nbreetages,type,etat_batterie, etat_AutoProd,etat_entre_deux)
    Economies_Mobilite= Economies_mobilite(territ,NbreVS,NbkmanVS,NbreVU,NbkmanVU,Presenceparking, Nb_pdc_choisi, Accessibilite_parking, Optionborne, NbrekWhfacture, Recurrencefacture, Montantfacture, surface, Nbreetages)

    #Projection des coûts Après Actions : Economique
    Bilan_apres[0,0]= Bilan_avant[0][0]- Economies_MDE[0][0]*nb_batiment-Economies_PV[0][0]*nb_batiment
    Bilan_apres[0,1]=Bilan_avant[0][1]-Economies_Mobilite[0][0]
    Bilan_apres[0, 2] = Bilan_apres[0,0]+ Bilan_apres[0,1]

    Bilan_apres[0,3]= Bilan_avant[0][3]- Economies_MDE[0][1]*nb_batiment-Economies_PV[0][1]*nb_batiment
    Bilan_apres[0,4]=Bilan_avant[0][4]-Economies_Mobilite[0][1]
    Bilan_apres[0, 5] = Bilan_apres[0,3]+ Bilan_apres[0,4]

    Bilan_apres[0, 6] = Bilan_avant[0][6] - Economies_MDE[0][2]*nb_batiment - Economies_PV[0][2]*nb_batiment
    Bilan_apres[0, 7] = Bilan_avant[0][7]  - Economies_Mobilite[0][2]
    Bilan_apres[0, 8] = Bilan_apres[0, 6] + Bilan_apres[0, 7]

    #Projection des coûts Après Actions : Energetique


    Bilan_apres[1, 0] = Bilan_avant[1][0]  - Economies_MDE[1][0]*nb_batiment - Economies_PV[1][0]*nb_batiment
    Bilan_apres[1, 1] = 0
    Bilan_apres[1, 2] = Bilan_apres[1, 0] + Bilan_apres[1, 1]

    Bilan_apres[1,3]= Bilan_avant[1][3] - Economies_MDE[1][1]*nb_batiment-Economies_PV[1][1]*nb_batiment
    Bilan_apres[1,4]=0
    Bilan_apres[1, 5] = Bilan_apres[1,3]+ Bilan_apres[1,4]

    Bilan_apres[1, 6] = Bilan_avant[1][6]  - Economies_MDE[1][2]*nb_batiment - Economies_PV[1][2]*nb_batiment
    Bilan_apres[1, 7] =0
    Bilan_apres[1, 8] = Bilan_apres[1, 6] + Bilan_apres[1, 7]


    #Projection des coûts Après Actions : Environnement

    Bilan_apres[2,0]= Bilan_avant[2][0] - Economies_MDE[2][0]*nb_batiment-Economies_PV[2][0]*nb_batiment


    Bilan_apres[2,1]=Bilan_avant[2][1] -Economies_Mobilite[1][0]
    Bilan_apres[2, 2] = Bilan_apres[2,0]+ Bilan_apres[2,1]

    Bilan_apres[2,3]= Bilan_avant[2][3] - Economies_MDE[2][1]*nb_batiment-Economies_PV[2][1]*nb_batiment

    print( Bilan_avant[2][3])
    Bilan_apres[2,4]=Bilan_avant[2][4] -Economies_Mobilite[1][1]
    Bilan_apres[2, 5] = Bilan_apres[2,3]+ Bilan_apres[2,4]

    Bilan_apres[2, 6] = Bilan_avant[2][6]  - Economies_MDE[2][2]*nb_batiment - Economies_PV[2][2]*nb_batiment
    Bilan_apres[2, 7] = Bilan_avant[2][7]  - Economies_Mobilite[1][2]
    Bilan_apres[2, 8] = Bilan_apres[2, 6] + Bilan_apres[2, 7]



    return Bilan_apres

























