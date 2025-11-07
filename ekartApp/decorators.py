from django.shortcuts import redirect
from django.contrib import messages



def login_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.warning(request,'Please login to access this page')
            return redirect('login')
        else:
            return fn(request,*args,**kwargs)
    return wrapper
        
            