from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.shortcuts import redirect
from django.conf import settings
from django.utils.translation import gettext as _

class StaffRequiredMixin(object):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            messages.warning(request,_('You do not have the permission required to perform the requested operation.'))
            return redirect(settings.LOGIN_URL)
        return super(StaffRequiredMixin, self).dispatch(request,*args, **kwargs)