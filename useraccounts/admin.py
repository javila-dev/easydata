from django.contrib import admin
from useraccounts import models

# Register your models here.

@admin.register(models.Perfil)
class admin_perfil(admin.ModelAdmin):
    list_display = ('usuario',)
    search_fields = ('usuario',)
    filter_horizontal = ['rol','permiso']
    
@admin.register(models.Rol)
class admin_rol(admin.ModelAdmin):
    list_display = ('descripcion',)
    search_fields = ('descripcion',)
    #filter_horizontal = ['permisos',]
    
@admin.register(models.Permiso)
class admin_permiso(admin.ModelAdmin):
    list_display = ('descripcion',)