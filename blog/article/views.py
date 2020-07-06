# coding=utf-8
import json
import re
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, render_to_response
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page  # 缓存
from .visit_info import change_info  # 当网站被访问时，更新网站访问次数

from django.views import generic
from django.urls import reverse
from django.views import View


# @cache_page(60 * 60)  # 设置为了永久缓存，当首页修改时需要删除缓存,None
# def index(request):
#     #    change_info(request)     #当网站被访问时，更新网站访问次数
#     return render(request, 'article/index.html')


class IndexView(generic.ListView):
    model = Article  # 不要就出错
    template_name = 'article/index.html'
    context_object_name = 'articles'


# 点击下一页时使用ajax局部刷新页面内容 index.html
@csrf_exempt  # 取消当前函数防跨站请求伪造功能，即便settings中设置了全局中间件。
def page1Ajax(request):
    if request.method == 'GET':
        page_id = request.GET.get('page_id')
        article = Article.objects.filter(isShow=True).order_by('-id')  # 获取所有博客
        paginator = Paginator(article, 4)  # 分页，每页显示4篇文章
        page_list = paginator.page(int(page_id)).object_list  # 获得要返回的页面的文章列表

        # 处理要返回的数据
        result = []
        array = []
        for p in page_list:
            time = p.createTime.strftime('%Y-%m-%d')  # 年月日
            time1 = p.createTime.strftime('%H:%M:%S')  # 时分秒
            array.append(time)  # 年月日数组
            array.append(time1)  # 时分秒数组
            array.append(p.title)  # 标题数组
            array.append(str(p.pic))
            temp = p.content
            dr = re.compile(r'<[^>]+>', re.S)
            temp = dr.sub('', temp).replace('\n', "").replace(' ', '')
            array.append(temp[0:95])
            array.append(p.id)  # 文章的id的数组
            array.append(p.slug)  # 文章的slug

            array.append(time[0:4])  # 年
            array.append(time[5:7])  # 月
            array.append(time[8:10])  # 日
            array.append(p.category.lifeOrStudy)  # 文章的类别总分类
            result.append(array)
            array = []
        context = {  # 字典类型
            'result': result,
            'page_id': page_id,  # 当前页面
            'num_pages': paginator.num_pages,  # 页面总数
        }
        return HttpResponse(json.dumps(context))  # json.dumps(context)是字符串类型


# 点击下一页时使用ajax局部刷新页面内容 life.html
@csrf_exempt  # 取消当前函数防跨站请求伪造功能，即便settings中设置了全局中间件。
def page2Ajax(request):
    if request.method == 'GET':
        page_id = request.GET.get('page_id')
        article = Article.objects.filter(isShow=True, category__lifeOrStudy='慢生活').order_by('-id')  # 获取’慢生活‘博客标题
        paginator = Paginator(article, 4)  # 分页，每页显示4篇文章
        page_list = paginator.page(int(page_id)).object_list  # 获得要返回的页面的文章列表

        # 处理要返回的数据
        result = []
        array = []
        for p in page_list:
            time = p.createTime.strftime('%Y-%m-%d')  # 年月日
            time1 = p.createTime.strftime('%H:%M:%S')  # 时分秒
            array.append(time)  # 年月日数组
            array.append(time1)  # 时分秒数组
            array.append(p.title)  # 标题数组
            array.append(str(p.pic))
            temp = p.content
            dr = re.compile(r'<[^>]+>', re.S)
            temp = dr.sub('', temp).replace('\n', "").replace(' ', '')
            array.append(temp[0:95])
            array.append(p.id)  # 文章的id的数组
            array.append(p.slug)  # 文章的slug

            array.append(time[0:4])  # 年
            array.append(time[5:7])  # 月
            array.append(time[8:10])  # 日
            array.append(p.category.lifeOrStudy)  # 文章的类别总分类
            result.append(array)
            array = []
        context = {  # 字典类型
            'result': result,
            'page_id': page_id,  # 当前页面
            'num_pages': paginator.num_pages,  # 页面总数
        }
        return HttpResponse(json.dumps(context))  # json.dumps(context)是字符串类型


class ArticleDetailView(generic.DateDetailView):  # 评论成功后，跳转的detail页面
    model = Article
    date_field = "createTime"
    month_format = "%m"

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        context.update({'next': reverse('comments-xtd-sent')})
        return context


