# coding = utf - 8
from django.urls import path
from django.conf.urls import url, include
from . import views

app_name = 'comment'

urlpatterns = [
    # 发表评论
    # path('post-comment/<int:article_id>/', views.post_comment, name='post_comment'),
    # # 新增代码，处理二级回复
    # path('post-comment/<int:article_id>/<int:parent_comment_id>', views.post_comment, name='comment_reply')
    url(r'^ajax_add/', views.ajax_add),
    url(r'^ajax_demo/', views.ajax_demo),
]
