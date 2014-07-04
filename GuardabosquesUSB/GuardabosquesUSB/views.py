from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
#from models import Persona
from models import ActividadForm, Actividad
from login.models import Estudiante
from django.db.models import Count, Min, Sum, Avg
from django.contrib.auth.models import User
import pdb;

#def completar_registro(request,correo):

    #default = 0
    #usr = User.objects.get(email=correo)
    
    #if usr.carnet == default:
        #render(request,'templates/registro.html')
    #else:
        #render(request,'templates/main.html')


#def insertar(request,correo,crt,crr):
    
    #default = 0
    #usr = User.objects.get(email=correo)
    #usr.carnet = crt
    #usr.carrera = crr
    #usr.save()

def determinarHoras(est):

    horas = 0
    qs = Actividad.objects.filter(estudiante=est,validado=True)

    if qs:
        horas = qs.aggregate(Sum('horas')).get('horas__sum')
        print horas

    return horas

def inicio(request):

    est = Estudiante.objects.get(user=request.user)
    horas = determinarHoras(est)

    #pdb.set_trace()
    #if request.user.email.endswith('usb.ve'):
    if True:
        d = True
        return render(request, 'main.html', {
        'dominio': d,
        'horas': horas,
        })
    else:
        d = False
        return render(request, 'main.html', {
        'dominio': d,
        'horas': horas,
    })

def actividades(request):
    return render(request, 'actividades.html')

def registroActividad(request):
    if request.method == 'POST':
        form = ActividadForm(request.POST) # A form bound to the POST data
        if form.is_valid():
            horas = form.cleaned_data['horas']
            descripcion = form.cleaned_data['descripcion']
            act = form.save(commit=False)
            act.estudiante = Estudiante.objects.get(user=request.user)
            act.save()

            est = Estudiante.objects.get(user=request.user)
            horas = determinarHoras(est)
            return render(request, 'main.html' , { 'dominio': True, 'horas': horas, })

    else:
        form = ActividadForm() 

    return render(request, 'registroActividad.html', {
        'form': form,
    })
