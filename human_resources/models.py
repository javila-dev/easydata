import datetime
from django.db import models
from django.db.models import Sum, Count
from django.contrib.auth.models import User
from django.utils import timezone
from Atlantic.utils import JsonRender
from useraccounts.models import Perfil

BONIFICACION_TYPE_CHOICES = (
    ('BONIFICACION POR RENDIMIENTO DE PLANTA', 'BONIFICACION POR RENDIMIENTO DE PLANTA'),
    ('COMISION', 'COMISION'),
    ('COMISION COMERCIALES', 'COMISION COMERCIALES'),
    ('AUXILIO POR PORCIONADOR', 'AUXILIO POR PORCIONADOR'),
    ('AUXILIO POR MONTACARGAS', 'AUXILIO POR MONTACARGAS'),
    ('AUXILIO POR CONECTIVIDAD', 'AUXILIO POR CONECTIVIDAD'),
    ('AUXILIO POR INVENTARIOS', 'AUXILIO POR INVENTARIOS'),
    ('AUXILIO DE DISPONIBILIDAD', 'AUXILIO DE DISPONIBILIDAD'),
    ('AUXILIO DE ESCOLARIDAD', 'AUXILIO DE ESCOLARIDAD'),
    ('AUXILIO DE VIVIENDA', 'AUXILIO DE VIVIENDA'),
    ('BONO DE MOVILIZACION MENSUAL ADICIONAL CELTA', 'BONO DE MOVILIZACION MENSUAL ADICIONAL CELTA'),
    ('INDICADORES', 'INDICADORES'),
    ('EBITDA', 'EBITDA'),
    ('CXS', 'CXS'),
    ('COMPENSACION VARIABLE', 'COMPENSACION VARIABLE'),
    ('CARGO X ENCARGO', 'CARGO X ENCARGO'),
    ('ENCARGO', 'ENCARGO'),
    ('ENCARGO X 3 MESES', 'ENCARGO X 3 MESES'),
    ('ENCARGO X 6 MESES', 'ENCARGO X 6 MESES'),
    ('GARANTIZADO X 3 MESES', 'GARANTIZADO X 3 MESES'),
    ('GARANTIZADO LOS 6 PRIMERO MESES', 'GARANTIZADO LOS 6 PRIMERO MESES'),
    ('GARANTIZADO LOS 2 PRIMEROS MESES', 'GARANTIZADO LOS 2 PRIMEROS MESES'),
    ('GARANTIZADO HASTA DEFINIR INDICADORES', 'GARANTIZADO HASTA DEFINIR INDICADORES'),
    ('GARANTIZADO SUSPENDIDO POR INC', 'GARANTIZADO SUSPENDIDO POR INC'),
)

# Create your models here.
class dependencia(models.Model):
    descripcion = models.CharField(max_length=255, unique=True)
    
    def __str__(self):
        return self.descripcion.upper()
    
    def getbudgets(self,datecontrol):
        bgt= base_teorica.objects.filter(
            cargo__area__gerencia = self.pk,
            vigente_desde__gte = datecontrol,
            vigente_hasta__lte = datecontrol,
        )
        
        counter = 0
        
        if bgt.exists():
            counter = bgt.aggregate(total=Sum('cantidad')).get('total')
            counter = 0 if counter is None else counter
            
        return counter
    
    def budgetdifference(self, datecontrol):
        control = self.getbudgets(datecontrol)
        today = datetime.date.today()
        datecontrol = datetime.datetime.strptime(datecontrol,"%Y-%m-%d").date()
        if datecontrol < today:
            real = base_personal.objects.filter(cargo__area__gerencia = self.pk,
                                            activo=True).count()
        else:
            real = base_personal.objects.filter(cargo__area__gerencia = self.pk,
                                                fecha_ingreso__lte=datecontrol,
                                            fecha_retiro__gte=datecontrol).count()
        
        return real-control
    
