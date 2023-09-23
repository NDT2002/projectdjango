from django.utils import timezone
from django.contrib.auth.models import AbstractUser, BaseUserManager,PermissionsMixin
from django.db import models

def upload_to(instance, filename):
    return f'profile_images/{instance.id}/{filename}'
def upload_img(instance, filename):
    return f'news_images/{instance.id}/{filename}'


class CustomUser(AbstractUser):
    user_url = models.URLField(max_length=100, blank=True)
    display_name = models.CharField(max_length=250, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to=upload_to, null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def create_user(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        if extra_fields.get('is_staff') is not True:
            extra_fields.setdefault('is_active', True)

        return self._create_user(username, password, **extra_fields)

    def update_user(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.save()
    def delete_user(self):
        self.is_active = False
        self.deleted_at = timezone.now()
        self.save()
    def restore_user(self):
        self.deleted_at = None
        self.save()


class CommentMeta(models.Model):
    comment_id = models.ForeignKey('Comment', on_delete=models.CASCADE)  # Liên kết với Comment
    meta_key = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    meta_value = models.TextField(blank=True, null=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = 'commentmeta'

class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    author = models.TextField()
    author_email = models.CharField(max_length=100, db_index=True)
    date = models.DateTimeField()
    content = models.TextField()
    approved = models.BooleanField(default=False)
    user = models.ForeignKey('CustomUser', on_delete=models.SET_NULL, null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'comments'
 
    def create_comment(cls, post, author, author_email, content, approved=False, user=None):
        return cls.objects.create(
            post=post,
            author=author,
            author_email=author_email,
            date=timezone.now(),
            content=content,
            approved=approved,
            user=user,
        )

    def delete_comment(self):
        self.deleted_at = timezone.now()
        self.save()
    def restore(self):
        self.deleted_at = None
        self.save()

from django.db import models
from django.utils import timezone

class Link(models.Model):
    url = models.URLField(max_length=255)
    name = models.CharField(max_length=255)
    image = models.URLField(max_length=255)
    target = models.CharField(max_length=25)
    description = models.CharField(max_length=255)
    visible = models.CharField(max_length=20, db_index=True, default='Y')
    owner = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    updated = models.DateTimeField()
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'links'

    @classmethod
    def create_link(cls, url, name, image, target, description, owner, rating=0, updated=None):
        if updated is None:
            updated = timezone.now()
        return cls.objects.create(
            url=url,
            name=name,
            image=image,
            target=target,
            description=description,
            owner=owner,
            rating=rating,
            updated=updated,
        )

    def delete_link(self):
        self.deleted_at = timezone.now()
        self.save()

    def update_link(self, url=None, name=None, image=None, target=None, description=None, rating=None, updated=None):
        if url is not None:
            self.url = url
        if name is not None:
            self.name = name
        if image is not None:
            self.image = image
        if target is not None:
            self.target = target
        if description is not None:
            self.description = description
        if rating is not None:
            self.rating = rating
        if updated is not None:
            self.updated = updated
        self.save()
    def restore(self):
        self.deleted_at = None
        self.save()

class Option(models.Model):
    name = models.CharField(max_length=64, unique=True)
    value = models.TextField()
    autoload = models.BooleanField(default=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'options'

    @classmethod
    def create_option(cls, name, value, autoload=True):
        return cls.objects.create(
            name=name,
            value=value,
            autoload=autoload,
        )

    @classmethod
    def restore(self):
        self.deleted_at = None
        self.save()

    def update_option(self, value=None, autoload=None):
        if value is not None:
            self.value = value
        if autoload is not None:
            self.autoload = autoload
        self.save()

    def delete_option(self):
        self.deleted_at = timezone.now()
        self.save()
class PostMeta(models.Model):
    post_id = models.ForeignKey('Post', on_delete=models.CASCADE)  # Liên kết với Post
    meta_key = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    meta_value = models.TextField(blank=True, null=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = 'postmeta'

from django.db import models
from django.utils import timezone

class Post(models.Model):
    post_author = models.ForeignKey('CustomUser', on_delete=models.SET_NULL, null=True)
    post_date = models.DateTimeField(auto_now_add=True, db_index=True)
    post_content = models.TextField()
    post_image = models.ImageField(upload_to=upload_img, null=True, blank=True)
    post_title = models.TextField()
    post_excerpt = models.TextField()
    post_status = models.CharField(max_length=20, db_index=True, default='publish')
    comment_status = models.BooleanField(default=True)
    post_name = models.CharField(max_length=200, db_index=True)
    post_modified = models.DateTimeField(auto_now=True)
    post_parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    post_guid = models.CharField(max_length=255, null=True, blank=True)
    post_type = models.CharField(max_length=20, db_index=True, default='post')
    comment_count = models.BigIntegerField(default=0)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'posts'

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        self.deleted_at = None
        self.save()

    def is_deleted(self):
        return self.deleted_at is not None


class TermMeta(models.Model):
    term_id = models.ForeignKey('Term', on_delete=models.CASCADE)  # Liên kết với Term
    meta_key = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    meta_value = models.TextField(blank=True, null=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = 'termmeta'

class Term(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    term_group = models.BigIntegerField(default=0)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'terms'

    def create_term(cls, term_name, term_slug, description, parent=None, term_group=0):
        return cls.objects.create(
            name=term_name,
            slug=term_slug,
            description=description,
            parent=parent,
            term_group=term_group,
        )

    def update_term(self, term_name=None, term_slug=None, description=None, parent=None, term_group=None):
        if term_name is not None:
            self.name = term_name
        if term_slug is not None:
            self.slug = term_slug
        if description is not None:
            self.description = description
        if parent is not None:
            self.parent = parent
        if term_group is not None:
            self.term_group = term_group
        self.save()

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        self.deleted_at = None
        self.save()

    def is_deleted(self):
        return self.deleted_at is not None
    @property
    def name_with_indent(self):
        indentation = '-' * self.calculate_depth()
        return f'{indentation} {self.name}'

    def calculate_depth(self):
        depth = 0
        parent = self.parent
        while parent:
            depth += 1
            parent = parent.parent
        return depth
class TermRelationship(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    term = models.ForeignKey('Term', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('post', 'term')
        db_table = 'term_relationships'

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'tags'

    def __str__(self):
        return self.name
class TagRelationship(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE)

    class Meta:
        db_table = 'tag_relationships'
        unique_together = ('post', 'tag')
class UserMeta(models.Model):
    user_id = models.ForeignKey('CustomUser', on_delete=models.CASCADE)  # Liên kết với CustomUser
    meta_key = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    meta_value = models.TextField(blank=True, null=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = 'usermeta'

