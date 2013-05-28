from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from secret.forms import SecretForm
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt

def home(request):
    return HttpResponseRedirect("/secret/")

