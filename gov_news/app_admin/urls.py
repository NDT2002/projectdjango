from . import views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
urlpatterns = [
    path("dang-xuat/", auth_views.LogoutView.as_view(next_page='/admin/'), name='logout'),
    path("bai-viet/", login_required(views.post), name="post"),
    path("bai-viet/<str:filter>?=<str:val>", login_required(views.post), name="post_filter"),
    path("bai-viet/create", login_required(views.create_post), name="create_post"),
    path("bai-viet/add", login_required(views.add_posts), name="add_post"),
    path("bai-viet/<int:post_id>/edit/", login_required(views.edit_post), name="edit_post"),
    path("bai-viet/update/", login_required(views.update_post), name="update_post"),
    path("bai-viet/<int:post_id>/delete/", login_required(views.delete_post), name="delete_post"),
    path('bai-viet/<int:post_id>/restore/', login_required(views.restore_post), name='restore_post'),

    path("tac-gia/", login_required(views.author), name="author"),
    path("tac-gia/create", login_required(views.create_author), name="create_author"),
    path("tac-gia/add", login_required(views.add_authors), name="add_author"),
    path("tac-gia/<int:author_id>/edit/", login_required(views.edit_author), name="edit_author"),
    path("tac-gia/<int:author_id>/update/", login_required(views.update_author), name="update_author"),

    path("danh-muc/", login_required(views.term), name="term"),
    path("danh-muc/create", login_required(views.add_term), name="create_term"),
    path("danh-muc/<int:term_id>/view/", login_required(views.term_detail), name="detail_term"),
    path("danh-muc/<int:term_id>/update/", login_required(views.update_term), name="update_term"),
    path("danh-muc/<int:term_id>/delete/", login_required(views.delete_term), name="delete_term"),
    path('danh-muc/<int:term_id>/restore/', login_required(views.restore_term), name='restore_term'),

    path("tu-khoa/", login_required(views.tags), name="tags"),
    path("tu-khoa/create", login_required(views.add_tag), name="create_tag"),
    path("tu-khoa/<int:tag_id>/drop/", login_required(views.permanent_delete_tag), name="drop_tag"),
    # path("tu-khoa/<int:tag_id>/update/", login_required(views.update_tag), name="update_tag"),
    path("tu-khoa/<int:tag_id>/delete/", login_required(views.delete_tag), name="delete_tag"),
    path('tu-khoa/<int:tag_id>/restore/', login_required(views.restore_tag), name='restore_tag'),

    path('tuy-chon/menu', login_required(views.restore_tag), name='restore_tag'),
    path("giao-dien/widget/", login_required(views.widget), name="widget"),
    path("giao-dien/widget/create", login_required(views.create_widget), name="create_widget"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
