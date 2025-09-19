from django.contrib import admin
from .models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "content", "preview", "created_at")
    list_filter = ("created_at", "is_published", "views_count")
    search_fields = ("title", "created_at", "views_count")
