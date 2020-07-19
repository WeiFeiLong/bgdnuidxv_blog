# # coding=utf-8
from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse


#
# from article.models import Article
# from .forms import CommentForm
# # from .models import Comment
#
#
# # 文章评论
# @login_required(login_url='/userprofile/login/')
# def post_comment(request, article_id):
#     article = get_object_or_404(Article, id=article_id)
#
#     # 处理 POST 请求
#     if request.method == 'POST':
#         comment_form = CommentForm(request.POST)
#         if comment_form.is_valid():
#             new_comment = comment_form.save(commit=False)
#             new_comment.article = article
#             new_comment.user = request.user
#
#             # # 二级回复
#             # if parent_comment_id:
#             #     parent_comment = Comment.objects.get(id=parent_comment_id)
#             #     # 若回复层级超过二级，则转换为二级
#             #     new_comment.parent_id = parent_comment.get_root().id
#             #     # 被回复人
#             #     new_comment.reply_to = parent_comment.user
#             #     new_comment.save()
#             #     return HttpResponse('200 OK')
#
#             new_comment.save()
#             return redirect(article)
#         else:
#             return HttpResponse("表单内容有误，请重新填写。")
#
#     # # 处理 GET 请求
#     # elif request.method == 'GET':
#     #     comment_form = CommentForm()
#     #     context = {
#     #         'comment_form': comment_form,
#     #         'article_id': article_id,
#     #         'parent_comment_id': parent_comment_id
#     #     }
#     #     return render(request, 'comment/reply.html', context)
#
#     # 处理错误请求
#     else:
#         return HttpResponse("发表评论仅接受POST请求。")


def ajax_demo(request):
    return render(request, "comment/ajax_demo.html")


def ajax_add(request):  # time.sleep(10)  #不影响页面发送其他的请求
    i1 = int(request.GET.get("i1"))
    i2 = int(request.GET.get("i2"))
    ret = i1 + i2
    return JsonResponse(ret, safe=False)  # JsonResponse在抛出列表的时候需要将safe设置为False