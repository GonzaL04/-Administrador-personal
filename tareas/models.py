from django.db import models
from django.contrib.auth.models import User
from contacto.models import Contacto

class Tareas(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(max_length=1000)
    fcreada = models.DateTimeField(auto_now_add=True)
    fcompletada = models.DateTimeField(null=True, blank=True)
    importante = models.BooleanField(default=False)
    contacto = models.ManyToManyField(Contacto, related_name='tareas')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ESTADO_TAREA = (
        ('pendiente', 'Pendiente'),
        ('en_curso', 'En Curso'),
        ('completada', 'Completada'),
    )
    estado = models.CharField(max_length=20, choices=ESTADO_TAREA, default='pendiente')
    
    def __str__(self):
        return self.titulo + ' - ' + self.user.username
