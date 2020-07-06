# coding=utf-8
from django.contrib import admin
from .models import *

admin.site.site_header = '博客后台管理系统'
admin.site.site_title = '博客后台管理'


class ArticleAdmin(admin.ModelAdmin):
    list_per_page = 20  # admin中每页放多少条数据
    list_display = ['id', 'title', 'author', 'createTime', 'modifyTime', 'clickNums', 'category',
                    'isShow', 'allow_comments', 'slug']  # admin中显示的些属性
    search_fields = ['title']  # 搜索框（只有Charfield可以搜索）
    date_hierarchy = 'createTime'  # 详细时间分层筛选　
    filter_horizontal = ('tag',)  # 修改manytomany自带的显示效果
    list_filter = ['category', 'tag']  # 右侧过滤器
    ordering = ('-createTime', 'title')  # ordering设置默认排序字段，负号表示降序排序
    fieldsets = (  # 分组显示
        ("基础信息", {'fields': ['title', 'author', 'category', 'pic', 'clickNums', 'tag', 'isShow', 'allow_comments']}),
        ("文章内容", {'fields': ['content']})
    )


class CategoryAdmin(admin.ModelAdmin):
    list_per_page = 20  # admin中每页放多少条数据
    list_display = ['id', 'cname', 'lifeOrStudy', 'isShow']
    ordering = ('id', 'cname')
    search_fields = ['cname']  # 搜索框（只有Charfield可以搜索）
    list_filter = ['lifeOrStudy']  # 搜索框（只有Charfield可以搜索）


class TagAdmin(admin.ModelAdmin):
    list_per_page = 20  # admin中每页放多少条数据
    list_display = ['id', 'tname', 'isShow']
    ordering = ('id', 'tname')


# class TagAdmin(admin.ModelAdmin):
#    list_per_page = 20  # admin中每页放多少条数据
#    list_display = ['id', 'tname', 'isShow']
#    ordering = ('id', 'tname')


class UseripAdmin(admin.ModelAdmin):
    list_per_page = 20  # admin中每页放多少条数据
    list_display = ['id', 'ip', 'count']
    ordering = ('id', 'count')


class VisitNumberAdmin(admin.ModelAdmin):
    list_display = ['id', 'count']


admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Userip, UseripAdmin)
admin.site.register(VisitNumber, VisitNumberAdmin)
