from django.contrib import admin
from .models import Contact, EmailList

# Register your models here.

class ContactAdmin(admin.ModelAdmin):
    list_display=('emaillist','email')
    list_filter = ('emaillist',)
    search_fields = ('email', )

admin.site.register(Contact, ContactAdmin)
admin.site.register(EmailList)