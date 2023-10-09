from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator
from django.core.cache import cache
from django.http import HttpResponse
from app_admin import models
from random import sample
from . import forms
# Create your views here.
def home(request):
    term = models.Term.objects.all()
    all_categories = models.Term.objects.filter(termrelationship__isnull=False).distinct()

    # Lấy ngẫu nhiên 4 danh mục từ tất cả danh mục
    random_categories = sample(list(all_categories), 6)

    posts_in_categories = {}
    for category in random_categories:
        term_relationships = models.TermRelationship.objects.filter(term=category)
        post_ids = term_relationships.values_list('post_id', flat=True)
        posts = models.Post.objects.filter(id__in=post_ids).order_by('?')[:4]
        posts_in_categories[category] = posts
    hot_news = models.Post.objects.filter(tagrelationship__tag__name='tin nổi bật')[:4]
    action_news = models.Post.objects.filter(tagrelationship__tag__name='hoạt động')[:6]
    return render(request, 'home.html', { 'hot_news':hot_news, 'actions':action_news, 
                                           'posts_in_categories': posts_in_categories,
                                        })

def signin(request):
    return render(request, 'login.html')

def user_login(request):
    if request.method == 'POST':
        form = forms.UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active and not user.is_staff:
                    login(request, user)
                    return redirect('home')  # Chuyển hướng đến trang chính sau khi đăng nhập
                else:
                    return redirect('post')  # Điều hướng đến trang đăng nhập admin nếu không phải người dùng thường
    else:
        form = forms.UserLoginForm()
    return render(request, 'login.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = forms.UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password']) 
            user.save() 
            login(request, user)
            return redirect('signin')  # Chuyển hướng sau khi đăng ký thành công
    else:
        form = forms.UserRegistrationForm()
    return render(request, 'regisiter.html', {'form': form})

def user_register(request):
    return render(request, 'regisiter.html')
def contact(request):
    return render(request, 'contact.html')

def news(request, post_id):
    term=models.Term.objects.all()
    # Lấy bài viết cụ thể hoặc trả về 404 nếu không tìm thấy
    post = get_object_or_404(models.Post, pk=post_id)
    categories = models.TermRelationship.objects.get(post=post_id)
    # Lấy danh sách 5 bài viết cùng danh mục với bài viết đã chọn
    related_posts = models.Post.objects.filter(termrelationship__term_id=categories.term)[:5]
    related_comment=models.Comment.objects.filter(post_id=post_id)
    return render(request, 'newspage/newsdetail.html', { 'terms':term,'post': post,'related_posts':related_posts, 'term':categories,'related_comment':related_comment})

def news_tag_list(request, tag=None):
    Tags=models.Tag.objects.all()
    related_posts = models.Post.objects.filter(tagrelationship__tag__name='tin nổi bật')
    if tag :
        all_posts=related_posts
    # Phân trang
    posts_per_page = 5
    paginator = Paginator(all_posts, posts_per_page)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'newspage/postlist.html',{'posts':posts, 'terms':Tags, 'ter':tag})

def news_list(request, term_slug=None):
     # Truy vấn tất cả bài viết
    all_posts = models.Post.objects.all()
    terms=models.Term.objects.all()
    if term_slug :
        term=models.Term.objects.get(slug=term_slug)
        related_posts = models.Post.objects.filter(termrelationship__term=term)
        all_posts=related_posts
    # Phân trang
    posts_per_page = 5
    paginator = Paginator(all_posts, posts_per_page)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'newspage/postlist.html',{'posts':posts, 'terms':terms, 'ter':term})


def add_comment(request, post_id):
    post = get_object_or_404(models.Post, pk=post_id)

    if request.method == 'POST':
        form = forms.CommentForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            user = request.user if request.user.is_authenticated else None
            author = request.user.display_name if user else form.cleaned_data['author']
            author_email = user.email if user else form.cleaned_data['author_email']

            models.Comment.create_comment(
                post=post,
                author=author,
                author_email=author_email,
                content=content,
                user=user,
            )
            cache.clear()
            return redirect('news_detail', post_id=post_id)

    else:
        return redirect('news_detail', post_id=post_id)