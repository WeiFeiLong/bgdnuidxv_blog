# coding=utf-8
# from django import forms
# from .models import Comment
#
#
# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields = ['body']   # models中2个外键将通过视图逻辑自动填写

# from django.utils.translation import ugettext_lazy as _
#
# from django_comments_xtd.forms import XtdCommentForm
# from django_comments_xtd.models import TmpXtdComment
#
#
# class MyCommentForm(XtdCommentForm):
#     title = forms.CharField(
#         max_length=256,
#         widget=forms.TextInput(attrs={'placeholder': _('title')})
#     )
#
#     def get_comment_create_data(self):
#         data = super(MyCommentForm, self).get_comment_create_data()
#         data.update({'title': self.cleaned_data['title']})
#         return data