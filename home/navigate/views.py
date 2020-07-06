from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse
from django.views import generic
from .models import DomainPost


class IndexView(generic.ListView):
    model = DomainPost
    template_name = 'navigate/index.html'
    context_object_name = 'homes'

    # def get_queryset(self):
    #     """
    #     可查询集
    #     """
    #     queryset = DomainPost.objects.all()
    #     return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        homes = DomainPost.objects.filter(isShow=True).order_by('id')
        # 处理要返回的数据
        result = []
        array = []
        for p in homes:
            time = p.created.strftime('%Y-%m-%d')  # 年月日
            time1 = p.created.strftime('%H:%M:%S')  # 时分秒
            array.append(time)  # .append函数是将数据累加在原列表中，文章大时间
            array.append(time1)  # 文章小时间
            array.append(p.title)  # 文章标题
            array.append(p.domain)  # 文章的domain
            array.append(str(p.pic))  # 文章图片
            array.append(p.body)  # 文章的body
            array.append(time[0:4])  # 年
            array.append(time[5:7])  # 月
            array.append(time[8:10])  # 日
            result.append(array)
            array = []  # 循环后的结果是，所有的文章以数组单元的形式放置在result中，result=[[],[],[],[]]
        context['result'] = result
        return context
