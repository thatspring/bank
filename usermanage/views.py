from django.shortcuts import render, get_object_or_404,redirect

# Create your views here.
from django.contrib.auth.models import User, Group
from .forms import RegisterForm, LoginForm
from .models import Accounts
from django.contrib.auth import hashers, authenticate, login, logout

from django.forms import ValidationError
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.decorators import login_required
from bank.settings import LOGIN_URL
#email check
from django.conf import settings
from .utils.token import Token
from django.core.mail import send_mail
token_confirm = Token(settings.SECRET_KEY.encode())

from ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='5/h')
def index(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            human = True
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            captcha=form.cleaned_data['captcha']
            user_profile = get_object_or_404(User, username=username)
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('usermanage:homepage')
            else:
                form.add_error(None, ValidationError(_('Please check your log in credentials'), code='invalid'))
    else:
        form = LoginForm()
    return render(request=request, template_name='usermanage/login.html', context={'form': form})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user_profile = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password,
                is_active=False,)
            user_profile.save()
            account = Accounts(user=user_profile,balance=20)
            account.save()
            token = token_confirm.generate_validate_token(username)
            message = "\n".join(['Hello!!'.format(username), 'please click your link in email to complete your register:','/'.join(['http://localhost:8080/activate',token])])
            send_mail('user confirm information',message,'345981440@qq.com', [email], fail_silently=False)
            return HttpResponse("请登录到注册邮箱中验证用户，有效期为1个小时。")
    else:
        form = RegisterForm()
    return render(request=request, template_name='usermanage/register.html', context={'form': form})

def active_user(request, token):
    try:
        username = token_confirm.confirm_validate_token(token)
    except:
        username = token_confirm.remove_validate_token(token)
        users = User.objects.filter(username=username)
        for user in users:
	        user.delete()
        return HttpResponse('sorry，your link has been out of date，please <a href=\"' + 'http://localhost:8080/register\">signup</a> again ')
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponse("sorry，your link has some error")
    user.is_active = True
    user.save()
    message = 'successfully!!!，please <a href=\"' + 'http://localhost:8080/\">login</a>'
    return HttpResponse(message)


@login_required(login_url=LOGIN_URL)
def homepage(request):
    user_account = get_object_or_404(Accounts, user=request.user)
    user_profile = user_account.user
    return render(request=request, template_name='usermanage/homepage.html',
                  context={'user_profile': user_profile, 'user_account': user_account})
