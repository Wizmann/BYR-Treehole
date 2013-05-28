# coding=utf-8
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Count, Q

from secret.models import Secret


@csrf_exempt
def preview(request):
    if request.method == 'POST':
        idx = request.POST.get('idx', None)
        ptype = request.POST.get('ptype', None).strip()
        if idx and ptype in ('awesome','good','bad'):
            secret = Secret.objects.get(id=idx)
            print secret
            if not secret.preview_user.filter(username=request.user):
                if ptype == 'awesome':
                    secret.rank_val += 2000
                elif ptype == 'good':
                    secret.rank_val += 1000
                elif ptype == 'bad':
                    secret.rank_val -= 500
                secret.preview_user.add(request.user)
                secret.save() 
                return HttpResponse('true')
        return HttpResponseBadRequest()
    elif request.method == 'GET':
        try:
            secret = Secret.objects \
                           .filter(is_public=True)\
                           .filter(is_banned=False)\
                           .annotate(cc=Count('stared_user'))\
                           .filter(rank_val__lt=19000)\
                           .exclude(preview_user=request.user)\
                           .order_by('?')[0]
            #19是一个奇妙的数字～
        except:
            import traceback
            traceback.print_exc()
            secret = 'None'
        return render_to_response(
            'secret/preview.html',
            {'title': '审核新秘密',
             'secret': secret,
             'css_files':['/static/css/preview.css'],
             'js_files': ['/static/js/secret/preview.js']},
            context_instance=(RequestContext(request)))
    else:
        raise Http404
