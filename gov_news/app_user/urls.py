from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.home,name='home'),
    path('gioi-thieu',views.contact,name='contact'),
    path('dang-nhap', views.signin,name='signin'),
    path('login', views.user_login,name='login'),
    path('dang-ky', views.user_register,name='regisiter'),
    path('register', views.signup, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    
    path('tin-tuc/', views.news_list, name='news_list'),
    path('tin-tuc/<str:term_slug>', views.news_list, name='news_term_list'),
    path('tin-tuc/<int:post_id>/', views.news, name='news_detail'),
    path('tin-tuc/<str:tag>/', views.news_tag_list, name='news_tag_list'),
    path('tin-tuc/binh-luan/<int:post_id>/', views.add_comment, name='news_comment'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)