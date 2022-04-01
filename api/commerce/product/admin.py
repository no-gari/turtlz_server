from django_summernote.admin import SummernoteModelAdmin
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
    search_fields = ['name']
    readonly_fields = ['slug', 'hits']
    summernote_fields = ('description',)

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, change, **kwargs)
        form.request = request
        return form
