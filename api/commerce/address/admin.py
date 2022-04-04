from api.commerce.address.models import Address
from django.contrib import admin


@admin.register(Address)
class AddressAdmin(admin.modelAdmin):
    pass
