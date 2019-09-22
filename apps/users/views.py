from django.shortcuts import render,HttpResponse
from django.contrib.auth import authenticate,login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.views.generic import View,TemplateView
from django.contrib.auth.hashers import make_password
from utils.email_send import send_register_eamil

from .forms import LoginForm,RegisterForm,ForgetPwdForm,ChangePwdForm
from .models import UserProfile,EmailVerifyRecord

class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            # user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            print(user,'haha')
            if user.check_password(password):
                return user
        except Exception as e:
            return None

#
class LoginView(View):
    def get(self,request):
        return render(request,'login.html',{})
    def post(self,request):
        login_form=LoginForm(request.POST)
        if login_form.is_valid():
            user_name=login_form.cleaned_data.get('username')
            pass_word=login_form.cleaned_data.get('password')
            user = authenticate(username=user_name, password=pass_word)
            if user:
                if user.is_active:
                    login(request, user)
                    return render(request, 'index.html', {'user': user})
                else:
                    return render(request,'login.html',{'message':'未激活请激活邮箱账号'})
            else:
                return render(request,'login.html',{'message':'用户名或密码错误'})
        else:
            return render(request, 'login.html', {'login_form':login_form})



# 函数方法解决登陆问题
# def log_in(request):
#     if request.method == 'POST':
#         user_name=request.POST.get('username','')
#         pass_word=request.POST.get('password','')
#         user=authenticate(username=user_name,password=pass_word)
#         if user:
#             login(request,user)
#             return render(request,'index.html',{'user':user})
#         else:
#             return render(request,'login.html',{'message':'用户名或密码错误'})
#     elif request.method == 'GET':
#         return render(request,'login.html',{})

class RegisterView(View):
    def get(self,request):
        register_form=RegisterForm()
        return render(request,'register.html',{'register_form':register_form})
    def post(self,request):
        register_form=RegisterForm(request.POST)
        print(register_form)
        if register_form.is_valid():
            user_name = register_form.cleaned_data.get('email')
            if UserProfile.objects.filter(email=user_name):
                return render(request, 'register.html', {'msg': '邮箱已经注册','register_form':register_form})
            else:
                pass_word = register_form.cleaned_data.get('password')
                user_profile = UserProfile(username=user_name, email=user_name, password=make_password(pass_word))
                user_profile.is_active = False
                user_profile.save()
                send_register_eamil(user_name, 'register')
                # print(user_name,pass_word,'dddddddd')
                return render(request, 'login.html')
        else:
            return render(request,'register.html',{'register_form':register_form})

class ActiveView(View):
    def get(self,request,active_code):
        all_recoreds=EmailVerifyRecord.objects.filter(code=active_code)
        if all_recoreds:
            for recored in all_recoreds:
                email=recored.email
                user=UserProfile.objects.get(email=email)
                user.is_active=True
                user.save()
        else:
            return render(request,'active_fail.html')
        return render(request,'index.html')

class ForgetPassView(View):
    def get(self,request):
        forget_form=ForgetPwdForm()
        return render(request,'forgetpwd.html',{'forget_form':forget_form,'register_form':RegisterForm()})

    def post(self,request):
        forget_form=ForgetPwdForm(request.POST)
        if forget_form.is_valid():
            email=forget_form.cleaned_data.get('email')
            send_register_eamil(email,send_type = 'forget')
            return render(request,'send_success.html')
        else:
            return render(request,'forgetpwd.html',{'forget_form':forget_form})

class Reset(View):
    def get(self,request,active_code):
        record=EmailVerifyRecord.objects.filter(code=active_code).first()
        if record:
            email=record.email
            return render(request,'password_reset.html',{'email':email,'active_code':active_code})
        else:
            return render(request,'active_fail.html')

class ChangepwdView(View):
    def post(self,request):
        change_pwd_form=ChangePwdForm(request.POST)
        if change_pwd_form.is_valid():
            pwd1=change_pwd_form.cleaned_data.get('password1')
            pwd2=change_pwd_form.cleaned_data.get('password2')
            email=request.POST.get('email','')
            active_code = request.POST.get('active_code')
            active_code = EmailVerifyRecord.objects.filter(code=active_code).first()

            if pwd1!=pwd2:
                return render(request,'password_reset.html',{'msg':'密码不一致','email':email})

            if active_code.email == email:
                user=UserProfile.objects.get(email=email)
                user.password=make_password(pwd1)
                user.save()
                return render(request, 'login.html')
            else:
                return render(request,'password_reset.html',{'msg':'邮箱内激活链接无效'})

        else:
            email=request.POST.get('email','')
            active_code = request.POST.get('active_code')
            return render(request,'password_reset.html',{'email':email,'change_pwd_form':change_pwd_form,'active_code':active_code})