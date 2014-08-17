from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from models import ActividadForm, Actividad, ValidacionForm
from login.models import Estudiante, EstudianteForm
from django.db.models import Count, Min, Sum, Avg
from django.views.generic.edit import UpdateView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User

def completar_registro(request):
  
    # Vemos si el correo es usb.ve sino lo mandamos palco
    if request.user.email.endswith('usb.ve'):
      
        # Vemos si termino de completas su informacion de usuario
        try:
          usr = Estudiante.objects.get(user=request.user)
        except Estudiante.DoesNotExist:
          usr = None
          
        # Si no lo ha hecho lo mandamos a completar
        if usr == None:
            if request.method == 'POST':
                form = EstudianteForm(request.POST) # A form bound to the POST data
                if form.is_valid():
                    est = form.save(commit=False)
                    est.user = request.user
                    est.save()
                    horas = determinarHoras(est)
                    d = True
                    return render(request, 'main.html', {
                                  'dominio': d,
                                  'horas': horas,
                                  })
            else:
                form = EstudianteForm() 
                return render(request, 'account/registro.html', {
                    'form': form,
                })
        # Caso contrario bienvenido sea
        else:
            horas = determinarHoras(usr)
            d = True
            return render(request, 'main.html', {
                          'dominio': d,
                          'horas': horas,
                          })

    # Caso de un admin o nosotros
    elif request.user.email == 'arturo.voltattorni@gmail.com' or request.user.email == 'patrick.rengifo@gmail.com':
        d = True
        horas = 0
        return render(request, 'main.html', {
                      'dominio': d,
                      'horas': horas,
                      })
    # palco
    else:
        d = False
        horas = 0
        return render(request, 'main.html', {
                      'dominio': d,
                      'horas': horas,
                      })

# Vista para modificar los datos del usuario
class ProfileUpdate(UpdateView):
    model = Estudiante
    template_name = 'account/update.html'
    form_class = EstudianteForm
    success_url = reverse_lazy('registry') # This is where the user will be 
                                       # redirected once the form
                                       # is successfully filled in

    def get_object(self, queryset=None):
        '''This method will load the object
           that will be used to load the form
           that will be edited'''
        return self.request.user.estudiante

# Funcion para determinar las horas que ha realizado un estudiante (validadas)
def determinarHoras(est):

    horas = 0
    qs = Actividad.objects.filter(estudiante=est,validado=True)

    if qs:
        horas = qs.aggregate(Sum('horas')).get('horas__sum')
        print horas

    return horas

# Funcion para obtener las actividades realizadas por un estudiante
def actividades(request):

    est = Estudiante.objects.get(user=request.user)
    acts = Actividad.objects.filter(estudiante=est)

    return render(request, 'actividades.html', {
                  'acts': acts,
                  })


# Funcion para obtener las actividades sin validar
def obtenerActividadesSinValidar():
    i = 1
    forms = []
    acts = Actividad.objects.filter(validado=False)

    for x in acts:

        data = {'estudiante': x.estudiante}

        cform = []
        cform.append(ValidacionForm(instance = x))
        cform.append(x.estudiante.user.first_name)
        cform.append(x.estudiante.user.last_name)
        cform.append(x.estudiante.carnet)
        cform.append(x.horas)
        cform.append(x.descripcion)
        cform.append(x.fecha)
        cform.append(x.estudiante)
        forms.append(cform)
        i += 1

    return forms

def validacion(request):

    cforms = obtenerActividadesSinValidar()
    return render(request, 'validacion.html' , 
                  { 'forms': cforms, })

def guardarValidacion(request, id):

    print(id)
    act = Actividad.objects.get(pk = id)
    print(act.descripcion)
    form = ValidacionForm(request.POST, instance = act) # A form bound to the POST data
    if form.is_valid():
        form.save()
        print('SALVE')

    cforms = obtenerActividadesSinValidar()
    return render(request, 'validacion.html' , 
                  { 'forms': cforms, })


def registroActividad(request):
    if request.method == 'POST':
        form = ActividadForm(request.POST) # A form bound to the POST data
        print form.errors
        if form.is_valid():
            act = form.save(commit=False)
            est = Estudiante.objects.get(user=request.user)            
            act.estudiante = est
            act.save()

            horasHechas = determinarHoras(est)
            return render(request, 'main.html' , 
                          { 'dominio': True, 'horas': horasHechas, })

    else:
        form = ActividadForm() 

    # Arturo esto no deberia estar indentado al mismo nivel que la variable form de arriba?
    return render(request, 'registroActividad.html', {
                  'form': form,
                  })


# Funcion para obtener todos los estudiantes que no han completado el servicio
def obtenerEstudiantesFaltantes():

    est = Estudiante.objects.all()
    listaEst = []

    # Obtener para cada estudiante, sus horas hechas, y si es menor de 120,
    # guardar su informacion
    for e in est:
        horas = determinarHoras(e)
        actual = []
        if horas < 120:
            nombre = e.user.first_name
            apellido = e.user.last_name
            actual.append(nombre + " " + apellido)
            actual.append(e.carnet)
            actual.append(horas)
            actual.append(120 - horas)
            listaEst.append(actual)

    return listaEst


# Funcion para mostrar la vista de los estudiantes con sus horas hechas y
# las que les faltan.

def mostrarEstudiantes(request):

    estudiantes = obtenerEstudiantesFaltantes()

    return render(request, 'horasEstudiantes.html', { 'est': estudiantes, })

