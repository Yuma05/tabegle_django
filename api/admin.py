from django.contrib import admin

from .models import Shop, Search, Place, Category, UserShop

admin.site.register(Shop)
admin.site.register(Search)
admin.site.register(Place)
admin.site.register(Category)
admin.site.register(UserShop)
