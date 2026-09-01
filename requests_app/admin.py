from django.contrib import admin

from .models import BusinessRequest


@admin.register(BusinessRequest)
class BusinessRequestAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "status", "created_at")
    list_filter = ("category", "status")
    search_fields = ("title", "description", "action_plan")

# Register your models here.
