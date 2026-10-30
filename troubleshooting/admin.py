from django.contrib import admin
from .models import TroubleshootingArticle, ArticleFeedback, ArticleBookmark

@admin.register(TroubleshootingArticle)
class TroubleshootingArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'device_type', 'category', 'recommendation', 'difficulty', 'created_at')
    list_filter = ('device_type', 'category', 'recommendation', 'difficulty')
    search_fields = ('title', 'symptoms', 'causes', 'related_forum_keyword')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(ArticleFeedback)
class ArticleFeedbackAdmin(admin.ModelAdmin):
    list_display = ('article', 'user', 'is_solved', 'actual_repair_cost', 'created_at')
    list_filter = ('is_solved', 'created_at')
    search_fields = ('comment', 'user__username', 'article__title')

@admin.register(ArticleBookmark)
class ArticleBookmarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'article', 'created_at')
    search_fields = ('user__username', 'article__title')