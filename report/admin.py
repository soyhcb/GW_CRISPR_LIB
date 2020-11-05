from django.contrib import admin

from report.models import Report

# Register your models here.
class ReportAdmin(admin.ModelAdmin):
    list_filter = ('category', 'solved', "marked")
    list_display = ('name', "category", 'problem', "solved", "marked", "time")
    fieldsets = [
        ('Admin', {'fields': [('solved', 'marked')]}),
        ('User Info', {'fields': ['name', 'email']}),
        ('Problem', {'fields': ['time', 'category', 'problem', 'detail']}),
    ]
    readonly_fields = ('time', )

admin.site.register(Report, ReportAdmin)
