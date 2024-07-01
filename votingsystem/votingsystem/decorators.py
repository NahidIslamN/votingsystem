from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def specific_user_required(user_id):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.id == user_id:
                return view_func(request, *args, **kwargs)
            else:
                # Redirect or handle unauthorized access
                messages.error(request, 'Unauthorized access!')
                return redirect('login_page')  # Redirect to login page
        return wrapper
    return decorator
