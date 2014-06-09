from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
#from models import Persona
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
    if request.user.email.endswith('usb.ve'):
        d = True
        return render(request, 'main.html', {
        'dominio': d,
        })
    else:
        d = False
        return render(request, 'main.html', {
        'dominio': d,
    })