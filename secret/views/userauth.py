# coding=utf-8
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from django import forms
from django.shortcuts import render_to_response
from django.template import RequestContext
from secret.forms import LoginForm, RegisterForm


@csrf_exempt
def login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            auth.login(request, form.get_user())
            return HttpResponseRedirect("/secret/")
        else:
            return render_to_response(
                'secret/login.html',
                {'auth_form': form, },
                context_instance=(RequestContext(request)))
    else:
        form = LoginForm()
        return render_to_response(
            'secret/login.html',
            {'auth_form': form,},
            context_instance=(RequestContext(request)))


@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/secret/login/")
        else:
            return render_to_response(
                'secret/register.html',
                {'auth_form': form},
                context_instance=(RequestContext(request)))

    else:
        form = RegisterForm()
        return render_to_response(
            'secret/register.html',
            {'auth_form': form},
            context_instance=(RequestContext(request)))


@csrf_exempt
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/secret/")
