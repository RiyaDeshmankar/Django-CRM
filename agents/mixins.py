from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect

# we are using custom mixins for custom login requiremnts
class OrganisorAndLoginRequiredMixin(AccessMixin):
    """Verify that current user is authenticated and is an organisor"""
    def dispatch(self,request, *args, **kwargs):
        #user logged in should have is_organisor attr
        if not request.user.is_authenticated or not request.user.is_organisor:
            return redirect("leads:lead-list") #if not organisor redirects them to login page
        return super().dispatch(request,*args,**kwargs)