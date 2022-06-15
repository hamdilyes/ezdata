from django import forms
from django.forms import ModelForm
from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from .models import *


class CsvImportForm(forms.Form):
    csv_file = forms.FileField()


class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = ['nom_entreprise', 'mail']

    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['nom_entreprise'].widget.attrs['placeholder'] = 'Green Technologie'
        self.fields['mail'].widget.attrs['placeholder'] = 'contact@greentechnologie.net'


class LocalisationForm(ModelForm):
    class Meta:
        model = Localisation
        fields = ('territ', 'adresse',)
        widget = {'Territoire': forms.Select(attrs={'class': 'form-control'}),
                  'Adresse': forms.Select(attrs={'class': 'form-control'}),
                  }

    def __init__(self, *args, **kwargs):
        super(LocalisationForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class EnseigneForm(ModelForm):
    class Meta:
        model = Enseigne
        fields = ('projet', 'name', 'secteur', 'effectif')
        widget = {'Projet': forms.Select(attrs={'class': 'form-control'}),
                  "Nom de l'enseigne": forms.Select(attrs={'class': 'form-control', 'placeholder': "Nom de l'enseigne"}),
                  'Secteur': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Services'}),
                  'Effectif': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '55'}),
                  }

    def __init__(self, *args, **kwargs):
        super(EnseigneForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['placeholder'] = "Nom de l'enseigne"
        self.fields['secteur'].widget.attrs['placeholder'] = 'Services'
        self.fields['effectif'].widget.attrs['placeholder'] = '55'


class ProjetForm(ModelForm):
    class Meta:
        model = Projet
        fields = ('name',)
        widget = {"Nom": forms.Select(
            attrs={'class': 'form-control', 'placeholder': "Nom du projet"})}

    def __init__(self, *args, **kwargs):
        super(ProjetForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['placeholder'] = 'Nom du projet'


class BatimentForm(ModelForm):
    class Meta:
        model = Batiment
        fields = ('type_batiment', 'nb_batiment',
                  'taille', 'nb_etages', 'num_sites')
        widget = {'type_batiment': forms.Select(attrs={'class': 'form-control'}),
                  'nb_batiment': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '10'}),
                  'taille': forms.Select(attrs={'class': 'form-control'}),
                  'nb_etages': forms.Select(attrs={'class': 'form-control'})
                  }

    def __init__(self, *args, **kwargs):
        super(BatimentForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['nb_batiment'].widget.attrs['placeholder'] = '10'
        self.fields['nb_etages'].widget.attrs['placeholder'] = '1'


class ProfilForm(ModelForm):
    class Meta:
        model = Profil
        fields = ('type_profil', )
        widget = {'Profil': forms.Select(attrs={'class': 'form-control'}),
                  }

    def __init__(self, *args, **kwargs):
        super(ProfilForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ProfilPersoForm(ModelForm):
    class Meta:
        model = ProfilPerso
        fields = ('profil',)
        widget = {'profil': forms.Select(attrs={'class': 'form-control'}),
                  }

    def __init__(self, *args, **kwargs):
        super(ProfilPersoForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class CourbeChargePersoForm(ModelForm):
    class Meta:
        model = CourbeChargePerso
        fields = ('name', 'type', 'coeff_0', 'coeff_1', 'coeff_2', 'coeff_3', 'coeff_4', 'coeff_5', 'coeff_6', 'coeff_7', 'coeff_8', 'coeff_9', 'coeff_10', 'coeff_11',
                  'coeff_12', 'coeff_13', 'coeff_14', 'coeff_15', 'coeff_16', 'coeff_17', 'coeff_18', 'coeff_19', 'coeff_20', 'coeff_21', 'coeff_22', 'coeff_23',)
        widget = {'name': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Nom du profil'}),
                  }

    def __init__(self, *args, **kwargs):
        super(CourbeChargePersoForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ToitureForm(ModelForm):
    class Meta:
        model = Toiture
        fields = ('toiture', 'surface')
        widget = {'Toiture': forms.Select(attrs={'class': 'form-control'}),
                  'Surface': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '100'}),
                  }

    def __init__(self, *args, **kwargs):
        super(ToitureForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ElectrificationForm(ModelForm):
    class Meta:
        model = Electrification
        fields = ('installation',)
        widget = {'Installation ': forms.Select(attrs={'class': 'form-control'}),
                  }

    def __init__(self, *args, **kwargs):
        super(ElectrificationForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class SouscriptionForm(ModelForm):
    class Meta:
        model = EDF
        fields = ('puissance', 'reference', 'nb_kW', 'facture')
        widget = {'Puissance Souscrite ': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '15'}),
                  'Reference': forms.Select(attrs={'class': 'form-control'}),
                  'Nombre kWh facture': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '5000'}),
                  'Montant facture': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '950'}),
                  }

    def __init__(self, *args, **kwargs):
        super(SouscriptionForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['puissance'].widget.attrs['placeholder'] = '15'
        self.fields['nb_kW'].widget.attrs['placeholder'] = '5000'
        self.fields['facture'].widget.attrs['placeholder'] = '950'


class MobiliteForm(ModelForm):
    class Meta:
        model = Mobilite
        fields = ('vehicule_fonction', 'km_an_vehicule_fonction', 'vehicule_utilitaire', 'km_an_vehicule_utilitaire', 'parking',
                  'acces', 'borne', 'pt_de_charge')

    def __init__(self, *args, **kwargs):
        super(MobiliteForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['vehicule_fonction'].widget.attrs['placeholder'] = '2'
        self.fields['km_an_vehicule_fonction'].widget.attrs['placeholder'] = '10 000'
        self.fields['vehicule_utilitaire'].widget.attrs['placeholder'] = '2'
        self.fields['km_an_vehicule_utilitaire'].widget.attrs['placeholder'] = '20 000'
        self.fields['pt_de_charge'].widget.attrs['placeholder'] = '4'


class Dimens_Centrale(forms.Form):
    # For BooleanFields, required=False means that Django's validation
    # will accept a checked or unchecked value, while required=True
    # will validate that the user MUST check the box.
    Auto_Prod = forms.BooleanField(initial=False, required=False)
    Auto_Conso = forms.BooleanField(initial=True, required=False)
    Entre_les_deux = forms.BooleanField(required=False)
    Batteries = forms.BooleanField(required=False)
    Revente = forms.BooleanField(required=False)
    centrale_form = forms.DecimalField(required=True)
    batterie_form = forms.DecimalField(required=True)

    Auto_Prod.widget.attrs.update({'class': 'form-check form-switch ms-auto"'})
    Auto_Conso.widget.attrs.update(
        {'class': 'form-check form-switch ms-auto"'})
    Entre_les_deux.widget.attrs.update(
        {'class': 'form-check form-switch ms-auto"'})
    Batteries.widget.attrs.update({'class': 'form-check form-switch ms-auto"'})
    Revente.widget.attrs.update({'class': 'form-check form-switch ms-auto"'})


class Slider(forms.Form):
    slider_form = forms.DecimalField(
        required=True,
        label=False,
        widget=forms.TextInput(
            attrs={
                'step': '5',
                'type': 'round-slider',
                'value': '21',
                'min': '4',
                'max': '180'
            }
        )
    )