class estructura(models.Model):
    descripcion = models.CharField(max_length= 255, unique=True)
    dependecia = models.ForeignKey(dependencia, on_delete=models.PROTECT)
    
    def __str__(self):
        return self.descripcion.upper()
    
    def getbudgets(self,datecontrol):
        bgt= base_teorica.objects.filter(
            cargo__area = self.pk,
            vigente_desde__lte = datecontrol,
            vigente_hasta__gte = datecontrol,
        )
        
        counter = 0
        
        if bgt.exists():
            counter = bgt.aggregate(total=Sum('cantidad')).get('total')
            counter = 0 if counter is None else counter
            
        return counter
    
    def budgetdifference(self, datecontrol):
        control = self.getbudgets(datecontrol)
        today = datetime.date.today()
        datecontrol = datetime.datetime.strptime(datecontrol,"%Y-%m-%d").date()
        if datecontrol >= today:
            real = base_personal.objects.filter(cargo__area = self.pk,
                                            activo=True).count()
        else:
            real = base_personal.objects.filter(cargo__area = self.pk,
                                                fecha_ingreso__lte=datecontrol,
                                                fecha_retiro__gte=datecontrol).count()
        
        return real-control
    
    def total_salarios(self, datecontrol):
        today = datetime.date.today()
        datecontrol = datetime.datetime.strptime(datecontrol,"%Y-%m-%d").date()
        if datecontrol >= today:
            workers = base_personal.objects.filter(cargo__area = self.pk,
                                            activo=True)
        else:
            workers = base_personal.objects.filter(cargo__area = self.pk,
                                                fecha_ingreso__lte=datecontrol,
                                                fecha_retiro__gte=datecontrol)
    
        total_salary = workers.aggregate(total=Sum('salario_base')).get('total')
        
        total_salary = 0 if total_salary is None else total_salary
        
        return total_salary
        
class area(models.Model):
    descripcion = models.CharField(max_length= 255)
    estructura = models.ForeignKey(estructura, on_delete=models.PROTECT) 
    responsable= models.ForeignKey('base_personal', on_delete=models.PROTECT,
                                   null=True, blank=True)
    
    class Meta:
        unique_together =['descripcion','estructura']
    
    def __str__(self):
        return self.descripcion.upper()
    
    def cantidad_actual(self):
        cantidad = contratos_personal.objects.filter(cargo__area = self.pk,
                                            activo=True).count()
        
        return cantidad
    
class canal(models.Model):
    """ Esto en realidad es la orden """
    descripcion = models.CharField(max_length= 255, unique=True)

    def __str__(self):
        return self.descripcion

class cceco(models.Model):
    descripcion = models.CharField(max_length= 255)
    codigo_sap = models.CharField(max_length= 255, null=True, blank=True)
    
    def __str__(self):
        return f'{self.descripcion} - {self.codigo_sap}'

class cargo(models.Model):
    TIPO_POSICION_CHOICES = (
        ('HC', 'HC'),
        ('HC PLUS', 'HC PLUS'),
        ('ESTRATEGIA ROTACION', 'ESTRATEGIA ROTACION'),
        ('APRENDIZ', 'APRENDIZ'),
        ('NO PLUS', 'NO PLUS'),
        ('PTE RECUPERAR', 'PTE RECUPERAR'),
        ('MATERNIDAD', 'MATERNIDAD'),
    )
    TAP_CHOICES = (
        ('BAJO', 'BAJO'),
        ('MEDIO', 'MEDIO'),
        ('ALTO', 'ALTO'),
    )

    descripcion = models.CharField(max_length= 255)
    area = models.ForeignKey(area, on_delete=models.PROTECT)
    activo = models.BooleanField(default=True)
    cantidad_aprobada = models.IntegerField()
    criticidad = models.CharField(max_length=255, choices=(
        ('BAJA','BAJA'),
        ('MEDIA','MEDIA'),
        ('ALTA','ALTA'),
    ), default='MEDIA')
    tipo_posicion = models.CharField(max_length=50, choices=TIPO_POSICION_CHOICES, default='HC')
    tap = models.CharField(max_length=10, choices=TAP_CHOICES, null=True, blank=True)
    
    class Meta:
        unique_together = ['descripcion','area']
        
    def __str__(self):
        return self.descripcion.upper()
    
    def cantidad_actual(self):
        cantidad = contratos_personal.objects.filter(
            cargo = self.pk,
            activo = True
        ).count()
        
        return cantidad
    
    def diferencia(self):
        
        return self.cantidad_aprobada - self.cantidad_actual()
    
