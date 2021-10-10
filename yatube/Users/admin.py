from django.contrib import admin
from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("avatar", 'user')
    search_fields = ("user",)
    list_filter = ("user",)
    empty_value_display = "-пусто-"


admin.site.register(UserProfile, UserProfileAdmin)
