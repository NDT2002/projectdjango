from django.contrib import admin
from django.urls import reverse
# from ckeditor.widgets import CKEditorWidget
from . import models
# Register your models here.
admin.site.register(models.Post)
admin.site.register(models.Term)
admin.site.register(models.TermRelationship)
admin.site.login_template = 'admin/login.html'
admin.site.index_template = 'admin/base_site.html'

# @admin.register(models.Post)
# class PostAdmin(admin.ModelAdmin):
#     change_list_template = 'admin/posts/posts_list.html'
#     add_form_template = 'admin/posts/add_post.html'
#     # def add_view(self, request, form_url='', extra_context=None):
#     #     # Tùy chỉnh hành vi khi truy cập trang thêm một bài viết
#     #     # Ví dụ: Thay đổi URL action của form
#     #     self.change_form_template = 'admin/posts/add_post.html'  # Template tùy chỉnh
#     #     return super().add_view(request, form_url, extra_context)
    
# @admin.register(models.Term)
# class TermAdmin(admin.ModelAdmin):
#     change_list_template = 'admin/term/term.html'
#     add_form_template = 'admin/term/term.html'
#     search_fields = ['name']
# @admin.register(models.TermTaxonomy)
# class TermTaxonomyAdmin(admin.ModelAdmin):
#     change_list_template = 'admin/term/term_taxonomy.html'
#     add_form_template = 'admin/term/term_taxonomy.html'
#     autocomplete_fields = ['term_id']