class DetailView(generic.DetailView):  # 文章显示的detail页面
    model = Article  # 获取数据库中的文章列表
    template_name = 'article/detail.html'  # 渲染的网页路径
    context_object_name = 'article'  # 项目urls下的子路由名称

    def get_object(self):  # 获得文章，并处理
        obj = super(DetailView, self).get_object()
        obj.clickNums = obj.clickNums + 1  # 增加访问次数
        obj.save()

        return obj

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['category'] = self.object.id
        return context


# @cache_page(60 * 0.1)  # 设置为了永久缓存，当首页修改时需要删除缓存,None
# def detail(request, id):
#     #    change_info(request)     #当网站被访问时，更新网站访问次数
#     article = Article.objects.get(id=int(id))  # 获取某一篇文章，文章标题
#     article.clickNums = article.clickNums + 1  # 增加访问次数
#     article.save()
#     time = article.createTime.strftime('%Y-%m-%d')  # 年月日
#     time1 = article.createTime.strftime('%H:%M:%S')  # 时分秒
#     meta_category = article.category  # 文章类别
#     meta_description = re.sub(r'<[^>]+>', "", article.content, re.S)[:80]  # 去掉html标签，并截取前80个字符,文章内容
#     # comments = Comment.objects.filter(article=id)  # 取出多个满足条件的对象
#     # comment_form = CommentForm()
#     context = {
#         'article': article,  # 文章标题
#         'meta_description': meta_description,  # 文章简介
#         'article.content': article.content,  # 文章内容
#         'meta_category': meta_category,  # 文章类别
#         'id': id,  # 文章id
#         'time': time,  # 年月日
#         'time1': time1,  # 时分秒
#         # 'comments': comments,
#         # 'comment_form': comment_form,
#     }
#     return render(request, 'article/detail.html', context)


# @cache_page(60 * 60)  # 设置为了永久缓存，当首页修改时需要删除缓存,None
def chartInfo(request):  # 饼图ajax请求数据
    if request.GET.get('name'):  # 加载二级图表
        name = request.GET.get('name')
        t1 = Category.objects.get(id=1)
        CategoryList = Category.objects.filter(lifeOrStudy=name).order_by('id')  # 获取类别
        list1 = []
        result = []
        for t in CategoryList:
            count = t.article_set.all().count()
            list1.append(count)
            list1.append(t.cname)
            list1.append(t.id)
            result.append(list1)
            list1 = []
        context = {'result': result, 'name': name, }
        return HttpResponse(json.dumps(context))
    else:  # 加载一级图表
        lifeList = Category.objects.filter(lifeOrStudy='慢生活')
        lifeCount = 0
        for t in lifeList:
            count = t.article_set.all().count()
            lifeCount += count

        studyList = Category.objects.filter(lifeOrStudy='学无止境')
        studyCount = 0
        for t in studyList:
            count = t.article_set.all().count()
            studyCount += count

        context = {
            'lifeCount': lifeCount,
            'studyCount': studyCount
        }
        print(context)
        return HttpResponse(json.dumps(context))


# @cache_page(60 * 60)  # 设置为了永久缓存，当首页修改时需要删除缓存,None
def about(request):
    # change_info(request)  # 当网站被访问时，更新网站访问次数
    return render(request, 'article/about.html')


# @cache_page(60 * 60)  # 设置为了永久缓存，当首页修改时需要删除缓存,None
def learn(request, category_id, page_id):
    # change_info(request)  # 当网站被访问时，更新网站访问次数
    category_id = int(category_id)
    page_id = int(page_id)
    if category_id == 0:
        article = Article.objects.filter(isShow=True, category__lifeOrStudy='学无止境').order_by('-id')
    else:
        category = Category.objects.get(id=category_id)
        article = Article.objects.filter(category=category, isShow=True, category__lifeOrStudy='学无止境').order_by('-id')
    category_learn_list = Category.objects.filter(lifeOrStudy='学无止境')

    paginator = Paginator(article, 4)  # 分页，每页显示4篇文章
    page_list = paginator.page(page_id).object_list  # 获得要返回的页面的文章列表

    # 处理要返回的数据
    result = []
    array = []
    for p in page_list:
        time = p.createTime.strftime('%Y-%m-%d')  # 年月日
        time1 = p.createTime.strftime('%H:%M:%S')  # 时分秒
        array.append(time)  # .append函数是将数据累加在原列表中，文章大时间
        array.append(time1)  # 文章小时间
        array.append(p.title)  # 文章标题
        array.append(str(p.pic))  # 文章图片
        temp = p.content
        dr = re.compile(r'<[^>]+>', re.S)
        temp = dr.sub('', temp).replace('\n', "").replace(' ', '')
        array.append(temp[0:130])  # 文章内容取前130字放在
        array.append(p.id)  # 文章的id
        array.append(p.slug)  # 文章的slug

        array.append(time[0:4])  # 年
        array.append(time[5:7])  # 月
        array.append(time[8:10])  # 日
        array.append(p.category.lifeOrStudy)  # 文章的类别总分类

        result.append(array)
        array = []  # 循环后的结果是，所有的文章以数组单元的形式放置在result中，result=[[],[],[],[]]
    context = {  # 字典类型
        'result': result,
        'page_id': page_id,  # 页面码
        'num_pages': paginator.num_pages,  # 页面总数
        'category_id': category_id,  # 类别对应对的id
        'page_list': page_list,
        'array': array,
        'category_learn_list': category_learn_list,
    }
    return render(request, 'article/learn.html', context)


