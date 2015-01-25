from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
import xhtml2pdf.pisa as pisa
from django.template.loader import get_template
from django.template import Context
import cStringIO as StringIO
from django.template import RequestContext
from models import ActividadForm, Actividad, ValidacionForm
from login.models import Estudiante, EstudianteForm
from django.db.models import Count, Min, Sum, Avg
from django.views.generic import UpdateView, CreateView, ListView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User
from .models import TipoActividad, TipoActividadForm
# from braces.views import

# Si se necesita algun cambio de los correos de administradores, se hace directamente aqui
admin_accounts = ['patrick.rengifo@gmail.com', 'danielar92@gmail.com',
                    'arturo.voltattorni@gmail.com', 'app.guardabosques@gmail.com']

# Funcion que determina si alguien es admin o no
def es_admin(mail):
    if (mail in admin_accounts):
        return True
    else:
        return False

CARRERA_CHOICES = (
    (0, 'Arquitectura'),
    (1, 'Ing. Computacion'),
    (2, 'Ing. Electrica'),
    (3, 'Ing. Electronica'),
    (4, 'Ing. Geofisica'),
    (5, 'Ing. Mantenimiento'),
    (6, 'Ing. Materiales'),
    (7, 'Ing. Mecanica'),
    (8, 'Ing. Produccion'),
    (9, 'Ing. Telecomunicaciones'),
    (10, 'Ing. Quimica'),
    (11, 'Lic. Biologia'),
    (12, 'Lic. Comercio Exterior'),
    (13, 'Lic. Gestion de la Hospitalidad'),
    (14, 'Lic. Fisica'),
    (15, 'Lic. Matematica'),
    (16, 'Lic. Quimica'),
    (17, 'Urbanismo'),
    (18, 'Admin. Aduanera'),
    (19, 'Admin. Hotelera'),
    (20, 'Admin. Transporte'),
    (21, 'Admin. Turismo'),
    (22, 'Comercio Exterior (Carrera Corta)'),
    (23, 'Mantenimiento Aeronautica'),
    (24, 'Organizacion Empresarial'),
    (25, 'Tec. Electrica'),
    (26, 'Tec. Electronica'),
    (27, 'Tec. Mecanica'),
)

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
                    d = True
                    a = es_admin(request.user.email)
                    return render(request, 'main.html', {
                                  'dominio': d,
                                  'admin': a,
                                  })
            else:
                form = EstudianteForm()
                return render(request, 'account/registro.html', {
                    'form': form,
                })
        # Caso contrario bienvenido sea
        else:
            a = es_admin(request.user.email)
            return render(request, 'main.html', {
                          'dominio': True,
                          'admin': a,
                          })

    # Caso de un admin o nosotros
    elif (es_admin(request.user.email)):
        return render(request, 'main.html', {
                      'dominio': True,
                      'admin' : True
                      })
    # palco
    else:
        print(request.user.email)
        return render(request, 'main.html', {
                      'dominio': False,
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
        admin = es_admin(self.request.user.email)
        return self.request.user.estudiante

# Funcion para determinar las horas que ha realizado un estudiante (validadas)
def determinarHoras(est):

    horas = 0
    qs = Actividad.objects.filter(estudiante=est,validado_nuevo=1)

    if qs:
        horas = qs.aggregate(Sum('horas')).get('horas__sum')
        print horas

    return horas

# Funcion para obtener las actividades realizadas por un estudiante
def actividades(request):

    est = Estudiante.objects.get(user=request.user)
    acts = Actividad.objects.filter(estudiante=est)
    horas = determinarHoras(est)
    completado = False
    if (horas >= 120):
        completado = True

    return render(request, 'actividades.html', {
                  'acts': acts,
                  'completado': completado,
                  })


# Funcion para obtener las actividades sin validar
def obtenerActividadesSinValidar():
    i = 1
    forms = []
    acts = Actividad.objects.filter(validado_nuevo=0)

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

    # Si eres admin puedes validar, sino fuck off
    if (es_admin(request.user.email)):
        cforms = obtenerActividadesSinValidar()
        return render(request, 'validacion.html' ,
                      { 'forms': cforms, })
    else:
        return HttpResponseRedirect(reverse('GuardabosquesUSB.views.completar_registro'))

def guardarValidacion(request, id):

    print(id)
    act = Actividad.objects.get(pk = id)
    act.validado_nuevo = 1
    # print(act.descripcion)
    form = ValidacionForm(request.POST, instance = act) # A form bound to the POST data
    if form.is_valid():
        form.save()
        print('SALVE')

    cforms = obtenerActividadesSinValidar()
    return render(request, 'validacion.html' ,
                  { 'forms': cforms, })


def guardarNoValidacion(request, id):

    print(id)
    act = Actividad.objects.get(pk = id)
    act.validado_nuevo = 2
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
            actual.append(CARRERA_CHOICES[e.carrera][1])
            listaEst.append(actual)

    return listaEst

# Funcion para obtener todos los estudiantes que han terminado
def obtenerEstudiantesFinalizados():

    est = Estudiante.objects.all()
    listaEst = []

    # Obtener para cada estudiante, sus horas hechas, y si es mayor o igual de 120,
    # guardar su informacion
    for e in est:
        horas = determinarHoras(e)
        actual = []
        if horas >= 120:
            nombre = e.user.first_name
            apellido = e.user.last_name
            actual.append(nombre + " " + apellido)
            actual.append(e.carnet)
            actual.append(horas)
            actual.append(CARRERA_CHOICES[e.carrera][1])
            listaEst.append(actual)

    return listaEst


# Funcion para mostrar la vista de los estudiantes con sus horas hechas y
# las que les faltan.

def mostrarEstudiantes(request):

    estudiantes = obtenerEstudiantesFaltantes()

    return render(request, 'horasEstudiantes.html', { 'est': estudiantes, })


# Funcion para mostrar la vista de los estudiantes que han competado el servicio
# y quieres revisar su informacion

def mostrarEstudiantesFinalizados(request):

    estudiantes = obtenerEstudiantesFinalizados()

    return render(request, 'horasEstudiantesFinalizados.html', { 'est': estudiantes, })


class TipoActividadCreateView(CreateView):
    model = TipoActividad
    form_class = TipoActividadForm
    success_url = '/main/actividades/registroTipoActividad'
    template_name = 'crearTipoActividad.html'

    def get_context_data(self, **kwargs):
        ctx = super(TipoActividadCreateView, self).get_context_data(**kwargs)
        ctx['actividades'] = TipoActividad.objects.all()
        return ctx


class TipoActividadListView(ListView):
    model = TipoActividad
    template_name = 'listaTipoActividad.html'
    context_object_name = 'objects'


class TipoActividadDeleteView(DeleteView):
    model = TipoActividad
    success_url = '/main/actividades/registroTipoActividad'

# Funcion para obtener las actividades realizadas y validadas por un estudiante
def actividadesValidadas(est):

    acts = Actividad.objects.filter(estudiante=est, validado_nuevo=1)
    listaAct = []

    # Obtener para cada estudiante, sus horas hechas, y si es mayor o igual de 120,
    # guardar su informacion
    for a in acts:
        actual = []
        actual.append(a.descripcion)
        actual.append(a.horas)
        actual.append(a.fecha)
        listaAct.append(actual)

    return listaAct

def calendario(request):
    a = es_admin(request.user.email)
    return render(request, 'calendario.html', {
        'admin' : a,
        })

def horasAcumuladas(request):
    est = Estudiante.objects.get(user=request.user)
    horas = determinarHoras(est)
    actividades = actividadesValidadas(est)
    return render(request, 'horasAcumuladas.html', {
                  'horas': horas,
                  'actividades': actividades,
                  })

def generarReporte(request):
    est = Estudiante.objects.get(user=request.user)
    acts = Actividad.objects.filter(estudiante=est)
    horas = determinarHoras(est)
    completado = False
    if (horas >= 120):
        completado = True

    return generar_pdf('reportePdf.html', {
        'pagesize':'letter',
        'acts': acts,
        'completado': completado,
        })



def generar_pdf(template_src, context_dict):
    template = get_template(template_src)
    context = Context(context_dict)
    html  = template.render(context)
    result = StringIO.StringIO()

    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("utf-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), mimetype='application/pdf')
    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))
