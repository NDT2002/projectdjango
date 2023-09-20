from django import forms
from . import models
class PostForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ['post_title','post_name','post_excerpt', 'post_content', 'post_author', 'post_status', 'post_type','post_image']
class TermForm(forms.ModelForm):
    class Meta:
        model = models.Term
        fields = ['name', 'slug', 'term_group']

class TermTaxonomyForm(forms.ModelForm):
    class Meta:
        model= models.TermTaxonomy
        fields=['term_id','taxonomy', 'parent']


class UserForm(forms.ModelForm):
    class Meta:
        model = models.CustomUser
        fields = ['username', 'first_name', 'last_name', 'email','display_name','password']
