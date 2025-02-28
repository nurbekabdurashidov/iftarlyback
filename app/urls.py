from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import *
router = DefaultRouter()
router.register('botuser',BotUserViewset)
router.register('channels',TelegramChannelViewset)
urlpatterns = [
    path('',include(router.urls)),
    path('user/',GetUser.as_view()),
    path('lang/',ChangeUserLanguage.as_view()),
    path('channel/',GetTelegramChannel.as_view()),
    path('delete_channel/',DeleteTelegramChannel.as_view()),
    path('change_user_region/', ChangeUserRegion.as_view(), name="change_user_region"),
    path("get_dua/", get_random_dua, name="get_dua"),
    path("get_ramadan_time/<int:telegram_id>/<str:day>/", get_ramadan_time, name="get_ramadan_time"),
    path("get_all_users/", get_all_users, name="get_all_users"),
    path("get_monthly_times/", get_monthly_times, name="get_monthly_times"),
]
