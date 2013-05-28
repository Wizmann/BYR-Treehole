from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from secret.forms import SecretForm
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def home(request):
    if request.method == 'POST':
        form = SecretForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/secret/profile/?q=new&action=new")
        else:
            return render_to_response(
                'secret/home.html',
                {'secret_form': form},
                context_instance=(RequestContext(request)))

    else:
        form = SecretForm(request.user)
        return render_to_response(
            'secret/home.html',
            {"secret_form": form},
            context_instance=(RequestContext(request)))

