from django.contrib import admin
from .models import (
    dependencia, estructura, area, canal, cceco, cargo, sede, tipos_auxilio,
    base_personal, contratos_personal, auxilios_contrato, cambios_salario,
    empalmes, historico_base_teorica, motivos_retiro, historial,
    eps, fondo_pensiones, fondo_cesantias, arl, ccf, empleadores, temporales,
    descargos, departamento, ciudad, importacion_personal_job,
)


# ── Inlines ────────────────────────────────────────────────────────────────

class auxilios_contrato_inline(admin.TabularInline):
    model = auxilios_contrato
    extra = 0


class contratos_personal_inline(admin.TabularInline):
    model = contratos_personal
    fk_name = 'trabajador'
    extra = 0
    show_change_link = True
    fields = ('fecha_inicio', 'fecha_retiro', 'cargo', 'area', 'salario_base', 'activo')
    readonly_fields = ('fecha_inicio',)


# ── Estructura organizacional ───────────────────────────────────────────────

@admin.register(dependencia)
class dependenciaAdmin(admin.ModelAdmin):
    list_display = ('descripcion',)
    search_fields = ('descripcion',)


@admin.register(estructura)
class estructuraAdmin(admin.ModelAdmin):
    list_display = ('descripcion', 'dependecia')
    list_filter = ('dependecia',)
    search_fields = ('descripcion',)


@admin.register(area)
class areaAdmin(admin.ModelAdmin):
    list_display = ('descripcion', 'estructura', 'responsable')
    list_filter = ('estructura', 'estructura__dependecia')
    search_fields = ('descripcion',)
    autocomplete_fields = ('responsable',)


@admin.register(cargo)
class cargoAdmin(admin.ModelAdmin):
    list_display = ('descripcion', 'area', 'activo', 'cantidad_aprobada', 'criticidad', 'tipo_posicion')
    list_filter = ('activo', 'criticidad', 'tipo_posicion', 'area__estructura__dependecia')
    search_fields = ('descripcion', 'area__descripcion')
    list_editable = ('activo',)


# ── Catálogos simples ───────────────────────────────────────────────────────

@admin.register(canal)
class canalAdmin(admin.ModelAdmin):
    search_fields = ('descripcion',)


@admin.register(cceco)
class ccecoAdmin(admin.ModelAdmin):
    list_display = ('descripcion', 'codigo_sap')
    search_fields = ('descripcion', 'codigo_sap')


@admin.register(sede)
class sedeAdmin(admin.ModelAdmin):
    list_display = ('descripcion', 'codigo_sap', 'codigo_map')
    search_fields = ('descripcion',)


@admin.register(tipos_auxilio)
class tipos_auxilioAdmin(admin.ModelAdmin):
    search_fields = ('descripcion',)


@admin.register(motivos_retiro)
class motivos_retiroAdmin(admin.ModelAdmin):
    search_fields = ('descripcion',)


@admin.register(eps)
class epsAdmin(admin.ModelAdmin):
    search_fields = ('nombre',)


@admin.register(fondo_pensiones)
class fondo_pensionesAdmin(admin.ModelAdmin):
    search_fields = ('nombre',)


@admin.register(fondo_cesantias)
class fondo_cesantiasAdmin(admin.ModelAdmin):
    search_fields = ('nombre',)


@admin.register(arl)
class arlAdmin(admin.ModelAdmin):
    search_fields = ('nombre',)


@admin.register(ccf)
class ccfAdmin(admin.ModelAdmin):
    search_fields = ('nombre',)


@admin.register(empleadores)
class empleadoresAdmin(admin.ModelAdmin):
    search_fields = ('nombre',)


@admin.register(temporales)
class temporalesAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activa')
    list_filter = ('activa',)
    search_fields = ('nombre',)


@admin.register(departamento)
class departamentoAdmin(admin.ModelAdmin):
    search_fields = ('nombre',)


@admin.register(ciudad)
class ciudadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'departamento')
    list_filter = ('departamento',)
    search_fields = ('nombre',)


# ── Personal ────────────────────────────────────────────────────────────────

@admin.register(base_personal)
class base_personalAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'numero_identificacion', 'tipo_id', 'sexo', 'activo', 'eps', 'arl')
    list_filter = ('activo', 'sexo', 'arl', 'eps', 'ccf')
    search_fields = ('primer_nombre', 'segundo_nombre', 'primer_apellido',
                     'segundo_apellido', 'numero_identificacion', 'email')
    readonly_fields = ('fecha_registro',)
    inlines = (contratos_personal_inline,)


@admin.register(contratos_personal)
class contratos_personalAdmin(admin.ModelAdmin):
    list_display = ('trabajador', 'cargo', 'area', 'fecha_inicio', 'fecha_retiro',
                    'salario_base', 'tipo_ingreso', 'activo')
    list_filter = ('activo', 'tipo_ingreso', 'tipo_contrato', 'area__estructura__dependecia')
    search_fields = ('trabajador__primer_nombre', 'trabajador__primer_apellido',
                     'trabajador__numero_identificacion', 'cargo__descripcion')
    date_hierarchy = 'fecha_inicio'
    inlines = (auxilios_contrato_inline,)


@admin.register(auxilios_contrato)
class auxilios_contratoAdmin(admin.ModelAdmin):
    list_display = ('contrato', 'tipo', 'valor')
    list_filter = ('tipo',)
    search_fields = ('contrato__trabajador__primer_apellido',)


@admin.register(cambios_salario)
class cambios_salarioAdmin(admin.ModelAdmin):
    list_display = ('trabajador', 'fecha', 'salario_anterior', 'nuevo_salario', 'motivo')
    list_filter = ('fecha',)
    search_fields = ('trabajador__primer_nombre', 'trabajador__primer_apellido')
    date_hierarchy = 'fecha'


@admin.register(empalmes)
class empalmesAdmin(admin.ModelAdmin):
    list_display = ('quien_ingresa', 'quien_sale', 'fecha_inicio', 'fecha_fin', 'motivo')
    list_filter = ('motivo',)
    search_fields = ('quien_ingresa__primer_apellido', 'quien_sale__primer_apellido')


@admin.register(historico_base_teorica)
class historico_base_teoricaAdmin(admin.ModelAdmin):
    list_display = ('cargo', 'cantidad', 'vigente_desde', 'vigente_hasta', 'usuario_crea')
    list_filter = ('cargo__area__estructura__dependecia',)
    search_fields = ('cargo__descripcion',)


@admin.register(historial)
class historialAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'texto', 'fecha')
    list_filter = ('usuario',)
    search_fields = ('texto', 'usuario__username')
    date_hierarchy = 'fecha'


@admin.register(descargos)
class descargosAdmin(admin.ModelAdmin):
    list_display = ('trabajador', 'fecha')
    search_fields = ('trabajador__primer_nombre', 'trabajador__primer_apellido')
    date_hierarchy = 'fecha'


@admin.register(importacion_personal_job)
class importacion_personal_jobAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'nombre_archivo', 'status', 'filas_procesadas',
                    'creados', 'actualizados', 'errores', 'fecha_creacion')
    list_filter = ('status',)
    search_fields = ('nombre_archivo', 'usuario__username')
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion', 'fecha_inicio', 'fecha_fin',
                       'total_filas', 'filas_importables', 'filas_procesadas',
                       'creados', 'actualizados', 'omitidos', 'conflictos',
                       'errores', 'no_importables', 'ignoradas',
                       'detalles_conflicto', 'detalles_error', 'detalles_no_importables',
                       'mensaje_error')
