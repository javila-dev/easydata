from datetime import datetime
from django import forms
from useraccounts.models import Rol
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Field, HTML
from crispy_forms.bootstrap import AppendedText, PrependedAppendedText, PrependedText, StrictButton, InlineRadios
from useraccounts.crispycustomfields import dropdownField, inlineField, dateField, iconField, checkbox, transparentInput

class usersForm(forms.Form):
    username = forms.CharField(max_length=255,label='')
    first_name = forms.CharField(max_length=255,label='Nombre')
    last_name = forms.CharField(max_length=255,label='Apellidos')
    birth_date = forms.DateField(label="Fecha de nacimiento")
    email = forms.EmailField()
    user_id = forms.CharField(max_length=255,label='Identificación', required = False)
    picture = forms.ImageField(label = 'Foto/Avatar', required=False)
    rols = forms.ModelChoiceField(queryset=Rol.objects.all().order_by('descripcion'),label='Roles')
    is_active = forms.BooleanField(label='Activo',required=False)
    is_staff = forms.BooleanField(label='Acceso al AdminSite',required=False)
    
    
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'form-user'
        self.helper.form_class = 'ui form'
        self.helper.layout =Layout(
            Div(
                transparentInput('username',css_class="text-center mb-2",
                                 readonly=True),
                checkbox('is_active',slider=True),
                Div(
                    HTML(
                        """
                        <h3 class="ui header">
                            <i class="address card outline icon"></i>
                            <div class="content">
                            Información personal
                            <div class="sub header">Información basica del usuario</div>
                            </div>
                        </h3>
                        """
                    ),
                    
                    Field('first_name'),
                    Field('last_name'),
                    Div(
                        Field('user_id'),
                        dateField('birth_date'),
                        css_class='two fields',
                    ),
                    Field('email'),
                    css_class='ui segment'
                ),
                Div(
                    HTML(
                        """
                        <h3 class="ui header">
                            <i class="question circle outline icon"></i>
                            <div class="content">
                            Perfil de usuario
                            <div class="sub header">Información del perfil</div>
                            </div>
                        </h3>
                        """
                    ),
                    dropdownField('rols',css_class='multiple search selection'),
                    Field('picture'),
                    checkbox('is_staff',slider=True),
                    css_class='ui segment'
                ),
                Div(
                    Submit('registrar','Registrar',css_class='ui green button'),
                    StrictButton('Cancelar',id="btn-cancel-user",css_class="ui red button"),
                    StrictButton('Reenviar correo',id="btn-resend-email",css_class="ui teal button", hidden=True),
                    css_class='ui center aligned basic segment'
                ),
                HTML('<div class="ui inverted active dimmer"></div>'),
            css_class="ui basic blurring segment",
            id='segment-users-form'
            )
        )
    