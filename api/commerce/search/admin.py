from django.contrib import admin
from .models import SearchKeywords


@admin.register(SearchKeywords)
class SearchKeywordAdmin(admin.ModelAdmin):
    pass
