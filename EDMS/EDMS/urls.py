"""EDMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, re_path
# from django.conf.urls import url
# from django.views.generic import TemplateView
from EDMS_backend.views import index, expert_list, expert_detail, paper_detail, login, edit_info, change_pwd, logout,\
    user_center, add_fav, del_fav, check_login, paper_list

urlpatterns = [
    path('admin/', admin.site.urls),
    # url(r'', TemplateView.as_view(template_name='index.html')),
    path('', index, name='index'),
    # path('/', index, name='index'),
    re_path('^$', index, name='index'),
    re_path('^expert_list', expert_list, name='expert_list'),
    re_path('^expert_detail', expert_detail, name='expert_detail'),
    re_path('^paper_list', paper_list, name='paper_list'),
    re_path('^paper_detail', paper_detail, name='paper_detail'),
    path('login/', login, name='login'),
    path('check_login/', check_login, name='check_login'),
    path('user_center/', user_center, name='user_center'),
    path('edit_info/', edit_info, name='edit_info'),
    path('change_pwd/', change_pwd, name='change_pwd'),
    path('logout/', logout, name='logout'),
    path('add_fav/', add_fav, name='add_fav'),
    path('del_fav/', del_fav, name='del_fav'),
    # re_path('^register', register, name='register'),
    # path('index/', index, name='index'),
    # re_path("^$", HomePageView.as_view(), name="index"),
    # re_path("^detail",  ExpertDetailView.as_view(), name="detail"),
    # re_path("^list",  ExpertListView.as_view(), name="list"),
]
