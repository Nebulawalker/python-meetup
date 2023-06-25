from django.contrib import admin

from .models import Donation, Issue, Report, Survey


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


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'specialization',
        'region',
    ]
    readonly_fields = ['created_at', 'modified_at']
    ordering = ['-modified_at']


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'amount',
        'created_at',
    ]
    readonly_fields = ['created_at', 'id']
    ordering = ['-created_at']
