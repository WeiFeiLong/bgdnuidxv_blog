# coding=utf-8
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

from django_comments_xtd.moderation import moderator, XtdCommentModerator
from article.badwords import badwords  # 敏感词

import random


# 文章类别
class Category(models.Model):
    cname = models.CharField(verbose_name='类别名字', unique=True, max_length=20)
    isShow = models.BooleanField(verbose_name='是否显示', default=True)  # 是否显示，默认显示
    objects = models.Manager()  # 数据库查询接口，默认objects，可修改 可不要
    lifeOrStudy_CHOICES = (
        ('学无止境', '学无止境'),
        ('慢生活', '慢生活'),  # 第一个参数是真正的model参数，#第二个参数则是方便人们理解阅读
    )
    lifeOrStudy = models.CharField(verbose_name='所属总分类', max_length=10, choices=lifeOrStudy_CHOICES, default='学无止境')

    class Meta:
        verbose_name = '文章类别'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.cname


# 文章标签
class Tag(models.Model):
    tname = models.CharField(verbose_name='标签', unique=True, max_length=30)  # 标签名字
    isShow = models.BooleanField(verbose_name='是否显示', default=True)  # 是否显示，默认显示
    objects = models.Manager()  # 数据库查询接口，默认objects，可修改 可不要

    class Meta:
        verbose_name = '文章标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.tname


class PublicManager(models.Manager):  # 添加额外的manager
    def published(self):
        return self.get_queryset().filter(createTime__lte=timezone.now())


# 博客文章
class Article(models.Model):
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='标题', unique=True, max_length=30)  # 标题
    # slug = models.SlugField(max_length=140, unique=True, unique_for_date="createTime")
    # slug = models.SlugField(unique=True)
    slug = models.SlugField('唯一码字', max_length=200, db_index=True, unique=True, default='3')
    content = RichTextUploadingField(verbose_name='正文', default='', config_name='wight')
    createTime = models.DateTimeField(verbose_name='创建时间',  default=timezone.now)
    # 可以暂时先用，default=timezone.now auto_now_add=True,
    modifyTime = models.DateTimeField(verbose_name='上次修改时间', auto_now=True)  # auto_now=True，在你修改时，会自动变成当前时间。
    clickNums = models.IntegerField(verbose_name='点击量', default=0)  # 点击量，默认从0开始
    pic = models.ImageField(verbose_name='博客封面图片', upload_to='pic_img', default='pic_img/book.jpg')
    tag = models.ManyToManyField(Tag, verbose_name='文章标签')  # 多对多关系
    category = models.ForeignKey(Category, verbose_name='文章类别', on_delete=models.CASCADE)  # 外键
    isShow = models.BooleanField(verbose_name='是否显示', default=True)  # 是否显示
    allow_comments = models.BooleanField('允许评论', default=True)
    # likes = models.PositiveIntegerField('点赞', default=0)

    objects = PublicManager()

    class Meta:
        verbose_name = '我的博客'
        verbose_name_plural = verbose_name
        ordering = ('-createTime',)  # ordering是元组，括号中只含一个元素时不要忘记末尾的逗号

    def __str__(self):
        return self.title[:20]

    def save(self, *args, **kwargs):
        if int(self.slug) <= 3:
            slug = (random.randint(100000, 999999))
            self.slug = str(slug)
        super(Article, self).save(*args, **kwargs)  # 一定要放置在if 后面，不然文章修改无效

    def get_absolute_url(self):
        return reverse(
            'article:detail',
            kwargs={
                'year': self.createTime.year,
                'month': int(self.createTime.strftime('%m').lower()),
                'day': self.createTime.day,
                'slug': self.slug})


# 访问网站的ip地址和次数
class Userip(models.Model):
    ip = models.CharField(verbose_name='IP地址', max_length=30)  # ip地址
    count = models.IntegerField(verbose_name='访问次数', default=0)  # 该ip访问次数
    objects = models.Manager()  # 数据库查询接口，默认objects，可修改 可不要

    class Meta:
        verbose_name = '访问用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.ip


# 网站总访问次数
class VisitNumber(models.Model):
    count = models.IntegerField(verbose_name='网站访问总次数', default=0)  # 网站访问总次数
    objects = models.Manager()  # 数据库查询接口，默认objects，可修改 可不要

    class Meta:
        verbose_name = '网站访问总次数'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.count)


#  评论审核，嵌套评论通知
class PostCommentModerator(XtdCommentModerator):
    removal_suggestion_notification = True  # 删除评论是否通知各位
    email_notification = True
    auto_moderate_field = 'createTime'
    moderate_after = 3650  # 天数

    def moderate(self, comment, content_object, request):  # 敏感词
        # Make a dictionary where the keys are the words of the message and
        # the values are their relative position in the message.
        def clean(word):
            ret = word
            if word.startswith('.') or word.startswith(','):
                ret = word[1:]
            if word.endswith('.') or word.endswith(','):
                ret = word[:-1]
            return ret

        lowcase_comment = comment.comment.lower()
        msg = dict([(clean(w), i)
                    for i, w in enumerate(lowcase_comment.split())])
        for badword in badwords:
            if isinstance(badword, str):
                if lowcase_comment.find(badword) > -1:
                    return True
            else:
                lastindex = -1
                for subword in badword:
                    if subword in msg:
                        if lastindex > -1:
                            if msg[subword] == (lastindex + 1):
                                lastindex = msg[subword]
                        else:
                            lastindex = msg[subword]
                    else:
                        break
                if msg.get(badword[-1]) and msg[badword[-1]] == lastindex:
                    return True
        return super(PostCommentModerator, self).moderate(comment,
                                                          content_object,
                                                          request)


moderator.register(Article, PostCommentModerator)
