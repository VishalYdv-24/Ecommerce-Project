from django.contrib import admin
from .models import UserProfile,Order,Category,Product,OrderItem
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Category)
admin.site.register(Product)