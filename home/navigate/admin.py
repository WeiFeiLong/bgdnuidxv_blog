from django.contrib import admin

# Register your models here.
from .models import DomainPost

admin.site.site_header = '小眼记站点地图后台管理系统'
admin.site.site_title = '小眼记站点地图后台管理'


class DomainPostAdmin(admin.ModelAdmin):
    list_per_page = 10  # admin中每页放多少条数据
    list_display = ['id', 'title', 'author', 'domain', 'created', 'updated', 'isShow']  # admin中显示的些属性
    search_fields = ['title']  # 搜索框（只有Charfield可以搜索）
    date_hierarchy = 'created'  # 详细时间分层筛选　
    ordering = ('-created', 'title')  # ordering设置默认排序字段，负号表示降序排序
    fieldsets = (  # 分组显示
        ("基础信息", {'fields': ['title', 'author', 'domain', 'pic', 'isShow', 'created']}),
        ("文章内容", {'fields': ['body']})
    )


admin.site.register(DomainPost, DomainPostAdmin)
