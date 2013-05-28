# coding=utf-8
from django.http import HttpResponse, HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import F, Q, Max, Count

import json
import datetime
import math
from secret.models import Secret


@csrf_exempt
def secret_ban(request):
    if request.method == 'POST':
        is_ant = request.user.groups.filter(name='ant')
        print is_ant
        try:
            idx = int(request.POST.get('sid', None))
        except:
            idx = None
        print is_ant,idx
        if not is_ant or not idx:
            raise Http404
        else:
            secret = Secret.objects.filter(id=idx).update(is_banned=True)
            return HttpResponse("ok")
    else:
        raise Http404
            
@csrf_exempt
def starlight(request):
    if request.method == 'POST':
        idx = request.POST.get("sid", None)
        cmd = request.POST.get("cmd", None)

        if not request.user.is_authenticated():
            return HttpResponse(json.dumps({"status":"false","info":"请先登录"}))

        if idx and cmd in ('on','off','dislike'):
            s = Secret.objects.get(id=idx)
            if cmd == 'on':
                if not s.stared_user.filter(username=request.user):
                    s.stared_user.add(request.user)
                    s.star += 1
                    s.rank_val += 1000
                    s.save()
            elif cmd == 'off':
                if s.stared_user.filter(username=request.user):
                    s.stared_user.remove(request.user)
                    s.star -= 1000
                    s.rank_val -= 1000
                    s.save()
            else:
                if s.unlike_user.filter(username=request.user):
                    s.unlike_user.add(request.user)
                    s.rank_val -= 1000
                    s.save()
            return HttpResponse("true")
        else: return HttpResponseBadRequest()


    else:
        raise Http404

@csrf_exempt
def get_preview_num(request):
    if request.method == 'POST':
        if not request.user.is_authenticated():
            return HttpResponse("")
        else:
            preview_num = Secret.objects \
                           .filter(is_public=True)\
                           .filter(is_banned=False)\
                           .annotate(cc=Count('stared_user'))\
                           .filter(rank_val__lt=19000)\
                           .exclude(preview_user=request.user).count()
            print preview_num
            return HttpResponse(str(preview_num))
    else:
        raise Http404

@csrf_exempt
def cool_down(request):
    if request.method == 'GET':
        pin = request.GET.get("pin", None)

        # I don't like that, too evil...
        if pin != "******************":
            return HttpResponseBadRequest()
        else:
            from django.db import connection
            cursor = connection.cursor()
            cursor.execute(
                '''
                UPDATE 
                    `secret_secret` 
                SET 
                    `rank_val` = 
                        IF(`secret_secret`.`rank_val` * 0.959189457109138 > 19000,
                           `secret_secret`.`rank_val` * 0.959189457109138, 19001)
                WHERE 
                    `secret_secret`.`rank_val` > 19000 
                ''')
            from django.db import transaction
            transaction.commit_unless_managed()

            preview_secrets = Secret.objects\
                                    .filter(~Q(rank_val__gt=19000))\
                                    .filter(~Q(c_time__gt=datetime.datetime.now()-datetime.timedelta(days=19)))\
                                    .delete()
            return HttpResponse("true")
    else:
        return HttpResponseBadRequest()
