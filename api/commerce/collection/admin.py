from api.commerce.collection.models import CollectionModel
from django.contrib import admin


@admin.register(CollectionModel)
class PopupAdmin(admin.ModelAdmin):
    pass
