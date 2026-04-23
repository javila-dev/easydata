from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
# Create your models here.

class cuentas_contables(models.Model):
    cuenta = models.BigIntegerField(primary_key=True)
    nombre_cuenta = models.CharField(max_length=255)
    nombre_cuenta_mayor = models.CharField(max_length=255)
    subcuenta = models.CharField(max_length=255)
    nombre_final = models.CharField(max_length=255)
    p_y_g = models.CharField(max_length=50, null=True)
    
    class Meta:
        verbose_name = 'Cuenta Contable'
        verbose_name_plural = 'Cuentas Contables'
    
    def __str__(self):
        return f'{self.cuenta} - {self.nombre_cuenta.upper()}'
    
class centro_costo(models.Model):
    ceco = models.IntegerField(primary_key=True)
    ciudad = models.CharField(max_length=255)
    cedo = models.CharField(max_length=255,null=True,blank=True)
    tipo = models.CharField(max_length=255, choices = [
        ('Ce.Costo','Ce.Costo'),
        ('Orden','Orden')
    ])
    
    class Meta:
        verbose_name = 'Centro de costo'
        verbose_name_plural = 'Centros de costo'
        
class areas_empresa(models.Model):
    nombre_area = models.CharField(max_length=255, primary_key=True)
    usuario_responsable = models.ForeignKey(User, on_delete = models.PROTECT,null=True,blank=True)
    
    class Meta:
        verbose_name = 'Area empresa'
        verbose_name_plural = 'Areas empresa'
    
    def __str__(self):
        return self.nombre_area
    
class clasificacion(models.Model):
    cuenta = models.ForeignKey(cuentas_contables, on_delete = models.PROTECT)
    tipo = models.CharField(max_length=255, null = True, blank = True, choices=[
        ('FIJO','FIJO'),
        ('VARIABLE','VARIABLE'),
        ('MIXTO','MIXTO'),
    ])
    tipo_r_p = models.CharField(max_length = 255, null=True, blank = True, 
                                verbose_name='Real/Ppto', choices=([
                                    ('REAL','REAL'),
                                    ('PPTO','PPTO'),
                                ]))
    cedos = []
    for c in centro_costo.objects.all().order_by('cedo').distinct('cedo'):
        cedos.append((c.cedo,c.cedo))
    centro_costo = models.CharField(max_length = 255, null=True, blank = True, 
                                    verbose_name='Ceco/Orden', choices=cedos)
    nit_tercero = models.CharField(max_length=255, null = True, blank = True)
    nombre_tercero = models.CharField(max_length=255, null = True, blank = True)
    areas_choices = [(i.nombre_area,i.nombre_area) for i in areas_empresa.objects.all()]
    responsable = models.CharField(max_length=255, null = True, blank = True, choices = areas_choices)
    activo = models.BooleanField(default = True)
    
    class Meta:
        unique_together = ['tipo','tipo_r_p','cuenta','centro_costo','nit_tercero','responsable']
        verbose_name = 'Clasificacion'
        verbose_name_plural = 'Clasificaciones'
        
    def analysis_by_period(self,month,year, include_acumulate, comparate_year):

        obj_gastos = gastos.objects.filter(clasificacion=self.pk,
                                           fecha__year = year,
                                           fecha__month = month
                                           ).aggregate(total_gastos=Sum('importe'))
        obj_gastos = obj_gastos.get('total_gastos') if obj_gastos.get('total_gastos') else 0
        
        obj_rolling = rollling.objects.filter(clasificacion = self.pk,
                                              anio = year,
                                              mes = month
                                              ).aggregate(total_rolling=Sum('valor'))
        obj_rolling = obj_rolling.get('total_rolling') if obj_rolling.get('total_rolling') else 0
        
        obj_gastos_acum = None
        obj_rolling_acum = None
        obj_gastos_comp_year = None
        obj_rolling_comp_year = None
        
        if include_acumulate == 'true':
            
            obj_gastos_acum = gastos.objects.filter(clasificacion=self.pk,
                                            fecha__year = year,
                                            fecha__month__gte = 1,
                                            fecha__month__lte = month
                                            ).aggregate(total_gastos=Sum('importe'))
            
            obj_gastos_acum = obj_gastos_acum.get('total_gastos') if obj_gastos_acum.get('total_gastos') else 0
            
            obj_rolling_acum = rollling.objects.filter(clasificacion = self.pk,
                                                anio = year,
                                                mes__gte = 1,
                                                mes__lte = month
                                                ).aggregate(total_rolling=Sum('valor'))
        
            obj_rolling_acum = obj_rolling_acum.get('total_rolling') if obj_rolling_acum.get('total_rolling') else 0
            
            
        if comparate_year == 'true':
            obj_gastos_comp_year = gastos.objects.filter(clasificacion=self.pk,
                                            fecha__year = year-1,
                                            fecha__month__gte = 1,
                                            fecha__month__lte = month
                                            ).aggregate(total_gastos=Sum('importe'))
            
            obj_gastos_comp_year = obj_gastos_comp_year.get('total_gastos') if obj_gastos_comp_year.get('total_gastos') else 0
            
            obj_rolling_comp_year = rollling.objects.filter(clasificacion = self.pk,
                                                anio = year-1,
                                                mes__gte = 1,
                                                mes__lte = month
                                                ).aggregate(total_rolling=Sum('valor'))
            
            obj_rolling_comp_year = obj_rolling_comp_year.get('total_rolling') if obj_rolling_comp_year.get('total_rolling') else 0
        
        
        period = {
            'gastos':obj_gastos,
            'rolling':obj_rolling,
            'gastos_acum':obj_gastos_acum,
            'rolling_acum':obj_rolling_acum, 
            'gastos_comp_year':obj_gastos_comp_year,
            'rolling_comp_year':obj_rolling_comp_year,     
        }
            
        return period
    
    def __str__(self):
        return f'({self.pk}) - {self.cuenta} - {self.nombre_tercero}'
    
