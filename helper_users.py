#views.py

from django.shortcuts import render, redirect

def welcome(request):
    return render(request, "users/welcome.html")

def register(request):
    return render(request, "users/register.html")

def login(request):
    return render(request, "users/login.html")

def logout(request):
    # Redireccionamos a la portada
    return redirect('/')
#Las URL que las manejarán serán las siguientes:

proyecto/urls.py

from django.contrib import admin
from django.urls import path
from users import views

urlpatterns = [
    path('', views.welcome),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),

    path('admin/', admin.site.urls),
]
#Implementando el logout encontraremos en el módulo django.contrib.auth. Os sugiero importar la función con otro nombre porque de esa forma podemos usar logout en la función de la vista:

views.py

from django.contrib.auth import logout as do_logout

# ...

def logout(request):
    # Finalizamos la sesión
    do_logout(request)
    # Redireccionamos a la portada
    return redirect('/')
Tan sencillo como esto.

# nos centraremos en añadir una validación a la portada que redireccione al usuario al login en caso de no estar autenticado, así protegeremos su contenido: en views.py

def welcome(request):
    # Si estamos identificados devolvemos la portada
    if request.user.is_authenticated:
        return render(request, "users/welcome.html")
    # En otro caso redireccionamos al login
    return redirect('/login')


#welcome.html

<h2>Área para miembros</h2>

<p>
    Bienvenido <b>{{request.user.username}}</b>, 
    esta página es exclusiva para usuarios registrados.
</p>

<hr />
<a href="/logout">Cerrar sesión</a>

#Al añadir este código si intentamos acceder a la la raíz del sitio / nos redireccionará al /login que aún no hemos creado. En caso de ver la portada podría ser por tener una sesión activa préviamente desde el panel de administrador, ya que se gestionan con la misma app interna de Django. Si la cerráis desde el enlace inferior os llevará al login.

#Implementando el login. El formulario de identificación es la cosa más sencilla del mundo, sólo necesitamos un campo para el nombre del usuario y otro para la contraseña. Podríamos crearlos manualmente pero también podemos usar los built-in forms de Django.

#Así que vamos a importar el formulario de autenticación llamado AuthenticationForm y dejaremos que él lo gestione todo, nosotros sólo lo validaremos e iniciaremos la sesión si la información es correcta:

views.py

from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as do_login

# ...

def login(request):
    # Creamos el formulario de autenticación vacío
    form = AuthenticationForm()
    if request.method == "POST":
        # Añadimos los datos recibidos al formulario
        form = AuthenticationForm(data=request.POST)
        # Si el formulario es válido...
        if form.is_valid():
            # Recuperamos las credenciales validadas
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Verificamos las credenciales del usuario
            user = authenticate(username=username, password=password)

            # Si existe un usuario con ese nombre y contraseña
            if user is not None:
                # Hacemos el login manualmente
                do_login(request, user)
                # Y le redireccionamos a la portada
                return redirect('/')

    # Si llegamos al final renderizamos el formulario
    return render(request, "users/login.html", {'form': form})

#El template quedaría de la siguiente forma, dejando que sea el propio Django quién renderice el formulario:

#login.html

<h2>Iniciar sesión</h2>

<form method="POST">
    {{ form.as_p }}
    {% csrf_token %}
    <button type="submit">Login</button>
</form>

<hr />
<a href="/register">Registrar usuario</a>


#views.py

from django.contrib.auth.forms import UserCreationForm

# ...

def register(request):
    # Creamos el formulario de autenticación vacío
    form = UserCreationForm()
    if request.method == "POST":
        # Añadimos los datos recibidos al formulario
        form = UserCreationForm(data=request.POST)
        # Si el formulario es válido...
        if form.is_valid():

            # Creamos la nueva cuenta de usuario
            user = form.save()

            # Si el usuario se crea correctamente 
            if user is not None:
                # Hacemos el login manualmente
                do_login(request, user)
                # Y le redireccionamos a la portada
                return redirect('/')

    # Si llegamos al final renderizamos el formulario
    return render(request, "users/register.html", {'form': form})

#El template sería prácticamente un calco del de login:

#register.html

<h2>Registrar usuario</h2>

<form method="POST">
    {{ form.as_p }}
    {% csrf_token %}
    <button type="submit">Registrar</button>
</form>

<hr />

<a href="/login">Iniciar sesión</a>


#Este formulario de registro tiene la peculiaridad de contener mucho texto de ayuda a la hora de crear las cuentas, pero si queremos podemos esconder esa información borrando el atributo help_text de los tres campos del formulario:

#views.py

# Si queremos borramos los campos de ayuda
form.fields['username'].help_text = None
form.fields['password1'].help_text = None
form.fields['password2'].help_text = None

# Si llegamos al final renderizamos el formulario
return render(request, "users/register.html", {'form': form})

