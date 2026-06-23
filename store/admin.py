from django.contrib import admin

from .models import Category, Customer, Order, OrderItem, Product, ShippingAddress


class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "category", "stock", "digital")
    list_filter = ("category", "digital")
    search_fields = ("name", "description")
    # Slug prepopulation commented out — Product model has no slug field yet
    # prepopulated_fields = {"slug": ("name",)}


class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "date_ordered", "complete", "transaction_id")
    list_filter = ("complete", "date_ordered")
    search_fields = ("transaction_id", "customer__name", "customer__email")


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("product", "order", "quantity", "get_total", "date_added")


class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "user")
    search_fields = ("name", "email")


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name",)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(ShippingAddress)
