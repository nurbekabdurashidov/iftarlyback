from django.contrib import admin
from .models import *
# Register your models here.
from .models import BotUserModel,TelegramChannelModel
@admin.register(BotUserModel)
class BotUserAdmin(admin.ModelAdmin):
    list_display = ['name','telegram_id','language','added']
    list_editable = ['language','name']
    list_display_links = ['telegram_id']
    list_per_page = 10
@admin.register(TelegramChannelModel)
class TelegramChannelAdmin(admin.ModelAdmin):
    list_display = ['channel_id','channel_name','channel_members_count']
    list_display_links = ['channel_name']
    list_per_page = 10


@admin.register(Dua)
class DuaAdmin(admin.ModelAdmin):
    list_display = ("id", "caption")

@admin.register(RamadanTime)
class RamadanTimeAdmin(admin.ModelAdmin):
    list_display = ("region", "date", "suhoor_time", "iftar_time")
    search_fields = ("region", "date")
    list_filter = ("region", "date")
    ordering = ("-date",)

@admin.register(MonthlyRamadanTime)
class MonthlyRamadanTimeAdmin(admin.ModelAdmin): # Filter options in the admin panel
    readonly_fields = ("created_at",)  # Prevent modification of created_at