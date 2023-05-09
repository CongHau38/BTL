from django.contrib import admin
from .models import Category, Brank, Product
from django.utils.html import mark_safe

class BrankAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category']
    list_filter = ['id', 'name', 'category']

class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'rating', 'created_date', 'quantity', 'price', 'images']
    readonly_fields = ['images']

    def images(self, product):
        return mark_safe("<img src='/static/{img_url}' alt='{alt}' width='120px' />".format(img_url=product.images.name, alt=product.name))

#Regiter
admin.site.register(Category)
admin.site.register(Brank, BrankAdmin)
admin.site.register(Product, ProductAdmin)