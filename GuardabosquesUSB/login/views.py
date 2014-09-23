from django.shortcuts import render, render_to_response
from django.forms.models import modelformset_factory
from django.template import RequestContext

from login.models import Estudiante

# Create your views here.

def login(request):
    return render (request, 'login.html')


# def add_(request):
#     InvitadoFormSet = modelformset_factory(Invitado)
#     if request.method == 'POST':
#         formset = InvitadoFormSet(request.POST, request.FILES)
#         if formset.is_valid():
#             formset.save()
#             return consultar_invitados(request)
#     else:
#         formset = InvitadoFormSet(queryset=Invitado.objects.none())

#     return render(request, "agregar/agregarInvitado.html", {
#         "formset": formset,
#     })
