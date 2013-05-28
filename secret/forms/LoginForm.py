#coding=utf-8
from django import forms
from captcha.fields import CaptchaField
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    captcha = CaptchaField()
