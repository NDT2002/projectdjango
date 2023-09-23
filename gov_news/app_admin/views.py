from django.shortcuts import get_object_or_404, render
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from . import forms
from . import models
from django.utils import timezone
import pdb
def post(request, filter=None, val=None ):
    posts_table=models.Post.objects.all()
    posts=models.Post.objects.filter(deleted_at__isnull=True)
    published_count = models.Post.objects.filter(post_status='published')
    pending_count = models.Post.objects.filter(post_status='pending')
    draft_count = models.Post.objects.filter(post_status='draft')
    other_count = models.Post.objects.exclude(post_status__in=['published', 'pending', 'draft'])
    deleted_count = models.Post.objects.filter(deleted_at__isnull=False)
    if filter and val:
        if filter=='post_status':
            if val == 'published':
                posts_table=published_count
            elif val == 'pending':
                posts_table=pending_count
            elif val == 'draft':
                posts_table=draft_count
        else:
            posts_table=deleted_count
    return render(request, 'admin/posts/posts_list.html', {'posts_table':posts_table,'posts':posts,'published_count': published_count,
        'pending_count': pending_count,
        'draft_count': draft_count,
        'other_count': other_count,
        'deleted_count':deleted_count,
        })

def create_post(request):
    terms=models.Term.objects.all()
    tags=models.Tag.objects.all()
    return render(request, 'admin/posts/add_post.html', {'terms':terms,'tags':tags,})

def add_posts(request):
    if request.method == 'POST':
        form = forms.PostForm(request.POST, request.FILES)
        if form.is_valid():
            post=form.save()
            term_id=request.POST['term']
            term=models.Term.objects.get(pk=term_id)
            models.TermRelationship.objects.create(post=post, term=term)
            selected_tags = request.POST.getlist('tags_val')
            for tag_id in selected_tags:
                tag = models.Tag.objects.get(pk=tag_id)
                models.TagRelationship.objects.create(post=post, tag=tag)
            return redirect('post')  # Điều hướng đến trang danh sách bài viết sau khi thêm
    else:
        form = models.PostForm()
    return render(request, 'admin/posts/add_post.html', {'form': form})

def edit_post(request,post_id):
    posts = models.Post.objects.get(pk=post_id)
    users = models.CustomUser.objects.all() 
    taxonomies=models.TermTaxonomy.objects.all()
    term_relationships = models.TermRelationship.objects.filter(object_id=post_id).first()
    if term_relationships:
    # Lấy trường term_taxonomy_id từ TermRelationship
        tt = term_relationships.term_taxonomy_id
    else:
        tt=0
    return render(request, 'admin/posts/edit_post.html', {'post':posts, "users":users, "taxonomies":taxonomies, 'term_rls': tt})

def update_post(request):
    # Lấy ra bài viết hoặc trả về lỗi 404 nếu không tồn tại
    if request.method == 'POST':
        # Lấy dữ liệu từ biểu mẫu POST
        post_id = request.POST['post_id']
        post = get_object_or_404(models.Post, id=post_id)
        # Kiểm tra xác thực và quyền truy cập ở đây (nếu cần)
        # Ví dụ: if not request.user.has_perm('your_app.change_post'):
        post.post_title = request.POST['post_title']
        post.post_name = request.POST['post_name']
        post.post_excerpt = request.POST['post_excerpt']
        post.post_content = request.POST['post_content']
        post.post_type = request.POST['post_type']
        post.post_status = request.POST['post_status']
        post.post_date = request.POST['post_date']

        # Xử lý hình ảnh đại diện
        if 'post_image' in request.FILES:
            post.post_image = request.FILES['post_image']
        post.save()
        return redirect('post')  # Điều hướng đến trang danh sách bài viết sau khi cập nhật
    else:
        form = forms.PostForm(instance=post)
    return render(request, 'admin/posts/edit_post.html', {'form': form, 'post_id':post_id})

def delete_post(request, post_id):
    # Kiểm tra xác thực và quyền truy cập (nếu cần)
    # Ví dụ: if not request.user.has_perm('your_app.delete_post'):
    post = get_object_or_404(models.Post, id=post_id)
    post.soft_delete()
    return redirect('post') 
    # Nếu không phải yêu cầu POST hoặc không xác nhận xóa, hiển thị trang xác nhận xóa
    context = {'post': post}
    return render(request, 'admin/posts/posts_list.html', context)

def restore_post(request, post_id):
    post = get_object_or_404(models.Post, pk=post_id)
    
    # Kiểm tra xem bài viết có bị xóa không (có deleted_at không rỗng)
    if post.deleted_at:
        # Phục hồi bài viết bằng cách đặt deleted_at về None
        post.deleted_at = None
        post.save()
    
    # Chuyển hướng người dùng đến trang danh sách bài viết hoặc trang chi tiết của bài viết đã phục hồi
    return redirect('post')

def term(request):
    terms=models.Term.objects.all()
    form = forms.TermForm()
    return render(request,'admin/term/term.html', {'terms':terms,'form':form})
