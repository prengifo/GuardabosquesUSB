from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from models import ActividadForm, Actividad
from login.models import Estudiante, EstudianteForm
from django.db.models import Count, Min, Sum, Avg
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
    # palco
    else:
        d = False
        return render(request, 'main.html', {
                      'dominio': d,
                      'horas': horas,
                      })

def determinarHoras(est):

    horas = 0
    qs = Actividad.objects.filter(estudiante=est,validado=True)

    if qs:
        horas = qs.aggregate(Sum('horas')).get('horas__sum')
        print horas

    return horas


def actividades(request):

    est = Estudiante.objects.get(user=request.user)
    acts = Actividad.objects.filter(estudiante=est)

    return render(request, 'actividades.html', {
                  'acts': acts,
                  })

def registroActividad(request):
    if request.method == 'POST':
        form = ActividadForm(request.POST) # A form bound to the POST data
        if form.is_valid():
            horas = form.cleaned_data['horas']
            descripcion = form.cleaned_data['descripcion']
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
