from django.contrib import admin
from reports import models

# Register your models here.

@admin.register(models.clasificacion)
class admin_classify(admin.ModelAdmin):
    list_display = ('id', 'cuenta', 'centro_costo','nombre_tercero','responsable')
    search_fields = ('id', 'cuenta__pk', 'nit_tercero')
    
@admin.register(models.cuentas_contables)
class admin_cuentas(admin.ModelAdmin):
    list_display = ('cuenta', 'nombre_cuenta', 'nombre_cuenta_mayor','subcuenta','nombre_final')
    search_fields = ('cuenta', 'nombre_cuenta')

@admin.register(models.centro_costo)
class admin_cecos(admin.ModelAdmin):
    list_display = ('ceco', 'ciudad', 'cedo','tipo')
    search_fields = ('ceco', 'cedo')

@admin.register(models.rollling)
class admin_rolling(admin.ModelAdmin):
    list_display = ('clasificacion','anio', 'mes','valor')
    search_fields = ('clasificacion__pk','clasificacion__cuenta__pk')
    list_filter = ('anio', 'mes')
    readonly_fields = ['clasificacion','anio', 'mes']
    
    
@admin.register(models.areas_empresa)
class admin_areas(admin.ModelAdmin):
    list_display = ('nombre_area', 'usuario_responsable')
    search_fields = ('nombre_area', 'usuario_responsable')

@admin.register(models.gastos)
class admin_Gastos(admin.ModelAdmin):
    list_display = ('fecha', 'nombre_tercero','importe','clasificacion')
    search_fields = ('nombre_tercero', 'nit_tercero','clasificacion__pk')
    date_hierarchy = ('fecha')
    