import numpy as np
from .solutions import courbe_de_charges,courbe_irradiation

PR= 0.81 #A modifier ?
Rendement_batteries_Lithium= 0.95
Decharge_maximale_batteries_Lithium = 0.8
Perte1 = 0.05 #%
Nb_jours_ouvres= 261
Nb_jours_favorables= 219
Ep_moyenne= 4 #kWh/kWc
Ep_defavorable= 2.5 #kWh/kWc
Ep_favorable= 5 #kWh/kWc
hL = 6 #h
So = 12 #h
H_soleil = 5.41 #kWh/m2


def Profil_personalise(Nuit_jourouvre,Nuit_weekend,Matin_jourouvre,Matin_weekend,Matinee_jourouvre,
                       Matinee_weekend,Midi_jourouvre,Midi_weekend,Apresmidi_jourouvre,Apresmidi_weekend,
                        Soir_jourouvre,Soir_weekend):
    #Profil personnalisé :
    Nuit_jourouvre= Nuit_jourouvre/100
    Nuit_weekend= Nuit_weekend/100

    Matin_jourouvre= Matin_jourouvre/100
    Matin_weekend= Matin_weekend/100

    Matinee_jourouvre= Matinee_jourouvre/100
    Matinee_weekend= Matinee_weekend/100

    Midi_jourouvre= Midi_jourouvre/100
    Midi_weekend= Midi_weekend/100

    Apresmidi_jourouvre= Apresmidi_jourouvre/100
    Apresmidi_weekend= Apresmidi_weekend/100

    Soir_jourouvre= Soir_jourouvre/100
    Soir_weekend= Soir_weekend/100

    coeffs_ouvre = np.matrix([Nuit_jourouvre, Nuit_jourouvre, Nuit_jourouvre, Nuit_jourouvre, Nuit_jourouvre,
             Nuit_jourouvre, Nuit_jourouvre+(Matin_jourouvre-Nuit_jourouvre)/2,
             Matin_jourouvre, Matin_jourouvre, Matin_jourouvre+(Matinee_jourouvre-Matin_jourouvre)/2, Matinee_jourouvre, Matinee_jourouvre,
             Matinee_jourouvre+(Midi_jourouvre- Matinee_jourouvre)/2, Midi_jourouvre,
             Midi_jourouvre+(Apresmidi_jourouvre-Midi_jourouvre)/2, Apresmidi_jourouvre, Apresmidi_jourouvre, Apresmidi_jourouvre,
             Apresmidi_jourouvre+(Soir_jourouvre-Apresmidi_jourouvre)/3, (Apresmidi_jourouvre+(Soir_jourouvre-Apresmidi_jourouvre)/3)+(Soir_jourouvre-Apresmidi_jourouvre)/3,
             Soir_jourouvre,Soir_jourouvre, Soir_jourouvre+(Nuit_jourouvre-Soir_jourouvre)/3, (Soir_jourouvre+(Nuit_jourouvre-Soir_jourouvre)/3)+(Nuit_jourouvre-Soir_jourouvre)/3])

    coeffs_weekend = np.matrix([Nuit_weekend, Nuit_weekend, Nuit_weekend, Nuit_weekend, Nuit_weekend,
             Nuit_weekend, Nuit_weekend + (Matin_weekend - Nuit_weekend) / 2,
             Matin_weekend, Matin_weekend, Matin_weekend + (Matinee_weekend - Matin_weekend) / 2,
             Matinee_weekend, Matinee_weekend,
             Matinee_weekend + (Midi_weekend - Matinee_weekend) / 2, Midi_weekend,
             Midi_weekend + (Apresmidi_weekend - Midi_weekend) / 2, Apresmidi_weekend, Apresmidi_weekend,
             Apresmidi_weekend,
             Apresmidi_weekend + (Soir_weekend - Apresmidi_weekend) / 3,
             (Apresmidi_weekend + (Soir_weekend - Apresmidi_weekend) / 3) + (
                         Soir_weekend - Apresmidi_weekend) / 3,
             Soir_weekend, Soir_weekend, Soir_weekend + (Nuit_weekend - Soir_weekend) / 3,
             (Soir_weekend + (Nuit_weekend - Soir_weekend) / 3) + (Nuit_weekend - Soir_weekend) / 3])

    a = coeffs_ouvre.transpose()
    b = coeffs_weekend.transpose()

    return a,b

