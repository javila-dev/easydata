from datetime import datetime
from django import forms
from pkg_resources import require
from human_resources.models import (auxilios_contrato, base_personal, cargo, 
                                    BONIFICACION_TYPE_CHOICES,
                                    cceco as cceco_model, departamento as departamento_model, empleadores,
                                    eps as eps_model, estructura, 
                                    fondo_cesantias, fondo_pensiones, arl as arl_model,
                                    ccf as ccf_model, canal as canal_model, motivos_retiro, sede as sede_model, temporales, tipos_auxilio
)                               
from useraccounts.models import Rol
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Field, HTML
from crispy_forms.bootstrap import AppendedText, PrependedAppendedText, PrependedText, StrictButton, TabHolder, Tab, FieldWithButtons
from useraccounts.crispycustomfields import dropdownField, inlineField, dateField, iconField, checkbox, transparentInput


class checkworkersForm(forms.Form):
    archivo_compara = forms.FileField(label='Archivo comparacion')
    choices = (
        ('','Selecciona...'),
        (1,'A'),(2,'B'),(3,'C'),
        (4,'D'),(5,'E'),(6,'F'),
        (7,'G'),(8,'H'),(9,'I'),
        (10,'J'),(11,'K'),(12,'L'),
        (13,'M'),(14,'N'),(15,'O'),
        (16,'P'),(17,'Q'),(18,'R'),
        (19,'S'),(20,'T'),(21,'U'),
        (22,'V'),(23,'W'),(24,'X'),
        (25,'Y'),(26,'Z'),
    )
    nombre_hoja = forms.CharField(max_length=255)
    col_cc = forms.ChoiceField(choices=choices, label='Col cedula')
    col_fecharetiro = forms.ChoiceField(choices=choices, label='Col Fecha retiro')

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'form-checkworkers'
        self.helper.form_class = 'ui form'
        self.helper.layout =Layout(
            Div(
                Div(
                    Field('nombre_hoja'),
                    dropdownField('col_cc'),
                    dropdownField('col_fecharetiro'),
                    css_class="three fields hojas"
                ), id='content-sheet'
            ),
            
            Field('archivo_compara', css_class='readonly', readonly=True,
                  accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel"),
            
        )

class importMasiveForm(forms.Form):
    archivo_importar = forms.FileField(label='Archivo importar')
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'form-importmasive'
        self.helper.form_class = 'ui form'
        self.helper.layout =Layout(
            Field('archivo_importar', css_class='readonly', readonly=True,
                  accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel"),
            HTML('<br>Descarga el archivo para diligenciar <button class="ui primary tertiary button" type="button" id="btn-download-import-file">Aquí</button>, ten en cuenta que las listas estan solo en la primera fila (2), si necesitas agregar mas de una persona, por favor copia esta fila tantas veces como necesites.'),
            
            
        )

class workersForm(forms.Form):
    numero_id = forms.CharField(max_length=255,label="")
    tipo_id = forms.ChoiceField(choices=(
        ('','Selecciona...'),
        ('CC','Cedula de ciudadanía'),
        ('CE','Cedula de extranjería'),
        ('TI','Tarjeta de identidad'),
        ('PPT','PPT'),
        ('PEP','PEP'),
        ('PA','Pasaporte'),
    ), label = "")
    codigo_sap = forms.CharField(max_length=255, required=False, label = '')
    primer_nombre = forms.CharField(max_length=255,label="")
    segundo_nombre = forms.CharField(max_length=255, required=False,label="")
    primer_apellido = forms.CharField(max_length=255,label="")
    segundo_apellido = forms.CharField(max_length=255, required=False,label="")
    email = forms.EmailField(required=False)
    direccion = forms.CharField(max_length=255)
    departamento = forms.ModelChoiceField(departamento_model.objects.all().order_by('nombre'),
                                  empty_label='Seleciona...')
    ciudad = forms.ChoiceField(choices=(
        ('','Selecciona...'),
    ))
    celular = forms.CharField(max_length=255, label='')
    telefono = forms.CharField(max_length=255, required=False, label='')
    tipo_vivienda = forms.ChoiceField(choices=(
        ('','Selecciona...'),
        ('Propia','Propia'),
        ('Familiar','Familiar'),
        ('Arrendada','Arrendada'),
    ))
    sexo = forms.ChoiceField(choices=(
        ('','Selecciona...'),
        ('M','Masculino'),
        ('F','Femenino'),
        ('O','Otro'),
    ), required=True)
    nivel_educativo = forms.ChoiceField(choices=(
        ('','Selecciona...'),
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
    ))
    titulo = forms.CharField(max_length=255, required = False)
    rh = forms.ChoiceField(choices=(
        ('','Selecciona...'),
        ('A-','A-'),
        ('A+','A+'),
        ('AB-','AB-'),
        ('AB+','AB+'),
        ('B-','B-'),
        ('B+','B+'),
        ('O-','O-'),
        ('O+','O+'),
        ('ND','NO DEFINIDO'),
    ))
    estado_civil = forms.ChoiceField(choices=(
        ('','Selecciona...'),
        ('SOLTERO (A)','SOLTERO (A)'),
        ('CASADO (A)','CASADO (A)'),
        ('VIUDO (A)','VIUDO (A)'),
        ('DIVORCIADO (A)','DIVORCIADO (A)'),
        ('UNION LIBRE','UNION LIBRE'),
    ))
    fecha_nacimiento = forms.DateField()
    eps = forms.ModelChoiceField(eps_model.objects.all(), empty_label='Selecciona...')
    pension = forms.ModelChoiceField(fondo_pensiones.objects.all(), empty_label='Selecciona...')
    cesantias = forms.ModelChoiceField(fondo_cesantias.objects.all(), empty_label='Selecciona...')
    arl = forms.ModelChoiceField(arl_model.objects.all(), empty_label='Selecciona...')
    tipo_riesgo = forms.ChoiceField(choices=(
        ('','Selecciona...'),
        ('0.522','Riesgo I (0.522%)'),
        ('1.044','Riesgo II (1.044%)'),
        ('2.436','Riesgo III (2.436%)'),
        ('4.350','Riesgo IV (4.350%)'),
        ('6.960','Riesgo V (6.960%)'),
        ('OTRO','Otro'),
        ('NO APLICA','No Aplica'),
    ))
    ccf = forms.ModelChoiceField(ccf_model.objects.all(), empty_label='Selecciona...',
                                 label='Caja de compensación')
    
    talla_camisa = forms.CharField(max_length=255, required=False)
    talla_pantalon = forms.CharField(max_length=255, required=False)
    talla_calzado = forms.CharField(max_length=255, required=False)
    
    tipo_ingreso = forms.ChoiceField(choices=(
        ('','Selecciona...'),
        ('A','Aprendizaje'),
        ('T','Temporal'),
        ('V','Vinculado')
    ))
    modalidad_ingreso = forms.ChoiceField(choices=(
        ('','selecciona...'),
        ('Nuevo ingreso por temporal',' Nuevo ingreso por temporal'),
        ('Nuevo ingreso directo','Nuevo ingreso directo'),
        ('Nuevo ingreso directo (temporal a directo)','Cambio temporal a directo'),
        ('Reingreso','Reingreso'),
    ))
    tipo_contrato = forms.ChoiceField(choices=(
        ('','selecciona...'),
        ('Indefinido','Indefinido'),
        ('Obra o Labor','Obra o Labor'),
        ('Aprendizaje','Aprendizaje')
        )
    )
    empleador = forms.ModelChoiceField(empleadores.objects.all(),
                                       empty_label='Selecciona...')
    temporal = forms.ModelChoiceField(temporales.objects.all(),
                                       empty_label='Selecciona...', required=False)
    fecha_inicio = forms.DateField()
    fecha_fin_pp = forms.DateField(required = False, label = 'Fin periodo de prueba')
    fecha_fin_cto  = forms.DateField(required=False, label = 'Fecha fin contrato')
    
    estruct = forms.ModelChoiceField(estructura.objects.all(), 
                                   empty_label='Seleciona...',required=True,
                                   label='Gerencia')
    area = forms.ChoiceField(choices=(
        ('','selecciona...'),
    )) 
    cargo = forms.ChoiceField(choices=(
        ('','selecciona...'),
    ))
    canal =  forms.ModelChoiceField(canal_model.objects.all(), 
                                   empty_label='Seleciona...',required=False,
                                   label='Orden')
    cceco = forms.ModelChoiceField(cceco_model.objects.all(),
                                   empty_label='Seleciona...',required=False,
                                   label='Centro de costo')
    sede = forms.ModelChoiceField(sede_model.objects.all(),
                                  empty_label='Seleciona...',
                                  label='Ubicación')
    jefe_inmediato = forms.ModelChoiceField(
        base_personal.objects.filter(trabajador__activo = True),
        empty_label='Seleciona...'
    )
       
    
    salario_base = forms.CharField(max_length=255)
    motivo_cambio_salario = forms.CharField(max_length=255, required=False)
    auxilio_transporte = forms.CharField(max_length=255, required=False)
    bonificacion = forms.ChoiceField(choices=(('','Selecciona...'), *BONIFICACION_TYPE_CHOICES), required=False)
    base_bonificacion = forms.CharField(max_length=255, required=False)
    fecha_retiro = forms.DateField(required = False)
    motivo_retiro = forms.ModelChoiceField(motivos_retiro.objects.all(),
                                           empty_label='Seleciona...',required=False)
    motivo_retiro_real = forms.CharField(max_length=255, required=False,
                                         label='Motivo real de retiro')
    
    es_empalme = forms.BooleanField(required=False, label='¿Es empalme?')
    empleado_sale = forms.ModelChoiceField(
        base_personal.objects.filter(trabajador__activo = True),
        empty_label='Seleciona...', required=False
    )
    fecha_inicio_empalme = forms.DateField(required=False)
    fecha_fin_empalme = forms.DateField(required=False)
    motivo_empalme = forms.ChoiceField(choices=(
        ('','Selecciona...'),
        ('Licencia maternidad','Licencia maternidad'),
        ('Licencia medica','Licencia medica'),
        ('Reemplazo','Reemplazo'),
        ('NA','No aplica'),
    ))
    

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'form-workers'
        self.helper.form_class = 'ui form'
        self.helper.layout =Layout(
            Div(
                Div(
                    PrependedText('tipo_id','Tipo Id', css_class='not-modify ui dropdown'), 
                    css_class='five wide field'
                ),
                Div(
                    PrependedText('numero_id','Numero Id', css_class='text-center not-modify numbers'), 
                    css_class='six wide field'
                ),
                Div(
                    PrependedText('codigo_sap','Codigo SAP', css_class='text-center'), 
                    css_class='five wide field'
                ),
                css_class='fields personalinfo',  
            ),
            Div(
                HTML('<label>Nombre completo</label>'),
                Div(
                    Field('primer_nombre', css_class='', placeholder = 'Primer nombre'),
                    Field('segundo_nombre', css_class='', placeholder = 'Segundo nombre'),
                    Field('primer_apellido', css_class='', placeholder = 'Primer apellido'),
                    Field('segundo_apellido', css_class='', placeholder = 'Segundo apellido'),
                    css_class='four fields'
                ),
                css_class='field personalinfo'
            ),
            Div(
                Div(HTML('<i class="dropdown icon"></i>Información Personal'),id="div_infopersonal",css_class='title'),
                Div(
                    Div(
                        Div(
                            dateField('fecha_nacimiento', css_class=''),
                            css_class='field'
                        ),
                        Div(
                            dropdownField('sexo', css_class='required'),
                            css_class='field'
                        ),
                        Div(
                            dropdownField('tipo_vivienda', css_class='required'),
                            css_class='field'
                        ),
                        Div(
                            dropdownField('estado_civil', css_class='required'),
                            css_class='field'
                        ),
                        Div(
                            dropdownField('rh', css_class='required'),
                            css_class='field'
                        ),
                        css_class='five fields'
                    ),
                    Div(
                        Div(
                            HTML('<label>Numeros de contacto</label>'),
                            Div(
                                Field('celular', css_class='', placeholder = 'Principal'),
                                Field('telefono', css_class='', placeholder = 'Alterno'),
                                css_class='two fields'
                            ),
                            css_class='four wide field'
                        ),
                        Div(
                            Field('email'),
                            css_class='four wide field'
                        ),
                        
                        Div(
                            dropdownField('nivel_educativo', css_class='required'),
                            css_class='four wide field'
                        ),
                        Div(
                            Field('titulo', css_class='required'),
                            css_class='four wide field'
                        ),
                        css_class='fields'
                    ),
                    Div(
                        Div(
                            Field('direccion', css_class=''),
                            css_class='four wide field'
                        ),
                        Div(
                            dropdownField('departamento', css_class='search selection required'),
                            css_class='three wide field'
                        ),
                        Div(
                            dropdownField('ciudad', css_class='search selection required'),
                            css_class='three wide field'
                        ),
                        Div(
                            Div(
                                Field('talla_camisa', css_class='text-center'),
                                Field('talla_pantalon', css_class='text-center'),
                                Field('talla_calzado', css_class='text-center'),
                                css_class='three fields'
                            ),
                            css_class='six wide field'
                        ),
                        css_class='fields'
                    ),
                    css_class='content personalinfo'
                ),
                Div(HTML('<i class="dropdown icon"></i>Afiliaciones'),id="div_afiliaciones",css_class='title'),
                Div(
                    Div(
                        dropdownField('eps', css_class='search selection required'),
                        dropdownField('cesantias', css_class='search required selection'),
                        dropdownField('pension', css_class='search required selection'),
                        css_class='three fields'
                    ),
                    Div(
                        dropdownField('arl', css_class='required'),
                        dropdownField('tipo_riesgo', css_class='required'),
                        dropdownField('ccf', css_class='search selection required'),
                        css_class='three fields'
                    ),
                    css_class='content personalinfo'
                ),
                Div(HTML('<i class="dropdown icon"></i>Generalidades contrato'),id="div_contrato",css_class='title'),
                Div(
                    Div(
                        dropdownField('tipo_ingreso', css_class='not-modify required'),
                        dropdownField('empleador', css_class='not-modify required'),
                        dropdownField('temporal', css_class='not-modify'),
                        dropdownField('modalidad_ingreso', css_class='not-modify required'),
                        css_class='equal width fields'
                    ),
                    Div(
                        dropdownField('tipo_contrato', css_class='not-modify required'),
                        dateField('fecha_inicio', css_class='not-modify'),
                        dateField('fecha_fin_pp', css_class='not-modify'),
                        dateField('fecha_fin_cto', css_class='not-modify'),
                        css_class='four fields'
                    ),
                    checkbox('es_empalme', css_class='slider not-modify', slider=True),
                    Div(
                        Div(
                            dropdownField('empleado_sale', css_class='not-modify'),
                            css_class='five wide field'
                        ),
                        dateField('fecha_inicio_empalme', css_class='not-modify'),
                        dateField('fecha_fin_empalme', css_class='not-modify'),
                        
                        dropdownField('motivo_empalme', css_class='not-modify'),
                        
                        
                        css_class='four fields initial-hide', id='div-empalme'
                    ),
                    css_class='content contractinfo'
                ),
                Div(HTML('<i class="dropdown icon"></i>Cargo y clasificaciones'),id="div_cargo",css_class='title'),
                Div(
                    Div(
                        dropdownField('estruct', css_class='not-modify required'),
                        dropdownField('area', css_class='not-modify required'),
                        dropdownField('cargo', css_class='not-modify search selection required'),
                        css_class='three fields'
                    ),
                    Div(
                        dropdownField('sede', css_class='not-modify search selection required'),
                        dropdownField('cceco', css_class='not-modify search selection required'),
                        dropdownField('jefe_inmediato', css_class='search selection'),
                        css_class='three fields'
                    ),
                    css_class='content contractinfo'
                ),
                Div(HTML('<i class="dropdown icon"></i>Salario, auxilios y bonificaciones'),id="div_salarios",css_class='title'),
                Div(
                    Div(
                        Div(
                            PrependedText('salario_base','$', css_class='not-modify text-center money'),
                            css_class='five wide field'
                        ),
                        Div(
                            PrependedText('auxilio_transporte','$', css_class='not-modify text-center money'),
                            css_class='four wide field'
                        ),
                        Div(
                            dropdownField('bonificacion',css_class='not-modify ui dropdown'),
                            css_class='three wide field'
                        ),
                        Div(
                            PrependedText('base_bonificacion',"$", css_class='not-modify text-center money'),
                            css_class='four wide field'
                        ),
                        css_class='fields'
                    ),
                            Field('motivo_cambio_salario'),
                    
                    HTML(
                        '<table class="ui compact celled definition table" style="width:60%!important" id="table-auxilios"><thead><tr><th><button class="btn ui primary button visible" id="btn_auxilios" type="button" style="display: inline-block !important;">Agregar</button></th><th style="width:50%">Auxilio</th><th style="width:30%">Valor</th></tr></thead><tbody></tbody></table>'
                    ),
                    css_class='content contractinfo'
                ),
                Div(HTML('<i class="dropdown icon"></i>Retiro'),id="div_retiro",css_class='title'),
                Div(
                    Div(
                        Div(
                            dateField('fecha_retiro', css_class='not-modify'),
                            css_class='five wide field'
                        ),
                        Div(
                            dropdownField('motivo_retiro', css_class='not-modify'),
                            css_class='five wide field'
                        ),
                        Div(
                            Field('motivo_retiro_real', css_class='not-modify'),
                            css_class='six wide field'
                        ),
                        css_class='fields'
                    ),
                    css_class='content contractinfo'
                ),
                css_class='ui styled fluid accordion'
            ),
            
        )
        
class auxiliosForm(forms.Form):
    tipo_auxilio = forms.ModelChoiceField(tipos_auxilio.objects.all())
    valor_auxilio = forms.CharField(max_length=255, required=False)
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'form-auxilios'
        self.helper.form_class = 'ui form'
        self.helper.layout =Layout(
            dropdownField('tipo_auxilio'),
            PrependedText('valor_auxilio', '$', css_class='text-center money'),
        )

class retiroForm(forms.Form):
    motivo_retiro = forms.ModelChoiceField(motivos_retiro.objects.all(), 
                                           empty_label='Selecciona...')
    motivo_real = forms.CharField(max_length=255, widget=forms.Textarea({'rows':2}),
                                  required=False)
    fecha_retiro = forms.DateField()
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'form-retiro'
        self.helper.form_class = 'ui form'
        self.helper.layout =Layout(
            dateField('fecha_retiro'),
            dropdownField('motivo_retiro',css_class='ui dropdown required'),
            Field('motivo_real'),
        )

class descargosForms(forms.Form):
    fecha_descargo = forms.DateField()
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'form-descargos'
        self.helper.form_class = 'ui form'
        self.helper.layout = Layout(
            dateField('fecha_descargo'),
        )
