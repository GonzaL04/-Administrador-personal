from django.contrib.auth.models import User
from django.db import models
from datetime import date

# Create your models here.

class Contacto(models.Model):
    nombre = models.CharField(max_length=50, blank=False, null=False)
    apellido = models.CharField(max_length=50, blank=True, null=True)
    celular = models.CharField(max_length=12, blank=False, null=False)
    email = models.EmailField()
    compania = models.CharField(max_length=50, blank=True, null=True)
    fecha = models.DateField(default=date.today)
    notas = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre