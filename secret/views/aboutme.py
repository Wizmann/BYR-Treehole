# coding=utf-8
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from django.shortcuts import render_to_response
from django.template import RequestContext

def aboutme(request):
    return render_to_response("secret/aboutme.html",
        context_instance=(RequestContext(request)))
