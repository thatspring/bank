from django.shortcuts import render, get_object_or_404,redirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
# Create your views here.
from django.contrib.auth.models import User, Group
from .forms import TransferForm,InfoForm,ShowForm,PayForm
from .models import TemporaryRecord
from django.contrib.auth import hashers, authenticate, login, logout

from django.forms import ValidationError
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from bank.settings import LOGIN_URL
from django.contrib import messages

from django.utils import timezone
import time
def transferAccount(request):
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            human=True
            money = form.cleaned_data['money']
            comment = form.cleaned_data['comment']
            target = form.cleaned_data['target']
            captcha=form.cleaned_data['captcha']
            target_user=get_object_or_404(User, username=target)
            userID=request.user.id
            time1=time.strftime("%Y%m%d%H%M%S",time.localtime(time.time()))
            transferID=str(userID).zfill(10)+time1
            info = TemporaryRecord(transferID=transferID,
                                user=str(request.user),
                                money=money,
                                comment=comment,
                                target=target,
                                process=False)
            try :
                TemporaryRecord.objects.filter(user=request.user).delete()
            except:
                pass
            info.save()
            if target_user is not None:
                if target_user.is_active:
                    return redirect('accmanage:checkTransfer')
                    #return redirect(accmanage:checkTransfer)
            else:
                form.add_error(None, ValidationError(_('target error'), code='invalid'))
    else:
        form = TransferForm()
    return render(request=request, template_name='accmanage/transfer.html', context={'form': form})


def checkTransfer(request):
    transfer = get_object_or_404(TemporaryRecord,user=request.user)
    target=transfer.target
    #money=transfer.money
    #order=transfer.transferID
    #comment=transfer.comment
    target_user=get_object_or_404(User,username=target)
    target_email=target_user.email
    return render(request=request, template_name='accmanage/checkinfo.html', context={'transfer': transfer,'target_email':target_email})

#@csrf_protect
def pay(request):
    if request.method == 'POST':
        form = PayForm(request.POST)
    else:
        form=PayForm()
    return render(request=request,template_name='accmanage/pay.html',context={'form':form})
