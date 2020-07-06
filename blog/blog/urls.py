# coding=utf-8
"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.views.i18n import JavaScriptCatalog

from django.views.static import serve

urlpatterns = [
                  path('admin/', admin.site.urls),
                  # 新增代码，配置app的url
                  path('', include('article.urls', namespace='article')),
                  # namespace可以保证反查到唯一的url，即使不同的app使用了相同的url（后面会用到）。
                  # path('comment/', include('comment.urls', namespace='comment')),  # app2
                  path('userprofile/', include('userprofile.urls', namespace='userprofile')),  # 用户管理,app3
                  path('password-reset/', include('password_reset.urls')),  # 重置密码
                  path('search/', include('haystack.urls')),  # url(r'^search/', include('haystack.urls')),
                  path('ckeditor/', include('ckeditor_uploader.urls')),  # 有APP的才加namespace=''

                  url(r'^comments/', include('django_comments_xtd.urls')),
                  # path('comments/', include('django_comments_xtd.urls')),
                  path(r'jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
                  url(r'^drive/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),
                  url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}, name='media'),
                  # 防止setting.py中的DEBUG=F后无法加载静态文件的问题
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
