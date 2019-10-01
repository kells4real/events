from django.contrib import admin
from .models import *


class HastagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class EventAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


class FeaturedEventAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Hashtag, HastagAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(TicketType)
admin.site.register(State)
admin.site.register(Emails)
admin.site.register(FeaturedEvent, FeaturedEventAdmin)