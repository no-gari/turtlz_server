from django.contrib import admin
from api.firebase_push.models import PushToken


@admin.register(PushToken)
class PushTokenAdmin(admin.ModelAdmin):
    pass
