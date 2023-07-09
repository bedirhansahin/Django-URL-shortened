from django.contrib import admin
from .models import URLData


# Admin Model for URLData
@admin.register(URLData)
class URLDataAdmin(admin.ModelAdmin):
    list_display = ["url", "shortened_url"]

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()
