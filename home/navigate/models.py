from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class DomainPost(models.Model):
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='标题', max_length=100)
    domain = models.CharField(verbose_name='网址', max_length=100)
    pic = models.ImageField(verbose_name='封面图', upload_to='home/%Y%m%d/', default='home/home.jpg')
    body = models.TextField(verbose_name='内容')
    created = models.DateTimeField(verbose_name='创建日期', default=timezone.now)
    updated = models.DateTimeField(verbose_name='更新日期', auto_now=True)
    isShow = models.BooleanField(verbose_name='是否显示', default=True)  # 是否显示

    class Meta:
        ordering = ('-created',)
        verbose_name = '网址导航'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
