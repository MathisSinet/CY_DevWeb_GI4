from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect
from accounts.models import User, UserLevel

def verified_required(view_func):
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.verified:
            return redirect("check_email")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def expert_required(view_func):
    @verified_required
    def _wrapped_view(request, *args, **kwargs):
        user: User = request.user
        if not user.current_level == UserLevel.EXPERT:
            return redirect("index")
        return view_func(request, *args, **kwargs)
    return _wrapped_view