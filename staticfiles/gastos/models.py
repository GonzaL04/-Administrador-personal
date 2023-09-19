from django.db import models
from django.contrib.auth.models import User

class Categorias(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=150)

    def __str__(self):
        return self.nombre

class Cuentas(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=150)
    fecha_de_creacion = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.nombre
    
class Gastos(models.Model):
    fk_id_categoria = models.ForeignKey(Categorias,on_delete=models.CASCADE,null = True)
    fk_id_cuenta = models.ForeignKey(Cuentas,on_delete=models.CASCADE, null = True)
    descripción = models.CharField(max_length=200,null=True,blank=True)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    fecha = models.DateField()

    def __str__(self):
        if( self.descripción == None):
            return "Gasto sin descripción ("+str(self.precio)+"$)"
        return self.descripción+" ("+str(self.precio)+"$)"