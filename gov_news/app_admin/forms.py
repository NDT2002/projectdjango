from django import forms
from . import models
class PostForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ['post_author', 'post_content', 'post_image', 'post_title', 'post_excerpt', 'post_status', 'comment_status', 'post_name', 'post_type']
class TermForm(forms.ModelForm):
    class Meta:
        model = models.Term
        fields = ['name', 'slug', 'parent','term_group','description']
class TagForm(forms.ModelForm):
    class Meta:
        model = models.Tag
        fields = ['name','description']
class UserForm(forms.ModelForm):
    class Meta:
        model = models.CustomUser
        fields = ['username', 'first_name', 'last_name', 'email','display_name','password']
