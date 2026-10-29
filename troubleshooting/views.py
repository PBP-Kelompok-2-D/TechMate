from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Q, Avg, Count
from django.utils.html import strip_tags

from .models import TroubleshootingArticle, ArticleFeedback, ArticleBookmark
from .forms import ArticleFeedbackForm


def troubleshooting_list(request):
    """Halaman utama direktori Troubleshooting (Guest & Authenticated)"""
    articles = TroubleshootingArticle.objects.all().order_by('-created_at')
    
    bookmarked_ids = []
    if request.user.is_authenticated:
        bookmarked_ids = list(
            ArticleBookmark.objects.filter(user=request.user).values_list('article_id', flat=True)
        )

    context = {
        'articles': articles,
        'bookmarked_ids': bookmarked_ids,
        'device_choices': TroubleshootingArticle.DEVICE_CHOICES,
        'category_choices': TroubleshootingArticle.CATEGORY_CHOICES,
        'recommendation_choices': TroubleshootingArticle.RECOMMENDATION_CHOICES,
    }
    return render(request, 'troubleshooting/article_list.html', context)


def filter_articles_ajax(request):
    query = request.GET.get('q', '').strip()
    device = request.GET.get('device', '')
    category = request.GET.get('category', '')
    bookmarked_only = request.GET.get('bookmarked', '') == 'true'

    # Mulai dengan semua artikel
    articles = TroubleshootingArticle.objects.all().order_by('-created_at')

    # Terapkan filter SATU PER SATU
    if query:
        articles = articles.filter(Q(title__icontains=query) | Q(symptoms__icontains=query) | Q(causes__icontains=query))
    
    if device:
        # Tampilkan perangkat spesifik ATAU yang bersifat 'ALL'
        articles = articles.filter(device_type__in=[device, 'ALL'])
        
    if category:
        articles = articles.filter(category=category)
        
    if bookmarked_only and request.user.is_authenticated:
        articles = articles.filter(bookmarks__user=request.user)

    # Ambil data bookmark user untuk indikator bintang
    bookmarked_ids = set()
    if request.user.is_authenticated:
        bookmarked_ids = set(ArticleBookmark.objects.filter(user=request.user).values_list('article_id', flat=True))

    data = []
    for art in articles:
        data.append({
            'id': art.id,
            'title': art.title,
            'slug': art.slug,
            'device_type': art.get_device_type_display(),
            'category': art.get_category_display(),
            'recommendation_code': art.recommendation, # Asli dari DB
            'recommendation_label': art.get_recommendation_display(),
            'symptoms_preview': art.symptoms[:100] + '...' if len(art.symptoms) > 100 else art.symptoms,
            'estimated_cost_min': art.estimated_cost_min,
            'estimated_cost_max': art.estimated_cost_max,
            'is_bookmarked': art.id in bookmarked_ids,
        })
        
    return JsonResponse({'articles': data, 'count': len(data)})


def article_detail(request, slug):
    """Halaman detail diagnosis, edukasi kelayakan servis vs tukar tambah, dan catatan komunitas"""
    article = get_object_or_404(TroubleshootingArticle, slug=slug)
    feedbacks = article.feedbacks.select_related('user').order_by('-created_at')

    # Statistik pengalaman servis dari pengguna
    stats = feedbacks.aggregate(
        avg_actual_cost=Avg('actual_repair_cost'),
        total_reviews=Count('id'),
        solved_count=Count('id', filter=Q(is_solved=True))
    )
    success_rate = 0
    if stats['total_reviews'] > 0:
        success_rate = int((stats['solved_count'] / stats['total_reviews']) * 100)

    is_bookmarked = False
    user_feedback = None
    if request.user.is_authenticated:
        is_bookmarked = ArticleBookmark.objects.filter(user=request.user, article=article).exists()
        user_feedback = feedbacks.filter(user=request.user).first()

    form = ArticleFeedbackForm(instance=user_feedback)

    context = {
        'article': article,
        'feedbacks': feedbacks,
        'avg_actual_cost': int(stats['avg_actual_cost']) if stats['avg_actual_cost'] else None,
        'total_reviews': stats['total_reviews'],
        'success_rate': success_rate,
        'is_bookmarked': is_bookmarked,
        'user_feedback': user_feedback,
        'form': form,
    }
    return render(request, 'troubleshooting/article_detail.html', context)


@login_required
@require_POST
def toggle_bookmark_ajax(request, article_id):
    """Endpoint AJAX POST untuk menyimpan/menghapus Bookmark panduan perbaikan"""
    article = get_object_or_404(TroubleshootingArticle, id=article_id)
    bookmark, created = ArticleBookmark.objects.get_or_create(user=request.user, article=article)

    if not created:
        bookmark.delete()
        return JsonResponse({'status': 'removed', 'is_bookmarked': False, 'message': 'Dihapus dari Bookmark'})

    return JsonResponse({'status': 'saved', 'is_bookmarked': True, 'message': 'Disimpan ke Bookmark'})


@login_required
@require_POST
def submit_feedback_ajax(request, article_id):
    """Endpoint AJAX POST untuk mengirim atau memperbarui catatan pengalaman servis"""
    article = get_object_or_404(TroubleshootingArticle, id=article_id)
    existing_feedback = ArticleFeedback.objects.filter(article=article, user=request.user).first()

    form = ArticleFeedbackForm(request.POST, instance=existing_feedback)
    if form.is_valid():
        feedback = form.save(commit=False)
        feedback.article = article
        feedback.user = request.user
        feedback.comment = strip_tags(feedback.comment)
        feedback.save()

        return JsonResponse({
            'status': 'success',
            'message': 'Catatan pengalaman servis berhasil disimpan!',
            'feedback': {
                'id': feedback.id,
                'username': feedback.user.username,
                'is_solved': feedback.is_solved,
                'actual_repair_cost': feedback.actual_repair_cost,
                'comment': feedback.comment,
                'created_at': feedback.created_at.strftime('%d %b %Y'),
            }
        })

    return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)


@login_required
@require_POST
def delete_feedback_ajax(request, feedback_id):
    """Endpoint AJAX POST untuk menghapus catatan servis milik pengguna sendiri"""
    feedback = get_object_or_404(ArticleFeedback, id=feedback_id, user=request.user)
    feedback.delete()
    return JsonResponse({'status': 'deleted', 'message': 'Catatan pengalaman servis berhasil dihapus.'})