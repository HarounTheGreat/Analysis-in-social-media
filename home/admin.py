from django.contrib import admin
from home .models import ContactMessage,Settings,AccessTokenFB


# Register your models here.


class SettingsAdmin(admin.ModelAdmin):
    list_display=['title','company','update_at','status']

class ContactMessageAdmin(admin.ModelAdmin):
    list_display=['name','subject','update_at','status']
    reandonly_fileds=('name','subject','email','message','ip')
    list_filter=['status']


class AccessTokenAdmin(admin.ModelAdmin):
    list_display=['token']


admin.site.register(AccessTokenFB,AccessTokenAdmin)
admin.site.register(Settings,SettingsAdmin)
admin.site.register(ContactMessage,ContactMessageAdmin)
