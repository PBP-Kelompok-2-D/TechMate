from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Blog, Comment, Review
from .forms import BlogForm, CommentForm, ReviewForm

# 1. FITUR BACA (Bisa diakses semua orang)

def forum_list(request):
    """Menampilkan semua thread forum diskusi."""
    blogs = Blog.objects.all().order_by('-published_date_time')
    return render(request, 'forum.html', {'blogs': blogs})

def forum_detail(request, slug):
    """Menampilkan detail satu thread beserta komentar-komentarnya."""
    blog = get_object_or_404(Blog, slug=slug)
    comments = blog.comments.filter(parent__isnull=True) # Hanya ambil komentar utama (bukan balasan)
    form = CommentForm()
    return render(request, 'detail.html', {'blog': blog, 'comments': comments, 'form': form})

def review_list(request):
    """Menampilkan daftar rating & ulasan gadget dengan fitur pencarian."""
    query = request.GET.get('q', '') # Menangkap kata kunci dari URL
    
    if query:
        # Mencari ulasan yang nama perangkatnya mengandung kata kunci
        reviews = Review.objects.filter(device_name__icontains=query).order_by('-created_at')
    else:
        reviews = Review.objects.all().order_by('-created_at')
        
    form = ReviewForm()
    return render(request, 'reviews.html', {'reviews': reviews, 'form': form, 'query': query})

# 2. FITUR CREATE/UPDATE (Wajib Login)

@login_required(login_url='/login/')
def create_thread(request):
    """Membuat thread forum baru."""
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            return redirect('community:forum_detail', slug=blog.slug)
    else:
        form = BlogForm()
    return render(request, 'create_thread.html', {'form': form})

@login_required(login_url='/login/')
def create_review(request):
    """Menambah ulasan gadget baru."""
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.author = request.user
            review.save()
            return redirect('community:review_list')
    return redirect('community:review_list')

@login_required(login_url='/login/')
def add_comment(request, blog_id):
    """Menambahkan komentar pada suatu thread."""
    blog = get_object_or_404(Blog, id=blog_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.CommentPost = blog
            comment.author = request.user
            
            # Cek apakah ini balasan dari komentar lain (reply)
            parent_id = request.POST.get('parent_id')
            if parent_id:
                comment.parent = get_object_or_404(Comment, id=parent_id)
                
            comment.save()
            return redirect('community:forum_detail', slug=blog.slug)
    return redirect('community:forum_detail', slug=blog.slug)


# 3. FITUR INTERAKTIF (AJAX) & CRUD LANJUTAN

@login_required(login_url='/login/')
def upvote_thread(request, blog_id):
    """Fitur Upvote/Like menggunakan AJAX (tanpa reload halaman)."""
    if request.method == 'POST':
        blog = get_object_or_404(Blog, id=blog_id)
        
        # Jika user sudah pernah upvote, maka batalkan (unlike). Jika belum, tambahkan.
        if request.user in blog.upvoted_by.all():
            blog.upvoted_by.remove(request.user)
            upvoted = False
        else:
            blog.upvoted_by.add(request.user)
            upvoted = True
            
        # Mengembalikan data JSON untuk diproses oleh JavaScript di sisi klien
        return JsonResponse({'upvoted': upvoted, 'upvotes_count': blog.upvoted_by.count()})
    return JsonResponse({'error': 'Permintaan tidak valid'}, status=400)

@login_required(login_url='/login/')
def edit_thread(request, slug):
    """Mengedit thread milik sendiri."""
    blog = get_object_or_404(Blog, slug=slug)
    
    # Keamanan: Tolak jika yang mencoba edit bukan pembuat aslinya
    if request.user != blog.author:
        return redirect('community:forum_detail', slug=slug)
        
    if request.method == 'POST':
        # instance=blog artinya form ini akan berisi data lama yang mau diedit
        form = BlogForm(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('community:forum_detail', slug=blog.slug)
    else:
        form = BlogForm(instance=blog)
        
    return render(request, 'create_thread.html', {'form': form, 'is_edit': True})

@login_required(login_url='/login/')
def delete_thread(request, slug):
    """Menghapus thread milik sendiri."""
    blog = get_object_or_404(Blog, slug=slug)
    
    # Keamanan: Hanya hapus jika user yang login adalah pembuatnya