class sede(models.Model):
    codigo_sap = models.IntegerField(null=True, blank=True)
    descripcion = models.CharField(max_length= 255)
    codigo_map = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f'{self.descripcion.upper()}'

class tipos_auxilio(models.Model):
    descripcion = models.CharField(max_length= 255, unique=True)
    
    def __str__(self):
        return self.descripcion
  
class base_personal(models.Model):
    numero_identificacion = models.IntegerField(unique=True) 
    tipo_id = models.CharField(max_length=255, choices=(
        ('CC','CC'),
        ('CE','CE'),
        ('TI','TI'),
        ('PPT','PPT'),
        ('PEP','PEP'),
        ('PA','PA'),
    ))
    primer_nombre = models.CharField(max_length=255)
    segundo_nombre = models.CharField(max_length=255, null=True, blank=True)
    primer_apellido = models.CharField(max_length=255)
    segundo_apellido = models.CharField(max_length=255, null=True, blank=True)
    eps = models.ForeignKey('eps',on_delete=models.PROTECT,
                            null=True, blank=True)
    pension = models.ForeignKey('fondo_pensiones', on_delete=models.PROTECT,
                                null=True, blank=True)
    cesantias = models.ForeignKey('fondo_cesantias', on_delete=models.PROTECT,
                                null=True, blank=True)
    arl = models.ForeignKey('arl', on_delete=models.PROTECT)
    tipo_riesgo = models.CharField(max_length=255, choices=(
        ('0','0'),
        ('0.522','0.522'),
        ('1.044','1.044'),
        ('4.35','4.35'),
        ('NO APLICA','NO APLICA'),
        ('OTRO','OTRO'),
    ))
    ccf = models.ForeignKey('ccf', on_delete=models.PROTECT)
    email = models.EmailField(null=True, blank=True)
    direccion_residencia = models.CharField(max_length=255, null=True, blank=True)
    ciudad = models.ForeignKey('ciudad', on_delete=models.PROTECT)
    departamento = models.ForeignKey('departamento', on_delete=models.PROTECT)
    contacto = models.CharField(max_length=255, null=True, blank=True) 
    contacto_otro = models.CharField(max_length=255, null=True, blank=True)
    tipo_vivienda = models.CharField(max_length=255, choices=(
        ('Propia','Propia'),
        ('Familiar','Familiar'),
        ('Arrendada','Arrendada'),
    ), null=True, blank=True)
    nivel_educativo = models.CharField(max_length=255, choices=(
        ('BASICA PRIMARIA','BASICA PRIMARIA'),
        ('SECUNDARIA','SECUNDARIA'),
        ('BACHILLER','BACHILLER'),
        ('TECNICO','TECNICO'),
        ('TECNOLOGO','TECNOLOGO'),
        ('UNIVERSITARIO/PROFESIONAL','UNIVERSITARIO/PROFESIONAL'),
        ('INGENIERO','INGENIERO'),
        ('ESPECIALISTA','ESPECIALISTA'),
        ('MAGISTER','MAGISTER'),
        ('DOCTORADO','DOCTORADO'),
    ),null=True,blank=True)
    titulo = models.CharField(max_length=255, null=True, blank=True)
    sexo = models.CharField(max_length=255, choices=(
        ('M','Masculino'),
        ('F','Femenino'),
        ('O','Otro'),
    ))
    rh = models.CharField(max_length=255, choices=(
        ('A-','A-'),
        ('A+','A+'),
        ('AB-','AB-'),
        ('AB+','AB+'),
        ('B-','B-'),
        ('B+','B+'),
        ('O-','O-'),
        ('O+','O+'),
        ('ND','NO DEFINIDO'),
    ), null=True, blank = True)
    estado_civil = models.CharField(max_length=255, choices=(
        ('SOLTERO (A)','SOLTERO (A)'),
        ('CASADO (A)','CASADO (A)'),
        ('VIUDO (A)','VIUDO (A)'),
        ('DIVORCIADO (A)','DIVORCIADO (A)'),
        ('UNION LIBRE','UNION LIBRE'),
    ), null=True, blank= True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    talla_camisa = models.CharField(max_length=255, null=True, blank=True)
    talla_pantalon = models.CharField(max_length=255, null=True, blank=True)
    talla_calzado = models.CharField(max_length=255, null=True, blank=True)
    codigo_sap = models.CharField(null=True, blank=True, max_length=255)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    
    def get_full_name(self):
        nc= self.primer_nombre
        if self.segundo_nombre:
            nc += ' ' + self.segundo_nombre
        nc += ' ' + self.primer_apellido
        if self.segundo_apellido:
            nc += ' ' + self.segundo_apellido
        
        return nc.upper()
    
    def contrato_activo(self,type='json'):
        _contrato = contratos_personal.objects.filter(trabajador=self.pk)
        if self.activo:
            _contrato = _contrato.filter(activo=True)
        
        data = []
        if _contrato.exists():
            if type=='json':
                data = JsonRender(_contrato, query_functions=['auxilios_contrato',]).render()[-1]
            else:
                data = _contrato.last()
        
        return data
    
    def historico_contratos(self):
        _contrato = contratos_personal.objects.filter(trabajador=self.pk).order_by('-activo_hasta')
        if _contrato.exists():
            return JsonRender(_contrato, query_functions=['auxilios_contrato',]).render()
        
        return []
    
    def historico_acciones(self):
        h = historial.objects.filter(texto__icontains=self.numero_identificacion).order_by('-fecha')
        if h.exists():
            return JsonRender(h, query_functions=['profile_user','since']).render()
        return []
        
    def __str__(self):
        return self.get_full_name()
    
class contratos_personal(models.Model):
    trabajador = models.ForeignKey(base_personal, on_delete=models.CASCADE,
                                   related_name = 'trabajador')
    fecha_inicio = models.DateField()
    fecha_periodo_prueba = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)
    tipo_ingreso = models.CharField(choices=(
        ('A','Aprendizaje'),
        ('T','Temporal'),
        ('V','Vinculado'),
    ), max_length=255)
    modalidad_ingreso = models.CharField(choices=(
        ('NUEVO INGRESO POR TEMPORAL','NUEVO INGRESO POR TEMPORAL'),
        ('REINGRESO','REINGRESO'),
        ('NUEVO INGRESO DIRECTO','NUEVO INGRESO DIRECTO'),
        ('NUEVO INGRESO DIRECTO (TEMPORAL A DIRECTO)','NUEVO INGRESO DIRECTO (TEMPORAL A DIRECTO)'),
    ), max_length=255)
    tipo_contrato = models.CharField(choices=[
        ('Indefinido','Indefinido'),
        ('Obra o Labor','Obra o Labor'),
        ('Aprendizaje','Aprendizaje'),
    ], max_length=255)
    tipo_posicion = models.CharField(choices=[
        ('HC','HC'),
        ('HC PLUS','HC PLUS'),
        ('ESTRATEGIA ROTACION','ESTRATEGIA ROTACION'),
        ('APRENDIZ','APRENDIZ'),
        ('NO PLUS','NO PLUS'),
        ('PTE RECUPERAR','PTE RECUPERAR'),
        ('MATERNIDAD','MATERNIDAD'),
    ], max_length=255, null=True, blank=True)
    empleador = models.ForeignKey('empleadores',on_delete=models.PROTECT)
    temporal = models.ForeignKey('temporales',on_delete=models.PROTECT, null=True, blank=True)
    cargo = models.ForeignKey(cargo, on_delete=models.PROTECT)
    area = models.ForeignKey(area, on_delete=models.PROTECT)
    canal = models.ForeignKey(canal, on_delete = models.PROTECT, null=True, blank=True)
    cceco = models.ForeignKey(cceco, on_delete=models.PROTECT, null=True, blank=True)
    sede = models.ForeignKey(sede, on_delete=models.PROTECT)
    ciudad_laboral = models.ForeignKey('ciudad', on_delete=models.PROTECT, null=True, blank=True, related_name='contratos_ciudad_laboral')
    jefe_inmediato = models.ForeignKey(base_personal, on_delete=models.PROTECT,
                                       null=True, blank= True,
                                       related_name='jefe_inmediato')
    salario_base = models.FloatField()
    auxilio_transporte = models.FloatField(null=True, blank=True)
    base_bonificacion = models.FloatField(null=True, blank=True)
    bonificacion = models.CharField(choices=BONIFICACION_TYPE_CHOICES, max_length=255, null=True, blank=True)
    fecha_retiro = models.DateField(null=True,blank=True)
    motivo_retiro = models.ForeignKey('motivos_retiro', on_delete=models.PROTECT, null=True, blank=True)
    motivo_retiro_real = models.CharField(max_length=255, null=True, blank=True)
    activo_desde = models.DateField(null=True, blank=True)
    activo_hasta = models.DateField(null=True, blank=True)
    activo = models.BooleanField(default=True)
    
    def auxilios_contrato(self):
        _auxilios = auxilios_contrato.objects.filter(contrato=self.pk)
        if _auxilios.exists():            
            return JsonRender(_auxilios).render()
        
        return []
    
    def rango_salario(self):
        if self.salario_base > 5e6: gs = 'Grupo 5'
        elif self.salario_base > 4e6: gs = 'Grupo 4'
        elif self.salario_base > 3e6: gs = 'Grupo 3'
        elif self.salario_base > 2e6: gs = 'Grupo 2'
        else: gs = 'Grupo 1'
        
        return gs
      
