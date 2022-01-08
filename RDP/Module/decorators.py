from django.http import HttpResponse
from django.shortcuts import redirect, render
def admin_only(view_func):
    def function(request, *args, **kwargs):
        if request.user.is_admin==True:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse("you don't have permisson!")
    return function