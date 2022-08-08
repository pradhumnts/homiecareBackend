from django.contrib import admin
from .models import *

class UserAdmin(admin.ModelAdmin):
    list_display = ('phoneNumber', 'email', 'pk', "city", "create_at")
    search_fields = ['first_name', 'last_name', 'phoneNumber' ]

class NurseAdmin(admin.ModelAdmin):
    list_display = ("id", "user")
    search_fields = ["user__first_name"]

class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "user_from", "user_to", "text")

admin.site.register(User, UserAdmin)
admin.site.register(Nurse, NurseAdmin)
admin.site.register(Address)
admin.site.register(Qualification)
admin.site.register(Message, MessageAdmin)
admin.site.register(Review)