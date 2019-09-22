__author__ = 'yuchen'
__date__ = '2018/8/1 04:45'

from django import forms
from django.forms import fields
from captcha.fields import CaptchaField
from django.core.exceptions import ValidationError,NON_FIELD_ERRORS

class LoginForm(forms.Form):
    username=forms.CharField(required=True)
    password=forms.CharField(required=True,min_length=5)



class RegisterForm(forms.Form):
    email=forms.EmailField(required=True)
    password=forms.CharField(required=True,min_length=5,error_messages={'min_length':'请输入足够位数的密码'})
    captcha=CaptchaField(error_messages={'invalid':'验证码错误'})

class ForgetPwdForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha=CaptchaField(error_messages={'invalid':'验证码错误'})

class ChangePwdForm(forms.Form):
    '''重置密码'''
    password1 = forms.CharField(required=True, min_length=5,max_length=20)
    password2 = forms.CharField(required=True, min_length=5,max_length=20)
