from django_summernote.admin import SummernoteModelAdmin
from django.utils.safestring import mark_safe
from api.commerce.product import models
from django.contrib import admin
from django import forms
import re


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = models.Product
        fields = '__all__'

    def save(self, commit=True):
        try:
            self.instance.user = self.request.user

            instance = super().save(commit=False)
            instance.save()

            content = self.cleaned_data['content']
            img_contents = re.findall(r'django-summernote/.*?"', content)
            for img in img_contents:
                imgs_path = img[0:len(img) - 1]
                summernote = models.Summernote.objects.get(file=imgs_path)
                summernote.document = instance
                summernote.save()
        except:
            instance = super().save(commit=False)

        return instance


@admin.register(models.ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Product)
class ProductAdmin(SummernoteModelAdmin):
    form = ProductAdminForm
    search_fields = ('name',)
    summernote_fields = ('description',)

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, change, **kwargs)
        form.request = request
        return form


@admin.register(models.Files)
class FilesAdmin(admin.ModelAdmin):
    list_display = ('product', 'file', 'org_file_name', 'created_at', 'updated_at',)
    list_display_links = ('product',)
    list_filter = ['product']
    search_fields = ('org_file_name',)
    readonly_fields = ['file_image_small']
    autocomplete_fields = ['product']

    def file_image_small(self, obj):
        if obj.org_file_name != '':
            file_ext = obj.org_file_name.split('.')[1]
            if file_ext in ['jpg', 'jpeg', 'png', 'gif', 'bmp']:
                return mark_safe('<img src="{url}" height="100" />'.format(url=obj.file.url))
            else:
                return mark_safe('this is not image')

    file_image_small.short_description = '이미지'


@admin.register(models.Summernote)
class SummernoteAdmin(admin.ModelAdmin):
    list_display = ('get_id', 'product', 'name', 'file', 'uploaded',)
    list_display_links = ('product', 'name',)
    readonly_fields = ['product', 'name', 'file_image_small']
    autocomplete_fields = ['product']

    def get_id(self, obj):
        return obj.id

    get_id.short_description = 'ID'

    def file_image_small(self, obj):
        if obj.name != '':
            file_ext = obj.name.split('.')[1]
            if file_ext in ['jpg', 'jpeg', 'png', 'gif', 'bmp']:
                return mark_safe('<img src="{url}" height="100" />'.format(url=obj.file.url))
            else:
                return mark_safe('this is not image')

    file_image_small.short_description = '이미지'
