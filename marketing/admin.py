from django.contrib import admin
from .models import EmailSubscribe
# Register your models here.

@admin.register(EmailSubscribe)
class MarketingAdmin(admin.ModelAdmin):
    """ Admin View for CategorieAdmin """
    list_display = ('email', 'timestamp')
    list_display_links = ('email',)
    ordering = ['timestamp']
    search_fields = ['timestamp']
