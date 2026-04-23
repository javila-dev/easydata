from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test

def user_permission(perms,raise_exception=True):
    
    def check_perms(user):
        if user.is_superuser:
            return True
        elif user.is_anonymous:
            return False
        if perms is not list: perm_list = (perms,) 
        else: perm_list = perms
        has_perms = user.user_profile.has_permissions(perm_list)
        if has_perms:
            return True
        if raise_exception:
            raise PermissionDenied
        return False
    
    return user_passes_test(check_perms,login_url='/accounts/login')

def rol_permissions(rols,raise_exception=True):
    
    def check(user):
        if user.is_superuser:
            return True
        elif user.is_anonymous:
            return False
        
        if rols is not list:
            perms = (rols,) 
        else: perms = rols
        
        has_perms = user.user_profile.has_permissions(perms)
        if has_perms:
            return True
        if raise_exception:
            raise PermissionDenied
        return False
    return user_passes_test(check,login_url='/accounts/login')

def rol_permission(rol,raise_exception=True):
    
    def check(user):
        if user.is_superuser:
            return True
        elif user.is_anonymous:
            return False
        
        has_perms = user.user_profile.has_rols(rol)
        if has_perms:
            return True
        if raise_exception:
            raise PermissionDenied
        return False
    
    return user_passes_test(check,login_url='/accounts/login')


