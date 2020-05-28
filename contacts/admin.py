from django.contrib import admin
from .models import Contact

# Register your models here.
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'fullname', 'email', 'message', 'contact_date')
    list_display_links = ('id', 'fullname')
    list_filter = ('fullname', 'contact_date')
    search_fields = ('fullname', 'email')
    list_per_page = 25

admin.site.register(Contact, ContactAdmin)
# Register your models here.
