from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
from .models import Contacto
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

#Pagina index Contacto
def indexContacto(request):
    contactos = Contacto.objects.filter(user=request.user)
    context = {'contactos': contactos}
    return render(request, 'contacto/indexContacto.html', context)


#Agregar Contacto
@login_required(login_url='signin')
def agregar_contacto(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        celular = request.POST.get('celular')
        email = request.POST.get('email')
        compania = request.POST.get('compania')
        fecha = request.POST.get('fecha')
        notas = request.POST.get('notas')
        
        if not fecha:
            fecha = timezone.now().strftime('%Y-%m-%d')

        nuevo_contacto = Contacto(nombre=nombre, apellido=apellido, celular=celular, email=email, compania=compania, fecha=fecha, notas=notas, user=request.user)
        nuevo_contacto.save()

        return redirect('indexContacto')
    
    return redirect('indexContacto')

#Editar contacto
def editar_contacto(request, contacto_id):
    contacto = get_object_or_404(Contacto, id=contacto_id)

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        celular = request.POST.get('celular')
        email = request.POST.get('email')
        compania = request.POST.get('compania')
        fecha = request.POST.get('fecha')
        notas = request.POST.get('notas')
        
        if not fecha:
            fecha = timezone.now().strftime('%Y-%m-%d')

        contacto.nombre = nombre
        contacto.apellido = apellido
        contacto.celular = celular
        contacto.email = email
        contacto.compania = compania
        contacto.fecha = fecha
        contacto.notas = notas

        contacto.save()
        
        return redirect('indexContacto')

    return render(request, 'contacto/indexContacto.html', {'contacto': contacto})

#Borrar contacto
def borrar_contacto(request, id):
    contacto = Contacto.objects.get(id=id)
    contacto.delete()
    return redirect('indexContacto')