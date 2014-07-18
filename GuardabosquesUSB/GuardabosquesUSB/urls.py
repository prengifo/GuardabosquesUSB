from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^$', TemplateView.as_view(template_name='account/login.html')),
    url(r'^main/home', 'GuardabosquesUSB.views.completar_registro', name='registry'),
    url(r'^main/validacion$', 'GuardabosquesUSB.views.validacion', name='validacion'),
    url(r'^main/mostrarEstudiantes$', 'GuardabosquesUSB.views.mostrarEstudiantes', name='mostrarEstudiantes'),
    url(r'^main/actividades$', 'GuardabosquesUSB.views.actividades', name='actividades'),
    url(r'^main/actividades/registroActividad', 'GuardabosquesUSB.views.registroActividad', name='registroActividad'),
    # Examples:
    # url(r'^$', 'GuardabosquesUSB.views.home', name='home'),
    # url(r'^GuardabosquesUSB/', include('GuardabosquesUSB.foo.urls')),

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
