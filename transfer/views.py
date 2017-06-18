from django.shortcuts import render, get_object_or_404,redirect

# Create your views here.
from django.contrib.auth.models import User, Group
from django.contrib.auth import hashers, authenticate, login, logout
from usermanage.models import Accounts
from .models import BusinessRecord
from django.forms import ValidationError
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from bank.settings import LOGIN_URL
from django.contrib import messages
from accmanage.models import TemporaryRecord
from django.utils import timezone
# Create your views here.
def transferProcess(request):
    transfer = get_object_or_404(TemporaryRecord,user=request.user)
    target=transfer.target
    money=transfer.money
    order=transfer.transferID
    comment=transfer.comment
    user_profile=get_object_or_404(User,username=str(request.user))
    if user_profile is not None:
        if user_profile.is_active :
            transfer.process=True
            transfer.save()
            user_account = get_object_or_404(Accounts, user=user_profile)
            user_account.balance -= money
            if user_account.balance>=0:
                user_account.save()
                target_user=get_object_or_404(User,username=target)
                target_account=get_object_or_404(Accounts, user=target_user)
                target_account.balance += money
                target_account.save()
                transferRec=BusinessRecord(transferID=str(order),
                                    user=str(request.user),
                                    money=money,
                                    operation=0,
                                    date=timezone.localtime(timezone.now()),
                                    comment=comment,
                                    target=target)
                transferRec.save()
                return redirect('transfer:paysuccess')
            else:
                return redirect('transfer:insufficientBalance')
    return render(request=request,emplate_name='transfer/pay.html')


def paysuccess(request):
    return render(request=request,template_name='transfer/paysuccess.html')

def insufficientBalance(request):
    return render(request=request,template_name='transfer/insufficientBalance.html')
