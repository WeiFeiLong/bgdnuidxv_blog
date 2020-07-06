# coding=utf-8
from django.db import models
from django.contrib.auth.models import User
# 引入内置信号
from django.db.models.signals import post_save
# 引入信号接收器的装饰器
from django.dispatch import receiver


# 用户扩展信息
class Profile(models.Model):
    # 与 User 模型构成一对一的关系
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # 电话号码字段
    phone = models.CharField(max_length=20, blank=True)
    # 头像
    avatar = models.ImageField(upload_to='avatar/%Y%m%d/', blank=True)
    # 个人简介
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return 'user {}'.format(self.user.username)

# 本章中用到了信号来实现User和Profile的同步创建，但是也产生了一个BUG：在后台中创建User时如果填写了Profile任何内容，则系统报错且保存不成功；其他情况下均正常。
# BUG产生原因：在后台中创建并保存User时调用了信号接收函数，创建了Profile表；但如果此时管理员填写了内联的Profile表，会导致此表也会被创建并保存。最终结果就是同时创建了两个具有相同User的Profile表，违背了”一对一“外键的原则。
# 解决的办法也不难。因为博客项目的需求较简单，其实没有必要用到信号。
# 修改model，把两个信号接收函数去除：
# # 信号接收函数，每当新建 User 实例时自动调用
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#
#
# # 信号接收函数，每当更新 User 实例时自动调用
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()