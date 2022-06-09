class Catalogue_GT(models.Model):
    toit = (('Tôle', 'Tôle '),
             ('Terasse', 'Terasse '))

    tailles= models.ManyToManyField(Tailles_Standards, blank=True)
    toiture = models.CharField(verbose_name="Type de toiture", choices=toit, max_length=255)

    Panneau= models.ManyToManyField(ModulesPV, blank=True, through='Modules_factu')
    Fixation=  models.ManyToManyField(Structure,  blank=True, through='Modules_factu')
    Onduleurs= models.ManyToManyField(Onduleurs,  blank=True, through='Modules_factu')
    Monitoring= models.ManyToManyField(Monitoring,  blank=True, through='Modules_factu')
    Batteries = models.ManyToManyField(Batteries, blank=True, through='Modules_factu')
    Extensions_Batteries= models.ManyToManyField(Extensions_Batteries, blank=True, through='Modules_factu')
    Cables = models.ManyToManyField(Cables, blank=True, through='Modules_factu')
    Tableaux = models.ManyToManyField(Tableaux, blank=True)
    Cheminement = models.ManyToManyField(Cheminement, blank=True, through='Modules_factu')
    Divers = models.ManyToManyField(Divers, blank=True, through='Modules_factu')
    Main_doeuvre = models.ManyToManyField(Main_doeuvre, blank=True, through='Modules_factu')


    def __str__(self):
        rqt0= self.tailles.all()
        rqt1= rqt0.values_list('taille', 'catag')
        value = np.array(rqt1).flatten().tolist()
        return str(value) + " : " + str(self.toiture)

class Factu_batiment(models.Model):
    batiment = models.ForeignKey(Batiment, on_delete=models.CASCADE, blank=True)
    devis= models.ForeignKey(Batiment, on_delete=models.CASCADE, related_name='qt_devis',  blank=True)



class Modules_factu(models.Model):
    nom = models.ForeignKey(Catalogue_GT,  on_delete=models.CASCADE)
    onduleur = models.ForeignKey(Onduleurs,  on_delete=models.CASCADE)
    panneau = models.ForeignKey(ModulesPV,  on_delete=models.CASCADE)
    fixation = models.ForeignKey(Structure,  on_delete=models.CASCADE)
    monitoring = models.ForeignKey(Monitoring,  on_delete=models.CASCADE)
    batterie = models.ForeignKey(Batteries,  on_delete=models.CASCADE)
    extension = models.ForeignKey(Extensions_Batteries,  on_delete=models.CASCADE)
    cables = models.ForeignKey(Cables,  on_delete=models.CASCADE)
    tableau = models.ForeignKey(Tableaux,  on_delete=models.CASCADE)
    cheminement = models.ForeignKey(Cheminement,  on_delete=models.CASCADE)
    divers = models.ForeignKey(Divers,  on_delete=models.CASCADE)
    main_doeuvre = models.ForeignKey(Main_doeuvre,  on_delete=models.CASCADE)

    qt = models.PositiveIntegerField(verbose_name='Quantité')
    cout_unitaire= models.PositiveIntegerField(verbose_name='Coût HA unitaire')
    cout_unitaire_transport = models.PositiveIntegerField(verbose_name='Coût Unitaire Transport', blank=True)
    cout_total = models.PositiveIntegerField(verbose_name='Coût Total HA')
    cout_total_transport = models.PositiveIntegerField(verbose_name='Coût Total Transport',  blank=True)
    marge = models.PositiveIntegerField()
    prix=models.PositiveIntegerField(verbose_name='Prix Vendu')
    prix_unitaire=models.PositiveIntegerField(verbose_name='Prix Unitaire')





class Modules_factu_Onduleurs(Info_facturation):
    Onduleur = models.ForeignKey(Onduleurs,  on_delete=models.CASCADE)

class Modules_factu_Fixation(Info_facturation):
    Fixation = models.ForeignKey(Structure, on_delete=models.CASCADE)

class Modules_factu_Lestage(Info_facturation):
    Lestage = models.ForeignKey(Structure, on_delete=models.CASCADE)

class Modules_factu_Monitoring(Info_facturation):
    Monitoring = models.ForeignKey(Monitoring, on_delete=models.CASCADE)

class Modules_factu_Batteries(Info_facturation):
    Batteries = models.ForeignKey(Batteries, on_delete=models.CASCADE)

class Modules_factu_Extensions_Batteries(Info_facturation):
    Extensions_Batteries = models.ForeignKey(Extensions_Batteries, on_delete=models.CASCADE)

class Modules_factu_Cables(Info_facturation):
    Cables = models.ForeignKey(Cables, on_delete=models.CASCADE)

class Modules_factu_Tableaux(Info_facturation):
    Tableaux = models.ForeignKey(Tableaux, on_delete=models.CASCADE)

class Modules_factu_Cheminement(Info_facturation):
    Cheminement = models.ForeignKey(Cheminement, on_delete=models.CASCADE)

class Modules_factu_Divers(Info_facturation):
    Divers = models.ForeignKey(Divers, on_delete=models.CASCADE)

class Modules_factu_Main_doeuvre(Info_facturation):
    Main_doeuvre = models.ForeignKey(Main_doeuvre, on_delete=models.CASCADE)

