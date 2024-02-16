from typing import Any, Mapping
from django import forms
from django.forms.renderers import BaseRenderer
from django.forms.utils import ErrorList
from .models import User

from django.contrib.auth import authenticate



class CreateUserForm(forms.ModelForm):
    
    password1 = forms.CharField(
        label = 'Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder':'Ingrese contraseña'
            }
        )
    )
    
    password2 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder':'Repita contraseña'
            }
        )
    )
    
    
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'nombres',
            'apellidos',
            'genero',
            )
    
    
    def clean_password2(self):
        if self.cleaned_data['password2'] != self.cleaned_data['password1']:
            self.add_error('password2', 'Las contraseñas no coinciden')



class LoginUserForm(forms.Form):
    
    username = forms.CharField(
        label='Usuario',
        required=True,
        widget=forms.TextInput(
            attrs={'placeholder':'Usuario'}
        )
    )
    
    password = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={'placeholder':'Contraseña'}
        )
    )

    
    def clean(self):
        cleaned_data = super(LoginUserForm, self).clean()
        
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        
        if not authenticate(username=username, password=password):
            raise forms.ValidationError('Usuario o contraseña erronea')
        
        return self.cleaned_data



class UpdateUserForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = (            
            'nombres',
            'apellidos',
            'genero',
            'email',
            
        )
    


class VerificationUserForm(forms.Form):
    
    codregistro = forms.CharField(required=True)
    
    
    def __init__(self, pk, *args, **kwargs):
        self.id_user=pk
        super(VerificationUserForm, self).__init__(*args, **kwargs)
        
        
    def clean_codregistro(self):
        codigo = self.cleaned_data['codregistro']
        
        if len(codigo)==6:
            activo = User.objects.cod_validation(self.id_user, codigo)
        if not activo:
            raise forms.ValidationError('El codigo no existe')



class UpdatePasswordForm(forms.Form):
    
    password1 = forms.CharField(
        label='Contraseña Actual',
        required=True,
        widget=forms.PasswordInput(
            attrs={'placeholder':'Contraseña Actual'}
        )
    )
    
    
    password2 = forms.CharField(
        label='Nueva Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={'placeholder':'Nueva Contraseña'}
        )
    )