# coding=utf-8
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views
from . import search_views

from article.models import Article
from article.views import ArticleDetailView, DetailView
from django.views.generic import DateDetailView

app_name = 'article'  # Django2.0之后，app的urls.py必须配置app_name，否则会报错
urlpatterns = [
    # path('', views.index, name='index'),  # url(r'^$', views.index, name='index'),

    path('', views.IndexView.as_view(), name='index'),
    path('page1Ajax', views.page1Ajax, name='page1Ajax'),  # url(r'^pageAjax$', views.pageAjax, name='pageAjax'),
    path('page2Ajax', views.page2Ajax, name='page2Ajax'),
    # path('detail/<int:id>/', views.detail, name='detail'), (?P<slug>.*?) <int:pk>
    # 文章详情页面
    # url(r'^detail/(?P<slug>.*?)/$', ArticleDetailView.as_view(),
    #     name='article-detail'),
    # path('detail/<int:pk>/', DetailView.as_view(), name='detail'),
    # url((r'^detail/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/'
    #      r'(?P<slug>[-\w]+)/$'),
    #     DetailView.as_view(), name='detail'),
    path('detail/<int:year>/<int:month>/<int:day>/<slug:slug>/', DetailView.as_view(), name='detail'),

    path('chartInfo', views.chartInfo, name='chartInfo'),  # url(r'^chartInfo$', views.chartInfo, name='chartInfo'),
    path('about/', views.about, name='about'),  # url(r'^about/$', views.about, name='about'),
    url(r'^learn/(\d+)/(\d+)/$', views.learn, name='learn'),
    url(r'^life/(\d+)/(\d+)/$', views.life, name='life'),
    # path('slowlife/', views.slowlife, name='slowlife'),  # url(r'^slowlife/$', views.slowlife, name='slowlife'),
    path('liuyan/', views.liuyan, name='liuyan'),  # url(r'^liuyan/$', views.liuyan, name='liuyan'),
    path('search/', search_views.MySeachView(), name='haystack_search'),
    url(r'^sitemap\.xml$', views.sitemap, name='sitemap'),

    # re_path(r'^(?P<pk>[0-9]+)/$', views.ArticleDetailView.as_view(), name='detail'),
    # re_path(r'^(?P<article_id>[0-9]+)/comment/$', ArticleCommentView.as_view(), name='article_comment'),

    # # 文章详情页面
    # url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$', ArticleDetailView.as_view(),
    #     name='article-detail'),
    # url((r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/'
    #      r'(?P<slug>[-\w]+)/$'),
    #     ArticleDetailView.as_view(),
    #     name='article-detail'),
    # 点赞 +1
    # path('increase-likes/<int:id>/', views.IncreaseLikesView.as_view(), name='increase_likes'),

]
