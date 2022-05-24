from django.contrib import admin
from api.user.models import User, Profile
from django import forms


class UserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('phone', 'email')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    form = UserAdminForm
    list_display = ('phone', 'email')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'kind', 'code', 'user', 'firebase_token')
