from . import views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("bai-viet/", views.post, name="post"),
    path("bai-viet/create", views.create_post, name="create_post"),
    path("bai-viet/add", views.add_posts, name="add_post"),
    path("bai-viet/<int:post_id>/edit/", views.edit_post, name="edit_post"),
    path("bai-viet/update/", views.update_post, name="update_post"),
    path("bai-viet/<int:post_id>/delete/", views.delete_post, name="delete_post"),

    path("tac-gia/", views.author, name="author"),
    path("tac-gia/create", views.create_author, name="create_author"),
    path("tac-gia/add", views.add_authors, name="add_author"),
    path("tac-gia/<int:author_id>/edit/", views.edit_author, name="edit_author"),
    path("tac-gia/update/", views.update_author, name="update_author"),

    path("danh-muc/", views.term, name="term"),
    path("danh-muc/create", views.add_term, name="create_term"),

    path("loai-danh-muc/", views.term_taxonomy, name="taxonomy"),
    path("loai-danh-muc/create", views.add_term_taxanomy, name="create_taxonomy"),
    
    path("giao-dien/widget/", views.widget, name="widget"),
    path("giao-dien/widget/create", views.create_widget, name="create_widget"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
