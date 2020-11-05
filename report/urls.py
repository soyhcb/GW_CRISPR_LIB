# -*- encoding: utf-8 -*-

from django.urls import path, re_path
from report import views

urlpatterns = [
    path('report', views.report, name='report'),
]
