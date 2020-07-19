# coding=utf-8
from django.db import models
# from django.contrib.auth.models import User
# from article.models import Article
# from ckeditor_uploader.fields import RichTextUploadingField
# # from mptt.models import MPTTModel, TreeForeignKey
#
#
# from django_comments_xtd.models import XtdComment
#
#
# class MyComment(XtdComment):
#     title = models.CharField(max_length=256)
# # 博文的评论
# class Comment(models.Model):
#     article = models.ForeignKey(
#         Article,
#         on_delete=models.CASCADE,
#         related_name='comments'
#     )  # 被评论的文章
#     user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name='comments'
#     )  # 评论的发布者
#     body = RichTextUploadingField()
#     created = models.DateTimeField(auto_now_add=True)
#
#     # # 新增，mptt树形结构
#     # parent = TreeForeignKey(
#     #     'self',
#     #     on_delete=models.CASCADE,
#     #     null=True,
#     #     blank=True,
#     #     related_name='children'
#     # )
#     #
#     # # 新增，记录二级评论回复给谁, str
#     # reply_to = models.ForeignKey(
#     #     User,
#     #     null=True,
#     #     blank=True,
#     #     on_delete=models.CASCADE,
#     #     related_name='replyers'
#     # )
#
#     class Meta:
#         ordering = ('created',)
#
#     # class MPTTMeta:
#     #     order_insertion_by = ['created']
#
#     def __str__(self):
#         return self.body[:20]