class auxilios_contrato(models.Model):
    contrato = models.ForeignKey(contratos_personal, on_delete=models.CASCADE)
    tipo = models.ForeignKey(tipos_auxilio, on_delete=models.CASCADE)
    valor = models.FloatField()
    
class cambios_salario(models.Model):
    trabajador = models.ForeignKey(base_personal, on_delete=models.PROTECT)
    contrato = models.ForeignKey(contratos_personal, on_delete=models.PROTECT)
    fecha = models.DateField()
    salario_anterior = models.FloatField()
    nuevo_salario = models.FloatField()
    motivo = models.CharField(max_length=255)

class empalmes(models.Model):
    quien_ingresa = models.ForeignKey(base_personal, on_delete=models.PROTECT, related_name='quien_ingresa')
    quien_sale = models.ForeignKey(base_personal, on_delete=models.PROTECT, related_name='quien_sale')
    contrato_sale = models.ForeignKey(contratos_personal, on_delete=models.PROTECT)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    motivo = models.CharField(choices=[
        ('Licencia maternidad','Licencia maternidad'),
        ('Licencia medica','Licencia medica'),
        ('Reemplazo','Reemplazo'),
        ('NA','No aplica'),
    ],max_length=255)
    
    def dias(self):
        return (self.fecha_fin - self.fecha_inicio).days
    
    def dias_reales(self):
        fin_real = self.contrato_sale.fecha_retiro
        if fin_real != None:
            return (fin_real - self.fecha_fin).days
        return ""

