"""
URL configuration for vk_web_aivan project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('question/', views.index, name='question'),
    path('question/<int:question_id>/', views.add_answer, name='add_answer'),
    path('handle_invalid_page/', views.handle_invalid_page, name='handle_invalid_page'),

    path('settings/', views.settings, name='settings'),
    path('logout_macro/', views.user_logout, name='logout'),
    path('login/', views.login_window, name='login'),
    path('register/', views.user_registration, name='register'),
    path('ask/', views.ask, name='ask'),

    path('tag/<str:tag>/', views.tag_questions, name='tag'),
    path('hot/', views.hot_questions, name='hot'),
    path('new/', views.new_questions, name='new'),
    path('question/<int:question_id>/', views.question, name='question'),

    path('admin/', admin.site.urls),
    
]
