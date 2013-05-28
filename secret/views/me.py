# coding=utf-8
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from django.shortcuts import render_to_response
from django.template import RequestContext

from secret.models import Secret

def me(request):
    if request.method == "GET":
        if not request.user.is_authenticated():
            return HttpResponseRedirect("/secret/")
        try:
            page = int(request.GET.get("page", 0))
        except:
            print 'page = ', page
            page = 0 
        secret_list = Secret.objects\
                            .filter(author=request.user)\
                            .order_by("-c_time")[page*20:page*20+20]

        url = '/secret/me?'
        for item in secret_list:
            item.mark = min(100, (item.rank_val-15000)/1000)
        if page - 1 >= 0:
            pre_page_url = url + ('page=%d' % (page-1))
        else:
            pre_page_url = url
        next_page_url = url + ('page=%d' % (page+1))

        return render_to_response(
            'secret/me.html',
            {'secret_list': secret_list,
             'title': '我的秘密',
             'pre_page_url': pre_page_url,
             'next_page_url': next_page_url,
             'css_files': ['/static/css/star.css']},
            context_instance=(RequestContext(request)))
    else:
        raise Http404
