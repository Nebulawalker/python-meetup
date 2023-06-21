from django.contrib import admin

from django.contrib.auth import get_user_model


@admin.register(get_user_model())
class UserADmin(admin.ModelAdmin):
    list_display = ['username', 'tg_id', ]
    readonly_fields = ['id']
