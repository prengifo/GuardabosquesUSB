from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
#from models import Persona
from models import ActividadForm
from login.models import Estudiante
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
        
def inicio(request):
    #pdb.set_trace()
    #if request.user.email.endswith('usb.ve'):
    if True:
        d = True
        return render(request, 'main.html', {
        'dominio': d,
        })
    else:
        d = False
        return render(request, 'main.html', {
        'dominio': d,
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
            return render(request, 'main.html' , { 'dominio': True, })
    else:
        form = ActividadForm() 

    return render(request, 'registroActividad.html', {
        'form': form,
    })