def term_detail(request, term_id):
    try:
        term=models.Term.objects.get(pk=term_id)
        list=models.Term.objects.all()
        # Tìm kiếm term_taxonomy dựa trên term_id
        term_taxonomy = models.Term.objects.filter(parent=term_id)
        posts = models.Post.objects.filter(termrelationship__term_id=term_id)
        return render(request,'admin/term/term_detail.html', {'term':term ,'terms':list , 'taxonomy':term_taxonomy, 'posts':posts})
    except models.Term.DoesNotExist:
        return redirect('term')

def add_term(request):
    if request.method == 'POST':
        form = forms.TermForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('term')
    else:
        form = forms.TermForm()
    return render(request, 'admin/term/term.html', {'form': form})

# Hàm cập nhật Term
def update_term(request, term_id):
    try:
        term = models.Term.objects.get(pk=term_id)
        if request.method == 'POST':
            form = forms.TermForm(request.POST, instance=term)
            if form.is_valid():
                form.save()
                return redirect('term')  # Chuyển hướng sau khi cập nhật
        return render(request, 'admin/term/term.html', {'form': term})
    except models.Term.DoesNotExist:
        return redirect('term')  # Xử lý khi không tìm thấy Term

# Hàm xóa Term (đánh dấu là đã xóa)
def delete_term(request, term_id):
    try:
        term = models.Term.objects.get(pk=term_id)
        term.soft_delete()
        return redirect('term')  # Chuyển hướng sau khi xóa
    except models.Term.DoesNotExist:
        return redirect('term')  # Xử lý khi không tìm thấy Term

# Hàm phục hồi Term đã xóa
def restore_term(request, term_id):
    try:
        term = models.Term.objects.get(pk=term_id)
        term.restore()
        return redirect('term')  # Chuyển hướng sau khi phục hồi
    except models.Term.DoesNotExist:
        return redirect('term')  # Xử lý khi không tìm thấy Term

def tags(request):
    tags=models.Tag.objects.all()
    return render(request, 'admin/term/tags.html', {'tags': tags})
def add_tag(request):
    if request.method == 'POST':
        form = forms.TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tags')
    else:
        form = forms.TagForm()
    return render(request, 'admin/term/tags.html', {'form': form})
def edit_tag(request, tag_id):
    tag = models.Tag.objects.get(pk=tag_id)

    if request.method == 'POST':
        form = forms.TagForm(request.POST, instance=tag)
        if form.is_valid():
            form.save()
            return redirect('tags')
    else:
        form = forms.TagForm(instance=tag)

    return render(request, 'admin/term/tags.html', {'form': form, 'tag': tag})
def delete_tag(request, tag_id):
    tag = models.Tag.objects.get(pk=tag_id)
    tag.delete()
    return redirect('tag_list')
def permanent_delete_tag(request, tag_id):
    tag = models.Tag.objects.get(pk=tag_id)
    tag.delete()
    return redirect('tag_list')
def restore_tag(request, tag_id):
    tag = models.Tag.objects.get(pk=tag_id)
    tag.deleted_at = None
    tag.save()
    return redirect('tag_list')

def author(request):
     # Lấy tất cả người dùng từ bảng CustomUser
    authors = models.CustomUser.objects.all()

    # Tạo một danh sách để lưu trữ thông tin mở rộng cho mỗi người dùng
    author_data_list = []

    # Lặp qua danh sách người dùng và lấy thông tin mở rộng từ bảng UserMeta
    for author in authors:
        user_id = author.id  # Lấy user_id của người dùng
        author_extended_data = {}  # Tạo từ điển cho thông tin mở rộng của người dùng

        # Các metakey bạn muốn truy xuất
        metakeys_to_retrieve = ["address", "phone", "description", "job"]

        # Lấy thông tin mở rộng cho người dùng cụ thể
        user_meta_data = models.UserMeta.objects.filter(user_id=user_id, meta_key__in=metakeys_to_retrieve)

        # Xây dựng từ điển thông tin mở rộng cho người dùng
        for meta in user_meta_data:
            author_extended_data[meta.meta_key] = meta.meta_value
        # Thêm thông tin mở rộng và người dùng vào danh sách
        author_data_list.append({'author': author, 'extended_data': author_extended_data})
    return render(request, 'admin/author/auth_list.html', {'author_data_list': author_data_list})

def create_author(request):
    return render(request, 'admin/author/add_auth.html')
def add_authors(request):
    if request.method == 'POST':
        form = forms.UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_registered = timezone.now()
            user.save()
            return redirect('author_list')
    else:
        form = forms.UserForm()
    return render(request, 'admin/author/add_auth.html', {'form': form})
def edit_author(request):
    return render(request, 'admin/term/term_taxonomy.html')
def update_author(request):
    return render(request, 'admin/term/term_taxonomy.html')

def widget(request):
    return render(request,'admin/widget/widget.html')
def create_widget(request):
    return render(request,'admin/widget/widgetnew.html')



# function riêng
