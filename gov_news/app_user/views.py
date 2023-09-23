from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import HttpResponse
from app_admin import models
# Create your views here.
def home(request):
    return render(request, 'home.html')

def signin(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'regisiter.html')

def news(request, post_id):
    # Lấy bài viết cụ thể hoặc trả về 404 nếu không tìm thấy
    post = get_object_or_404(models.Post, pk=post_id)
    categories = models.TermRelationship.objects.get(post=post_id)
    # Lấy danh sách 5 bài viết cùng danh mục với bài viết đã chọn
    related_posts = models.Post.objects.filter(termrelationship__term_id=categories.term)[:5]
    
    return render(request, 'newspage/newsdetail.html', {'post': post,'related_posts':related_posts, 'term':categories})

def news_list(request):
     # Truy vấn tất cả bài viết
    all_posts = models.Post.objects.all()
    # Phân trang
    posts_per_page = 5
    paginator = Paginator(all_posts, posts_per_page)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'newspage/postlist.html',{'posts':posts})
