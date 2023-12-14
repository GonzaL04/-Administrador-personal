from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from .forms import CreateUserForm

# Create your views here.

def home(request):
    return render(request, 'home.html')

@login_required(login_url='signin')
def index(request):
    return render(request, 'principal/index.html')

#AUTENTICACIONES AUTENTICACIONES AUTENTICACIONES AUTENTICACIONES AUTENTICACIONES AUTENTICACIONES 
def signup(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data.get('email')
                if User.objects.filter(email=email).exists():
                    messages.error(request, "El mail ya está registrado.")
                else:
                    form.save()
                    user = form.cleaned_data.get('username')
                    messages.success(request, "La cuenta fue registrada exitosamente para " + user)
                    return redirect('signin')
    
        context = {'form': form}
        return render(request, 'register/signup.html', context)


def singout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.info(request, "Usuario o contraseña incorrectos")
        
        context = {}
        return render(request, 'login/signin.html', context)
#FIN AUTENTICACIONES FIN AUTENTICACIONES FIN AUTENTICACIONES FIN AUTENTICACIONES FIN AUTENTICACIONES 