class historico_base_teorica(models.Model):
    cargo = models.ForeignKey(cargo, on_delete=models.PROTECT)
    cantidad = models.IntegerField() 
    vigente_desde = models.DateField(null=True, blank=True)
    vigente_hasta = models.DateField(null=True, blank=True)
    usuario_crea = models.ForeignKey(User, on_delete=models.PROTECT)
    
class motivos_retiro(models.Model):
    descripcion = models.CharField(max_length=255, unique=True)
    
    def __str__(self):
        return self.descripcion.upper()
    
class historial(models.Model):
    usuario = models.ForeignKey(User, on_delete = models.PROTECT)
    texto = models.CharField(max_length=255)
    fecha = models.DateTimeField(auto_now_add=True)
    
    def profile_user(self):
        
        perfil = Perfil.objects.get(usuario=self.usuario)
        data = {
            'nombre_completo': self.usuario.get_full_name().upper(),
            'avatar': perfil.avatar.__str__()
        }
        return data

    def since(self):
        days_beetwen = (timezone.now() - self.fecha).days
        fecha_fmt = datetime.datetime.strftime(self.fecha,'%d de %B de %Y a las %H:%M:%S')
        txt = f'Hace {days_beetwen} días - el {fecha_fmt}'
        
        return txt
    
    def __str__(self):
        msj = self.usuario.username + ' el ' + self.fecha.strftime('%Y-%m-%d') \
            + ' a las ' + self.fecha.strftime('%H:%M:%S') + ' ' + self.texto.capitalize()
        return msj
    
