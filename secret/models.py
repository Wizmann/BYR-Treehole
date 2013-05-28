# coding=utf-8
from django.db import models
from django.contrib.auth.models import User


class Secret(models.Model):
    author = models.ForeignKey(User, null=True, blank=True)
    c_time = models.DateTimeField(auto_now_add=True)
    rank_val = models.BigIntegerField(default=0)  # 热度
    star = models.IntegerField(default=0)
    content = models.TextField()

    # 不要过早优化？
    # 这三个bool值明明可以存在一个IntegerField里嘛～
    is_public = models.BooleanField()
    is_banned = models.BooleanField(default=False)
    is_hot = models.BooleanField(default=False)

    #点亮秘密的用户 
    stared_user = models.ManyToManyField(User, related_name="by_star", null=True, blank=True)
    #不喜欢这个秘密的用户
    unlike_user = models.ManyToManyField(User, related_name="by_unlike", null=True, blank=True)
    #审核过这个秘密的用户
    preview_user = models.ManyToManyField(User, related_name="by_preview", null=True, blank=True)


    def __unicode__(self):
        return "#%d[%s]%s" % (self.id, self.author, self.content)
    
    def save(self):
        if self.rank_val == 0:
            self.rank_val += 15000
        print 'add init'
        super(Secret, self).save()

    class Meta:
        verbose_name_plural = "秘密"