def Analyse_Production(Taille_centrale,Batterie,Decharge,territ, conso_perso,profil):
    compteur_jour_batterie_ouvre_nuageux = tab[:, 12][np.where(tab[:, 12] == 0)].size
    compteur_jour_batterie_ouvre_soleil = tab[:, 13][np.where(tab[:, 13] == 0)].size
    compteur_jour_batterie_weekend_nuageux = tab[:, 14][np.where(tab[:, 14] == 0)].size
    compteur_jour_batterie_weekend_soleil = tab[:, 15][np.where(tab[:, 15] == 0)].size

    ####Definition de l'état de la batterie pour l'heure 23:00 dans tous les cas (ensolléilé ouvré, weekend...)
    if (24 > compteur_jour_batterie_ouvre_soleil):
        tab[23][17] = tab[22][17] + tab[23][9] - tab[23][13]  # Etat batterie jour ouvré ensolleilé

    if (24 == compteur_jour_batterie_ouvre_soleil):
        tab[23][17] = tab[23][9] - tab[23][13]  # Etat batterie jour ouvré ensolleilé

    for i in range(23):
        if (i + 1 > compteur_jour_batterie_ouvre_nuageux):
            if i == 0:
                tab[i][16] = tab[0][16] + tab[i][8] - tab[i][12]
            tab[i][16] = tab[i - 1][16] + tab[i][8] - tab[i][12]

        if (i + 1 > compteur_jour_batterie_ouvre_nuageux):
            tab[i][16] = tab[i][8] - tab[i][12]  # Etat batterie jour ouvré nuageux

        if (i + 1 <= compteur_jour_batterie_ouvre_nuageux):
            tab[i][16] = tab[23][16] - np.sum(tab[0:i, 16])  # Etat batterie jour ouvré nuageux

        ########################################
        if (i + 1 > compteur_jour_batterie_ouvre_soleil):
            if i == 0:
                tab[i][17] = tab[0][17] + tab[i][9] - tab[i][13]  # Etat batterie jour ouvré ensolleilé

            tab[i][17] = tab[i - 1][17] + tab[i][9] - tab[i][13]  # Etat batterie jour ouvré ensolleilé

        if (i + 1 == compteur_jour_batterie_ouvre_soleil):
            tab[i][17] = tab[i][9] - tab[i][13]  # Etat batterie jour ouvré ensolleilé

        if (i + 1 < compteur_jour_batterie_ouvre_soleil):
            tab[i][17] = tab[23][17] - np.sum(tab[0:i, 13])  # Etat batterie jour ouvré ensolleilé

        ########################################

        if (i + 1 > compteur_jour_batterie_weekend_nuageux):
            if i == 0:
                tab[i][18] = tab[0][18] + tab[i][10] - tab[i][18]  # Etat batterie weekend ensolleilé

            tab[i][18] = tab[i - 1][18] + tab[i][10] - tab[i][18]  # Etat batterie weekend ensolleilé

        if (i + 1 > compteur_jour_batterie_weekend_nuageux):
            tab[i][18] = tab[i][10] - tab[i][14]  # Etat batterie weekend ensolleilé
        else:
            tab[i][18] = tab[23][18] - np.sum(tab[0:i, 18])  # Etat batterie weekend ensolleilé

        ########################################

        if (i + 1 > compteur_jour_batterie_weekend_soleil):
            if i == 0:
                tab[i][19] = tab[0][19] + tab[i][11] - tab[i][15]  # Etat batterie weekend nuageux

            tab[i][19] = tab[i - 1][19] + tab[i][11] - tab[i][15]  # Etat batterie weekend nuageux

        if (i + 1 > compteur_jour_batterie_weekend_soleil):
            tab[i][19] = tab[i][10] - tab[i][11]  # Etat batterie weekend nuageux
        else:
            tab[i][19] = tab[23][19] - np.sum(tab[0:i, 19])  # Etat batterie weekend nuageux

        # print(tab[i][13])

    for i in range(24):
        print(tab[i][17])

    #Retourne le tableau, le taux d'autoconso