class eps(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    
    def __str__(self) -> str:
        return self.nombre.capitalize()

class fondo_pensiones(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    
    def __str__(self) -> str:
        return self.nombre.capitalize()
    
class fondo_cesantias(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    
    def __str__(self) -> str:
        return self.nombre.capitalize()

class arl(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    
    def __str__(self) -> str:
        return self.nombre.capitalize()
    
class ccf(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    
    def __str__(self) -> str:
        return self.nombre.capitalize()

class empleadores(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    
    def __str__(self) -> str:
        return self.nombre.upper()
    
class temporales(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    activa = models.BooleanField(default=True)
    
    def __str__(self) -> str:
        return self.nombre.upper()
        
class descargos(models.Model):
    trabajador = models.ForeignKey(base_personal, on_delete=models.PROTECT)
    fecha = models.DateField()
    
    def __str__(self):
        return f'{self.trabajador} - {self.fecha}'

class departamento(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    def __str__(self) -> str:
        return self.nombre.capitalize()

class ciudad(models.Model):
    departamento = models.ForeignKey(departamento, on_delete=models.PROTECT)
    nombre = models.CharField(max_length=255)
    
    def __str__(self) -> str:
        return self.nombre.capitalize()


class importacion_personal_job(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'PENDING'),
        ('MAPPING', 'MAPPING'),
        ('RUNNING', 'RUNNING'),
        ('COMPLETED', 'COMPLETED'),
        ('FAILED', 'FAILED'),
    )

    usuario = models.ForeignKey(User, on_delete=models.PROTECT)
    nombre_archivo = models.CharField(max_length=255)
    ruta_archivo = models.CharField(max_length=500)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    total_filas = models.IntegerField(default=0)
    filas_importables = models.IntegerField(default=0)
    filas_procesadas = models.IntegerField(default=0)
    creados = models.IntegerField(default=0)
    actualizados = models.IntegerField(default=0)
    omitidos = models.IntegerField(default=0)
    conflictos = models.IntegerField(default=0)
    errores = models.IntegerField(default=0)
    no_importables = models.IntegerField(default=0)
    ignoradas = models.IntegerField(default=0)
    detalles_conflicto = models.JSONField(default=list, blank=True)
    detalles_error = models.JSONField(default=list, blank=True)
    detalles_no_importables = models.JSONField(default=list, blank=True)
    mensaje_error = models.TextField(null=True, blank=True)
    fecha_inicio = models.DateTimeField(null=True, blank=True)
    fecha_fin = models.DateTimeField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
