from django.urls import path
from . import views

app_name = 'navigate'

urlpatterns = [
    # path函数将url映射到视图
    # path('', views.list, name='list'),
    path('', views.IndexView.as_view(), name='index'),
]
