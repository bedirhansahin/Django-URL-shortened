from django.contrib import admin
from .models import URLData


# Admin Model for URLData
@admin.register(URLData)
class URLDataAdmin(admin.ModelAdmin):
    list_display = ["user", "url", "shortened_url", "click_count", "created_at", "last_click_at"]

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()
