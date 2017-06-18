from django.shortcuts import render, get_object_or_404,redirect
from django.utils.translation import ugettext as _
# Create your views here.
from django.contrib.auth.models import User, Group
from .forms import CheckForm
from usermanage.models import Accounts
from django.contrib.auth import hashers, authenticate, login, logout

from django.forms import ValidationError
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from ratelimit.decorators import ratelimit
#@ratelimit(key='ip', rate='5/h')
def check(request):
    if request.method == 'POST':
        form = CheckForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user_profile = get_object_or_404(User, username=username)
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    if username==str(request.user):
                        return redirect('transfer:transferProcess')
                    else:
                        form.add_error(None, ValidationError(_('Please check your log in credentials'), code='invalid'))
            else:
                form.add_error(None, ValidationError(_('Please check your log in credentials'), code='invalid'))
    else:
        form = CheckForm()
    return render(request=request,template_name='usercheck/paycheck.html', context={'form': form})
