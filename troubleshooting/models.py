from django.db import models
from django.contrib.auth.models import User

class TroubleshootingArticle(models.Model):
    DEVICE_CHOICES = [
        ('HP', 'Smartphone'),
        ('LAPTOP', 'Laptop'),
        ('TABLET', 'Tablet'),
        ('ALL', 'Semua Perangkat'),
    ]

    CATEGORY_CHOICES = [
        ('BATTERY', 'Baterai & Daya'),
        ('DISPLAY', 'Layar & Visual'),
        ('PERFORMANCE', 'Sistem & Performa Lambat'),
        ('THERMAL', 'Overheating & Suhu'),
        ('HARDWARE', 'Komponen & Fisik'),
    ]

    RECOMMENDATION_CHOICES = [
        ('DIY', 'Servis Mandiri (DIY)'),
        ('TECHNICIAN', 'Bawa ke Teknisi / Upgrade Komponen'),
        ('REPLACE', 'Tukar Tambah / Ganti Perangkat'),
    ]

    DIFFICULTY_CHOICES = [
        ('EASY', 'Mudah (Tanpa Bongkar)'),
        ('MEDIUM', 'Menengah (Butuh Alat Dasar)'),
        ('HARD', 'Sulit (Risiko Tinggi / Teknisi)'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=220)
    device_type = models.CharField(max_length=15, choices=DEVICE_CHOICES, default='ALL')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    
    # Gejala & Penyebab
    symptoms = models.TextField(help_text="Gejala kerusakan yang dialami pengguna")
    causes = models.TextField(help_text="Penyebab utama kerusakan")
    step_by_step_solution = models.TextField(help_text="Langkah penanganan mandiri")

    # Edukasi Kelayakan Servis vs Tukar Tambah
    recommendation = models.CharField(max_length=20, choices=RECOMMENDATION_CHOICES, default='DIY')
    difficulty = models.CharField(max_length=15, choices=DIFFICULTY_CHOICES, default='EASY')
    estimated_cost_min = models.PositiveIntegerField(default=0, help_text="Estimasi biaya minimal (Rp)")
    estimated_cost_max = models.PositiveIntegerField(default=0, help_text="Estimasi biaya maksimal (Rp)")
    when_to_replace = models.TextField(
        help_text="Penjelasan kapan perangkat sebaiknya ditukar tambah daripada diservis"
    )

    # Smart Linking & Metadata
    related_forum_keyword = models.CharField(
        max_length=100, blank=True,
        help_text="Kata kunci untuk mencari thread terkait di modul Community (misal: baterai, overheat)"
    )
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    helpful_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"[{self.get_device_type_display()}] {self.title}"


class ArticleFeedback(models.Model):
    """Mencatat feedback/pengalaman dari Authenticated User pada panduan perbaikan"""
    article = models.ForeignKey(TroubleshootingArticle, on_delete=models.CASCADE, related_name='feedbacks')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_solved = models.BooleanField(default=True, help_text="Apakah panduan ini berhasil mengatasi masalah?")
    actual_repair_cost = models.PositiveIntegerField(null=True, blank=True, help_text="Biaya servis yang dikeluarkan (opsional)")
    comment = models.TextField(max_length=500, help_text="Tips tambahan atau pengalaman servis")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('article', 'user') # 1 user 1 review per artikel

    def __str__(self):
        return f"Feedback {self.user.username} - {self.article.title}"
    
class ArticleBookmark(models.Model):
    """Menyimpan daftar panduan perbaikan favorit (Bookmark) milik Authenticated User"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='troubleshooting_bookmarks')
    article = models.ForeignKey(TroubleshootingArticle, on_delete=models.CASCADE, related_name='bookmarks')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'article')

    def __str__(self):
        return f"{self.user.username} -> {self.article.title}"