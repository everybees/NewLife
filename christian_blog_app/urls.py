from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    #path('', views.PostList.as_view(), name='index'),
    path('login', views.login, name= 'login'),
    path('logout', views.logout, name= 'logout'),
    path('register', views.register, name = 'register'),
    path('dashboard', views.dashboard, name = 'dashboard'),
    path('posts', views.posts, name = 'posts'),
    path('articles', views.articles, name='articles'),
    path('prayers', views.prayers,name='prayers' ),
    path('prayer_request', views.prayers, name='prayer_request'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
    path('testing', views.testing, name='testing'),
    path('activation',views.activate, name='activation'),

    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), 
        name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'), 
        name='password_change'),

    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html'),
     name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
     name='password_reset_complete'),
]