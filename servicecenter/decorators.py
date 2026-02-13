from django.shortcuts import redirect

def servicecenter_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get("servicecenter_id"):
            return redirect("company:login_servicecenter")
        return view_func(request, *args, **kwargs)
    return wrapper