# @cache_page(60 * 60)  # 设置为了永久缓存，当首页修改时需要删除缓存,None
def life(request, category_id, page_id):
    #    change_info(request)     #当网站被访问时，更新网站访问次数
    category_id = int(category_id)
    page_id = int(page_id)
    if category_id == 0:
        article = Article.objects.filter(isShow=True, category__lifeOrStudy='慢生活').order_by('-id')
    else:
        category = Category.objects.get(id=category_id)
        article = Article.objects.filter(category=category, isShow=True, category__lifeOrStudy='慢生活').order_by('-id')
    category_life_list = Category.objects.filter(lifeOrStudy='慢生活')

    paginator = Paginator(article, 4)  # 分页，每页显示4篇文章
    page_list = paginator.page(page_id).object_list  # 获得要返回的页面的文章列表

    # 处理要返回的数据
    result = []
    array = []
    for p in page_list:
        time = p.createTime.strftime('%Y-%m-%d')  # 年月日
        time1 = p.createTime.strftime('%H:%M:%S')  # 时分秒
        array.append(time)  # .append函数是将数据累加在原列表中，文章大时间
        array.append(time1)  # 文章小时间
        array.append(p.title)  # 文章标题
        array.append(str(p.pic))  # 文章图片
        temp = p.content
        dr = re.compile(r'<[^>]+>', re.S)
        temp = dr.sub('', temp).replace('\n', "").replace(' ', '')
        array.append(temp[0:130])  # 文章内容取前130字放在
        array.append(p.id)  # 文章的id
        array.append(p.slug)  # 文章的slug

        array.append(time[0:4])  # 年
        array.append(time[5:7])  # 月
        array.append(time[8:10])  # 日
        array.append(p.category.lifeOrStudy)  # 文章的类别总分类

        result.append(array)
        array = []  # 循环后的结果是，所有的文章以数组单元的形式放置在result中，result=[[],[],[],[]]
    context = {  # 字典类型
        'result': result,
        'page_id': page_id,  # 页面码
        'num_pages': paginator.num_pages,  # 页面总数
        'category_id': category_id,  # 类别对应对的id
        'page_list': page_list,
        'array': array,
        'category_life_list': category_life_list,
    }
    return render(request, 'article/life.html', context)


# # @cache_page(60 * 60)  # 设置为了永久缓存，当首页修改时需要删除缓存,None
# def slowlife(request):
#     # change_info(request)  # 当网站被访问时，更新网站访问次数
#     return render(request, 'article/slowlife.html')


# @cache_page(60 * 60)  # 设置为了永久缓存，当首页修改时需要删除缓存,None
def liuyan(request):
    # change_info(request)  # 当网站被访问时，更新网站访问次数
    return render(request, 'article/liuyan.html')


# 404界面
def page_not_found(request):
    # change_info(request)  # 当网站被访问时，更新网站访问次数
    return render_to_response('404.html')


# sitemap
def sitemap(request):
    return render(request, 'sitemap.xml', content_type="application/xml")

# # 点赞数 +1
# class IncreaseLikesView(View):
#     def post(self, request, *args, **kwargs):
#         article = ArticlePost.objects.get(id=kwargs.get('id'))
#         article.likes += 1
#         article.save()
#         return HttpResponse('success')
