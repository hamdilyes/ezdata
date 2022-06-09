from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import *


class UserForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ['email', 'entite']


class UpdateUserForm(forms.ModelForm):
    entite = forms.CharField(max_length=255,
                             required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = MyUser
        fields = ['email', 'entite']


# class UserAdminChangeForm(forms.ModelForm):

#     class Meta:
#         model = MyUser
#         fields = ['email', 'entite', 'is_active', 'is_staff', 'is_admin']