class gastos(models.Model):
    cuenta = models.ForeignKey(cuentas_contables, on_delete = models.PROTECT)
    nit_tercero = models.CharField(max_length=255, null = True, blank = True)
    nombre_tercero = models.CharField(max_length=255, null = True, blank = True)
    importe = models.FloatField()
    ceco = models.ForeignKey(centro_costo,on_delete=models.PROTECT, null = True, blank = True)
    fecha = models.DateField()
    n_doc = models.CharField(max_length=255, null = True, blank = True)
    referencia = models.CharField(max_length=255, null = True, blank = True)
    importe_usd = models.FloatField(null= True, blank = True)
    cebe = models.CharField(max_length=255, null =True, blank = True)
    texto = models.CharField(max_length=255, null=True, blank = True)
    asignacion = models.CharField(max_length=255,null=True, blank = True)
    posicion = models.IntegerField(null=True, blank = True)
    clasificacion = models.ForeignKey(clasificacion, on_delete=models.PROTECT,
                                      null=True, blank = True)
    usuario_carga = models.ForeignKey(User, on_delete=models.PROTECT,
                                      related_name='user_carga')
    
    class Meta:
        unique_together = ['n_doc','posicion']
        
class rollling(models.Model):
    mes = models.IntegerField()
    anio = models.IntegerField(verbose_name='Año')
    clasificacion = models.ForeignKey(clasificacion, on_delete= models.PROTECT)
    valor = models.FloatField()
    valor_previo = models.FloatField(null=True,blank=True)
    
    class Meta:
        
        unique_together = ['mes','anio','clasificacion']
        
    def real(self):
        object_gasto = gastos.objects.filter(fecha__year = self.anio, fecha__month=self.mes, 
                              clasificacion = self.clasificacion.pk).aggregate(total = Sum('importe'))
        total_gasto  = object_gasto.get('total')
        
        if total_gasto == None: total_gasto = 0
        
        return total_gasto
        
class cierre_de_mes(models.Model):
    mes = models.IntegerField()
    annio = models.IntegerField(verbose_name='Año')
    estado = models.CharField(max_length=255, choices=[
        ('Abierto','Abierto'),
        ('Cerrado','Cerrado'),
    ])
    usuario_cierra = models.ForeignKey(User, on_delete=models.PROTECT,
                                      related_name='user_cierra', null=True,
                                      blank=True)
    
    class Meta:
        
        unique_together = ['mes','annio']

class rules(models.Model):
    premise = models.CharField(max_length=999, unique = True)
    statement = models.CharField(max_length=999)
    active = models.BooleanField()

    

    