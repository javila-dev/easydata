import datetime
import secrets
import time
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponse, JsonResponse
from django.contrib.sites.models import Site
from django.contrib import messages
from reports.views import request_is_ajax
from useraccounts.forms import usersForm
from useraccounts.models import Timeline, Rol, Perfil, passwordreset
from Atlantic.utils import send_email_template, user_permission, passwordgenerate, JsonRender


# Create your views here.

def account_login(request):
    
    context = {
        
    }
    
    next_page = request.GET.get('next')
    
    if request.method == 'POST':
        
        username = request.POST.get('user')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        
        time.sleep(1.5)
        
        if user is not None:
            login(request,user)
            messages.info(request, f'Bienvenido de nuevo {user.get_full_name()}')
            next_page = "/welcome" if next_page == "" or next_page == "/" else next_page
            if next_page:
                return redirect(next_page)
            
            return redirect('/welcome')
        else:
            context = {
                'error':True,
                'message': 'El usuario y/o contraseña es incorrecto'
            }
    
    return render(request,'login.html',context)

def reset_password(request):
    
    context = {
        
    }
    
    if request.method == 'GET':
        token = request.GET.get('token')        
        reset = passwordreset.objects.filter(token=token)
        if reset.exists():
            reset = reset.first()
            if datetime.date.today() > reset.valid_true and reset.used is False:
                return  render(request,'404.html',context)
            
            context = {
                'token': token
            }
            
            return render(request, 'resetpassword.html', context)
        
        return  render(request,'404.html',context)
    
    if request.method == 'POST':
        todo = request.POST.get('todo')
        
        if todo == 'sendmail':
            email = request.POST.get('email')
            find_user = User.objects.filter(email=email)
            
            data = {
                    'status':'failed'
                }
            
            if find_user.exists():
                user = find_user.first()
                site =  Site.objects.get(pk=settings.SITE_ID).domain
                token = secrets.token_urlsafe(32)
                url = f'https://{site}/accounts/passwordreset?token=' + token
                email_message = f'Hemos recibido tu solicitud de reestablecimiento de contraseña, puedes continuar haciendo click en el siguiente enlace {url}'
                
                email_context = {
                    'email_title': 'Reestablecimiento de contraseña',
                    'email_message': email_message,
                    'user':user
                }
                
                send_email_template('Reestablecimiento de contraseña',
                                    [email,],
                                    template='email_notification.html',
                                    template_context=email_context)
                
                data = {
                    'status':'ok'
                }
                
                passwordreset.objects.create(
                    user = user,
                    token = token,
                    valid_true = datetime.datetime.now() + datetime.timedelta(days=7),
                )
                
            return JsonResponse(data)
        elif todo == 'resetpassword':
            token = request.POST.get('token')
            pwd = request.POST.get('new_password')
            
            reset = passwordreset.objects.get(token=token)
            user = reset.user
            
            user.set_password(pwd)
            user.save()
            
            reset.used = True
            reset.save()
            
            time.sleep(1.5)
            
            return redirect('/accounts/login/')
        
        
    return HttpResponse('')

@login_required
def welcome(request):
    context = {
        
    }
    
    return render(request, 'welcome.html', context)
    
def account_logout(request):
    logout(request)
    return redirect('/accounts/login')

def resend_welcome_mail(request):
    if request.method == 'POST':
        u = request.POST.get('user')
        
        user = User.objects.get(username=u)
        pswd = passwordgenerate()
        user.set_password(pswd)
        user.save()
            
        domain = Site.objects.get_current().domain
            
        protocol = 'HTTPS'
        email_message = f'''Hola {user.first_name} {user.last_name}, te damos la bienvenida a Easy data by Atlantic, a continuación te compartimos los datos para tu inicio de sesión:
            <ul>
                <li>
                    <strong>Usuario:</strong> {user.username}
                </li>
                <li>
                    <strong>Contraseña:</strong> {pswd}
                </li>
            </ul><br>
            Para ingresar puedes hacer ir a https://{domain}/accounts/login,
                te recomendamos cambiar la contraseña una vez ingreses por primera vez.
        '''
        
        email_context = {
            'email_title': '¡Bienvenid@!',
            'email_message': email_message,
            'user':user
        }
        
        send_email_template(f'Bienvenido a Easy data',
                            [user.email,],
                            template='email_notification.html',
                            template_context=email_context)
                            
        return JsonResponse({})

