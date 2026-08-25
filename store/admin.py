from django.contrib import admin

from . import models

@admin.register(models.Product)
class ProductAdminn(admin.ModelAdmin):
    list_display = ["title", "amount", "inventory"]
    list_editable = ["inventory"]
    list_filter = ["amount", "membership", "collection"]
    search_fields = ["title__istartswith"] # i for case-insensitive
    # list_per_page = 10 - this makes the list paginated
    # readonly_fields = ["title"] - used to set readonly fields while creating this obj
    prepopulated_fields = {
        "slug": ["title"]
    }
    autocomplete_fields = ["collection"] # instead of having a drop down, incase we have 100s of collections, we can auto-complete while filling the collection field



@admin.register(models.Collection)
class CollectionAdminn(admin.ModelAdmin):
    search_fields = ["title"]   


admin.site.register(models.Promotion)
admin.site.register(models.Customer)
admin.site.register(models.Address)
admin.site.register(models.Order)
admin.site.register(models.OrderItem)
admin.site.register(models.Cart)
admin.site.register(models.CartItem)
