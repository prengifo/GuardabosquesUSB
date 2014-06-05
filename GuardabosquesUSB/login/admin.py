from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from models import Estudiante

# Define an inline admin descriptor for Estudiante model
# which acts a bit like a singleton
class EstudianteInline(admin.StackedInline):
    model = Estudiante
    can_delete = False
    verbose_name_plural = 'estudiantes'

# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (EstudianteInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)