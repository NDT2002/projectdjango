from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.home,name='home'),

    path('dang-nhap', views.signin,name='signin'),
    path('dang-ky', views.signup,name='regisiter'),

    path('tin-tuc', views.news_list, name='news_list'),
    path('tin-tuc/<int:post_id>/', views.news, name='news_detail'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)