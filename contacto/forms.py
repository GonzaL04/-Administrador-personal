from django.forms import ModelForm
from .models import Contacto

class ContactForm(ModelForm):
    class Meta:
        model = Contacto
        exclude = '__all__'