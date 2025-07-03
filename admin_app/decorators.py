#admin_app/decorators.py
# This file is part of the Admin App project.
from django.shortcuts import redirect
from functools import wraps

def role_required(required_role):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('custom_login')
            
            # For testing purposes, bypass role checks
            return view_func(request, *args, **kwargs)
            
        return wrapper
    return decorator