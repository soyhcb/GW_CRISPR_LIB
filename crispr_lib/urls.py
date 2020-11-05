# -*- encoding: utf-8 -*-

from django.urls import path, re_path
from crispr_lib import views

urlpatterns = [
    path('crispr_lib', views.crispr_lib_page, name='crispr_lib_page'),
    path('crispr/<str:fullname>', views.check_gsrna, name='check_gsrna'),
]
