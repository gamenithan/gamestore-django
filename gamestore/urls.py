"""gamestore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from gamedata import views

urlpatterns = [
    path('admin/', admin.site.urls, name='admin1'),
    path('', views.home_page, name='index'),
    path('login/', views.my_login, name='login'),
    path('logout/', views.my_logout, name='logout'),
    path('change_password', views.change_password, name='change_password'),
    path('list/<int:game_num>', views.game_list, name='list'),
    path('home_page/', views.home_page, name='home_page'),
    path('show_error/', views.show_error_404),
    path('register/', views.regis, name='regis'),
    path('after/', views.my_regis, name='sign'),
    path('all/', views.my_all, name='all'),
    path('filter/', views.my_filter, name='filter'),
    path('buygame/<int:buy_num>', views.my_buygame, name='buygame'),
    path('afterbuy/<int:num>', views.user_game, name='afterbuy'),
    path('userlib/', views.my_lib, name="userlib"),
    path('edit/', views.my_edit, name='edit'),
    path('editaf/', views.after_edit, name='editaf')
        
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
