from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Permiso(models.Model):
    descripcion = models.CharField(unique=True,max_length=255)

    class Meta:
        verbose_name = 'Permiso'
        verbose_name_plural = 'Permisos'

    def __str__(self):
        return self.descripcion.capitalize()

class Rol(models.Model):
    descripcion = models.CharField(unique=True,max_length=255)
    permisos = models.ManyToManyField(Permiso)

    class Meta:
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'

    def __str__(self):
        return self.descripcion.capitalize()

class Perfil(models.Model):
    usuario = models.OneToOneField(User,on_delete=models.CASCADE,related_name='user_profile')
    identificacion = models.CharField(max_length=255,blank=True,null=True)
    fecha_nacimiento = models.DateField(null=True,blank=True)
    avatar = models.ImageField(upload_to='users',null=True,blank=True,verbose_name='Foto')
    rol = models.ManyToManyField(Rol,blank=True)
    permiso = models.ManyToManyField(Permiso,blank=True,)
    force_change_pswd = models.BooleanField(default=1,verbose_name='Forzar cambio de contraseña',
        help_text='Selecciona esta opcion para que el usuario deba cambiar su contraseña en el proximo inicio de sesión') 
    
    class Meta:
        verbose_name = 'Perfil de usuario'
        verbose_name_plural = 'Perfiles de usuarios'
        
    def __str__(self):
        return self.usuario.get_full_name()
    
    def all_permissions(self):
        owned_permissions = []
        roles = self.rol.all()
        for rol in roles:
            permisos = rol.permisos.all()
            for permiso in permisos:
                owned_permissions.append(permiso.descripcion.lower())
        permisos_individuales = self.permiso.all()
        for permiso in permisos_individuales:
            owned_permissions.append(permiso.descripcion.lower())
        if owned_permissions is not list:
            permissions_list = (owned_permissions,)
        else: permissions_list = owned_permissions
        return owned_permissions
    
    def all_rols(self):
        rols = self.rol.all()
        rol_list = []
        for rol in rols:
            rol_list.append(rol.descripcion.lower())
        return rol_list

    def has_permission(self,permission):
        if self.usuario.is_superuser:
            return True
        permisos = self.all_permissions()
        if permission.lower() in permisos:
            return True
        return False
    
    def has_permissions(self,permissions):
        if self.usuario.is_superuser:
            return True
        permisos = self.all_permissions()
        granted_needed = len(permissions)
        granted_owned = 0
        for permission in permissions:
            if permission.lower() in permisos:
                granted_owned += 1
        if granted_owned == granted_needed:
            return True
        return False

    def has_rols(self,rol):
        if self.usuario.is_superuser:
            return True
        roles = self.all_rols()
        if rol.lower() in roles:
                return True
        return False

class passwordreset(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    token = models.CharField(max_length=255)
    valid_true = models.DateField()
    used = models.BooleanField(default=False)
    

class Timeline(models.Model):
    user = models.ForeignKey(User,on_delete=models.PROTECT,related_name='user_timeline',verbose_name='Usuario')
    date = models.DateTimeField(auto_now_add=True,verbose_name='Fecha y hora')
    action = models.CharField(max_length=255,verbose_name='Accion')
    
    class Meta:
        verbose_name = 'Accion'
        verbose_name = 'Historial de acciones'
        
    def __str__(self):
        return self.user.username + '-' +str(self.date)