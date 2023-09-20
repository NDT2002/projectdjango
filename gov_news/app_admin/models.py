from django.utils import timezone
from django.contrib.auth.models import AbstractUser, BaseUserManager,PermissionsMixin
from django.db import models

def upload_to(instance, filename):
    return f'profile_images/{instance.id}/{filename}'


class CustomUser(AbstractUser):
    user_nicename = models.CharField(max_length=50, db_index=True)
    user_url = models.URLField(max_length=100)
    user_registered = models.DateTimeField(default=timezone.now, editable=False)
    display_name = models.CharField(max_length=250)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to=upload_to, null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)


class CommentMeta(models.Model):
    comment_id = models.ForeignKey('Comment', on_delete=models.CASCADE)  # Liên kết với Comment
    meta_key = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    meta_value = models.TextField(blank=True, null=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = 'commentmeta'

class Comment(models.Model):
    comment_post_id = models.BigIntegerField(db_index=True)
    comment_author = models.TextField()
    comment_author_email = models.CharField(max_length=100, db_index=True)
    comment_author_url = models.CharField(max_length=200)
    comment_author_IP = models.CharField(max_length=100)
    comment_date = models.DateTimeField()
    comment_date_gmt = models.DateTimeField(db_index=True)
    comment_content = models.TextField()
    comment_approved = models.CharField(max_length=20, db_index=True)
    comment_agent = models.CharField(max_length=255)
    comment_type = models.CharField(max_length=20)
    comment_parent = models.BigIntegerField(db_index=True)
    user_id = models.ForeignKey('CustomUser', on_delete=models.SET_NULL, null=True)  # Liên kết với CustomUser
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'comments'

class Link(models.Model):
    link_url = models.CharField(max_length=255)
    link_name = models.CharField(max_length=255)
    link_image = models.CharField(max_length=255)
    link_target = models.CharField(max_length=25)
    link_description = models.CharField(max_length=255)
    link_visible = models.CharField(max_length=20, db_index=True, default='Y')
    link_owner = models.ForeignKey('CustomUser', on_delete=models.CASCADE)  # Liên kết với CustomUser
    link_rating = models.IntegerField(default=0)
    link_updated = models.DateTimeField()
    link_rel = models.CharField(max_length=255)
    link_notes = models.TextField()
    link_rss = models.CharField(max_length=255)
    deleted_at = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = 'links'

class Option(models.Model):
    option_name = models.CharField(max_length=64, unique=True)
    option_value = models.TextField()
    autoload = models.CharField(max_length=20, db_index=True, default='yes')
    deleted_at = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = 'options'

class PostMeta(models.Model):
    post_id = models.ForeignKey('Post', on_delete=models.CASCADE)  # Liên kết với Post
    meta_key = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    meta_value = models.TextField(blank=True, null=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = 'postmeta'

class Post(models.Model):
    post_author = models.ForeignKey('CustomUser', on_delete=models.SET_NULL, null=True)  # Liên kết với CustomUser
    post_date = models.DateTimeField(auto_now_add=True, db_index=True)#
    post_content = models.TextField()#
    post_image = models.ImageField(upload_to=upload_to, null=True, blank=True)
    post_title = models.TextField()#
    post_excerpt = models.TextField()#
    post_status = models.CharField(max_length=20, db_index=True, default='publish')#
    comment_status = models.CharField(max_length=20, default='open')#
    post_password = models.CharField(max_length=20,null=True, blank=True)
    post_name = models.CharField(max_length=200, db_index=True)#
    post_modified = models.DateTimeField(auto_now=True)#
    post_parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)  # Liên kết với chính nó
    guid = models.CharField(max_length=255,null=True, blank=True)
    menu_order = models.IntegerField(default=0)
    post_type = models.CharField(max_length=20, db_index=True, default='post')
    post_mime_type = models.CharField(max_length=100,null=True, blank=True)
    comment_count = models.BigIntegerField(default=0)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        self.deleted_at = None
        self.save()

    def is_deleted(self):
        return self.deleted_at is not None

    class Meta:
        db_table = 'posts'

class Term(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.CharField(max_length=200, db_index=True)
    term_group = models.BigIntegerField(default=0)
    deleted_at = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = 'terms'

class TermMeta(models.Model):
    term_id = models.ForeignKey('Term', on_delete=models.CASCADE)  # Liên kết với Term
    meta_key = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    meta_value = models.TextField(blank=True, null=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = 'termmeta'

class TermTaxonomy(models.Model):
    term_id = models.ForeignKey('Term', on_delete=models.CASCADE)  # Liên kết với Term
    taxonomy = models.CharField(max_length=32, unique=True, db_index=True)
    description = models.TextField()
    parent = models.BigIntegerField(default=0)
    deleted_at = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = 'term_taxonomy'
        
class TermRelationship(models.Model):
    object_id = models.BigIntegerField(db_index=True)
    term_taxonomy_id = models.ForeignKey(TermTaxonomy, on_delete=models.CASCADE)
    term_order = models.IntegerField(default=0)  # Định nghĩa giá trị mặc định ở đây
    deleted_at = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = 'term_relationships'



class UserMeta(models.Model):
    user_id = models.ForeignKey('CustomUser', on_delete=models.CASCADE)  # Liên kết với CustomUser
    meta_key = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    meta_value = models.TextField(blank=True, null=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = 'usermeta'

