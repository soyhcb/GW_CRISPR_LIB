from django.urls import path, re_path
from general import views

urlpatterns = [
    # Matches any html file 
    re_path(r'^.*\.html', views.pages, name='pages'),

    # The home page
    path('', views.index, name='home'),
    path("login/", views.login_view, name="login")
]