@login_required
@user_permission('administrar usuarios')
def usersadmin(request):
    context = {
        'users': User.objects.exclude(is_superuser=True).order_by('-is_active','username'),
        'form': usersForm,
    }
    
    if request_is_ajax(request):
        if request.method == 'GET':
            user = request.GET.get('user')
            obj_profile = Perfil.objects.filter(usuario = user)
            rols = obj_profile[0].rol.all().values_list('id')
            
            obj_user = User.objects.filter(pk=user).values(
                'username','first_name','last_name','email','is_staff','is_active'
            )
            
            data = {
                'profile':JsonRender(obj_profile).render(),
                'rols':list(rols),
                'user':list(obj_user)
            }
            
            return JsonResponse(data)
    
    else:
        if request.method == 'POST':
            if request.POST.get('is_new'):
                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')
                email = request.POST.get('email')
                is_staff = request.POST.get('is_staff')
                birth_date = request.POST.get('birth_date')
                rols = request.POST.getlist('rols')
                
                username = email
                
                if User.objects.filter(email = email).exists() or \
                    User.objects.filter(username = username).exists():
                    messages.error(request,'<div class="header">¡Ups!</div>Ya existe un usuario asociado a este correo electronico, intenta con uno nuevo o cambia el correo asociado en el otro usuario.')
                    return render(request,'users_admin.html',context)
                                            
                pswd = passwordgenerate()
                
                username = username.lower().replace(" ","")
                user = User.objects.create_user(                    
                    username,email,pswd)
                
                user.first_name = first_name
                user.last_name = last_name
                user.is_active = True
                user.is_staff = True if is_staff == 'on' else False
                user.save()
                
                profile = Perfil.objects.create(
                    usuario = user,
                    identificacion = request.POST.get('user_id'),
                    fecha_nacimiento = birth_date,
                    force_change_pswd = True
                )
                
                for rol in rols:
                    if rol == "": continue
                    obj_rol = Rol.objects.get(pk=rol)
                    profile.rol.add(obj_rol)
                                    
                if request.FILES.get('picture'):
                    profile.avatar = request.FILES.get('picture')
                    profile.save()
                    
                messages.success(request,f'<div class="header">¡Lo hicimos!</div>Se creó el usuario <strong>{username}</strong>, los datos para el inicio de sesión fueron enviados al correo registrado.')

                Timeline.objects.create(
                    user = request.user,
                    action = f'Creó el usuario {username}',
                )
                
                domain = Site.objects.get_current().domain
                
                protocol = 'HTTPS'
                email_message = f'''Hola {user.first_name} {user.last_name}, te damos la bienvenida a Easy data by Atlantic, a continuación te compartimos los datos para tu inicio de sesión:
                    <ul>
                        <li>
                            <strong>Usuario:</strong> {username}
                        </li>
                        <li>
                            <strong>Contraseña:</strong> {pswd}
                        </li>
                    </ul><br>
                    Para ingresar puedes hacer ir a https://{domain}/accounts/login,
                     te recomendamos cambiar la contraseña una vez ingreses por primera vez.
                '''
                
                email_context = {
                    'email_title': '¡Bienvenid@!',
                    'email_message': email_message,
                    'user':user
                }
                
                send_email_template(f'Bienvenido a Easy data',
                                    [email,],
                                    template='email_notification.html',
                                    template_context=email_context)
            else:
                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')
                email = request.POST.get('email')
                is_staff = request.POST.get('is_staff')
                is_active = request.POST.get('is_active')
                birth_date = request.POST.get('birth_date')
                rols = request.POST.getlist('rols')
                username = request.POST.get('username')
                
                user = User.objects.get(username = username)
                
                if User.objects.filter(email = email).exists() and email != user.email:
                    messages.error(request,'<div class="header">¡Ups!</div>Ya existe un usuario asociado a este correo electronico, intenta con uno nuevo o cambia el correo asociado en el otro usuario.')
                    return render(request,'users_admin.html',context)
                
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.is_active = True if is_active == 'on' else False 
                user.is_staff = True if is_staff == 'on' else False
                user.save()
                
                profile = Perfil.objects.get(usuario = user.pk)
                profile.identificacion = request.POST.get('user_id'),
                profile.fecha_nacimiento = birth_date
                
                profile_rols = profile.rol.all()
                for rol in profile_rols:
                    if rol.pk not in rols:
                        profile.rol.remove(rol)
                
                for rol in rols:
                    obj_rol = Rol.objects.get(pk=rol)
                    has_rol = profile.rol.filter(pk=rol).exists()
                    if not has_rol:
                        profile.rol.add(obj_rol)
                
                        
                messages.success(request,
                    f'<div class="header">¡Lo hicimos!</div>Se actualizaron los datos del usuario <strong>{username}</strong>')

                Timeline.objects.create(
                    user = request.user,
                    action = f'Actualizó los datos del usuario {username}',
                )
    
    context = {
        'users': User.objects.exclude(is_superuser=True).order_by('-is_active','username'),
        'form': usersForm,
    }
    
    
    
    return render(request,'usersadmin.html',context)


def handler404(request, *args, **argv):
    context = {}
    return render(request,'404.html',context)