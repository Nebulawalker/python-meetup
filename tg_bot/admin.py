from django.contrib import admin

from .models import Report, Issue


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    readonly_fields = [
        'id',
    ]

    list_display = [
        'speaker',
        'topic',
        'starts_at',
        'ends_at',
        'is_current',
    ]

    ordering = ['starts_at']


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    readonly_fields = [
        'id',
    ]

    list_display = [
        'from_whom',
        'report',
        'status',
    ]

    ordering = ['asked_at']
