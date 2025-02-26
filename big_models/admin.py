from django.contrib import admin
from .models import AIModelLink

@admin.register(AIModelLink)
class AIModelLinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'description', 'created_at', 'order','click_count')
    list_editable = ('order',)