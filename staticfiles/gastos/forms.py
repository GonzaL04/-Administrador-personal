from .models import Categorias,Cuentas,Gastos
from django import forms

class GastoForm(forms.ModelForm):
    class Meta:
        model = Gastos
        fields = ['fk_id_categoria','descripción','precio','fecha']

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Cuentas
        fields = ['nombre']

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categorias
        fields = ['nombre']

