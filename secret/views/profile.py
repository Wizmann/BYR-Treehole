# coding=utf-8
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Count

from secret.models import Secret


@csrf_exempt
def profile(request):
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        is_ant = request.user.groups.filter(name='ant')
        q = request.GET.get('q', 'new')
        action = request.GET.get('action', None)
        try:
            page = request.GET.get('page', 0)
            page = int(page)
        except:
            page = 0

        secret_list = Secret.objects.filter(rank_val__gt=19000)\
                                    .filter(is_banned=False, is_public=True)

        if q == 'hot':
            secret_list = secret_list.order_by('-rank_val','-c_time')[page*20:page*20+20]
            title = '秘密 - 最热'
        else:
            q = 'new'
            secret_list = secret_list.order_by("-c_time")[page*20:page*20+20]
            title = '秘密 - 最新'

        for secret in secret_list:
            star_users = secret.stared_user.all()
            secret.status = "on" if request.user in star_users else "off"
            secret.star = len(star_users)

        url = '/secret/profile?q=%s&' % q
        if page - 1 >= 0:
            pre_page_url = url + ('page=%d' % (page-1))
        else:
            pre_page_url = url

        next_page_url = url + ('page=%d' % (page+1))

        return render_to_response(
            'secret/profile.html',
            {'secret_list': secret_list,
             'title' : title,
             'is_ant': is_ant,
             'action': action,
             'pre_page_url': pre_page_url,
             'next_page_url': next_page_url,
             'css_files': ['/static/css/star.css'],
             'js_files': ['/static/js/secret/star.js',
                          '/static/js/secret/profile.js']},
            context_instance=(RequestContext(request)))
    else:
        raise Http404
