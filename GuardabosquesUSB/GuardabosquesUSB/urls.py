from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView
from .views import ProfileUpdate, TipoActividadCreateView, TipoActividadListView, TipoActividadDeleteView
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^$', TemplateView.as_view(template_name='account/login.html')),
    url(r'^main/home', 'GuardabosquesUSB.views.completar_registro', name='registry'),
    url(r'^main/actualizar', ProfileUpdate.as_view(), name='update'),
    url(r'^main/validacion$', 'GuardabosquesUSB.views.validacion', name='validacion'),
    url(r'^main/validacion/(?P<id>\d+)/validar$', 'GuardabosquesUSB.views.guardarValidacion', name='validacionSave'),
    url(r'^main/validacion/(?P<id>\d+)/no_validar$', 'GuardabosquesUSB.views.guardarNoValidacion', name='validacionSave'),
    url(r'^main/mostrarEstudiantesRestantes$', 'GuardabosquesUSB.views.mostrarEstudiantes', name='mostrarEstudiantesRestantes'),
    url(r'^main/mostrarEstudiantesFinalizados$', 'GuardabosquesUSB.views.mostrarEstudiantesFinalizados', name='mostrarEstudiantesFinalizados'),
    url(r'^main/actividades$', 'GuardabosquesUSB.views.actividades', name='actividades'),
    url(r'^main/actividades/registroActividad', 'GuardabosquesUSB.views.registroActividad', name='registroActividad'),
    url(r'^main/actividades/registroTipoActividad', TipoActividadCreateView.as_view(), name='registroTipoActividad'),
    url(r'^main/actividades/lista', TipoActividadListView.as_view(), name='listaTipoActividad'),
    url(r'^main/borrarTipoActividad/(?P<pk>\d+)$',TipoActividadDeleteView.as_view(), name='borrarTipoActividad'),
    url(r'^main/calendario', 'GuardabosquesUSB.views.calendario', name='calendario'),
    url(r'^main/horas', 'GuardabosquesUSB.views.horasAcumuladas', name='horasAcumuladas'),
    url(r'^main/actividades/generarReporte', 'GuardabosquesUSB.views.generarReporte', name='generarReporte'),
    # Examples: url(r'^$', 'GuardabosquesUSB.views.home',
    # name='home'), url(r'^GuardabosquesUSB/',
    # include('GuardabosquesUSB.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)


# Uncomment the next line to serve media files in dev.
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
                            url(r'^__debug__/', include(debug_toolbar.urls)),
                            )
