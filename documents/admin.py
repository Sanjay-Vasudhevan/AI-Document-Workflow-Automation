from django.contrib import admin
from .models import Document

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_by', 'uploaded_at', 'status', 'ai_priority')
    list_filter = ('status', 'ai_priority', 'ai_category')