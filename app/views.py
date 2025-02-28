from django.shortcuts import render
# Create your views here.
from rest_framework.viewsets import ModelViewSet
from .serializer import BotUserSerializer, TelegramChannelSerializer
from .models import BotUserModel, TelegramChannelModel,RamadanTime
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
class BotUserViewset(ModelViewSet):
    queryset = BotUserModel.objects.all()
    serializer_class = BotUserSerializer
class GetUser(APIView):
    def post(self,request):
        data = request.data
        data = data.dict()
        if data.get('telegram_id',None):
            try:
                user = BotUserModel.objects.get(telegram_id=data['telegram_id'])
                serializer = BotUserSerializer(user, partial=True)
                return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)
            except BotUserModel.DoesNotExist:
                return Response({'error': 'Not found'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error':'Not found'},status=status.HTTP_204_NO_CONTENT)
class ChangeUserLanguage(APIView):
    def post(self,request):
        data = request.data
        data = data.dict()
        if data.get('telegram_id',None):
            try:
                user = BotUserModel.objects.get(telegram_id=data['telegram_id'])
                user.language = data['language']
                user.save()
                serializer = BotUserSerializer(user, partial=True)
                return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)
            except BotUserModel.DoesNotExist:
                return Response({'error': 'Not found'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error':'Not found'},status=status.HTTP_204_NO_CONTENT)
class TelegramChannelViewset(ModelViewSet):
    queryset = TelegramChannelModel.objects.all()
    serializer_class = TelegramChannelSerializer
class DeleteTelegramChannel(APIView):
    def post(self,request):
        data = request.data
        data = data.dict()
        if data.get('channel_id', None):
            try:
                user = TelegramChannelModel.objects.get(channel_id=data['channel_id'])
                user.delete()
                return Response({'status':"Deleted"},status=status.HTTP_200_OK)
            except TelegramChannelModel.DoesNotExist:
                return Response({'error': 'Not found'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error': 'Not found'}, status=status.HTTP_204_NO_CONTENT)
class GetTelegramChannel(APIView):
    def post(self,request):
        data = request.data
        data = data.dict()
        if data.get('channel_id',None):
            try:
                channel = TelegramChannelModel.objects.get(channel_id=data['channel_id'])
                serializer = TelegramChannelSerializer(channel, partial=True)
                return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)
            except TelegramChannelModel.DoesNotExist:
                return Response({'error': 'Not found'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error':'Not found'},status=status.HTTP_204_NO_CONTENT)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import BotUserModel
from .serializer import BotUserSerializer

class ChangeUserRegion(APIView):
    def post(self, request):
        data = request.data
        telegram_id = data.get("telegram_id")
        region = data.get("region")

        if not telegram_id or not region:
            return Response({"error": "Missing data"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user, created = BotUserModel.objects.get_or_create(telegram_id=telegram_id)
            user.region = region
            user.save()
            return Response({"success": "Region updated"}, status=status.HTTP_200_OK)
        except:
            return Response({"error": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


import base64
from django.http import JsonResponse
from .models import Dua
import random

def get_random_dua(request):
    duas = list(Dua.objects.all())
    if not duas:
        return JsonResponse({"error": "No duas found"}, status=404)

    dua = random.choice(duas)

    # Convert image to Base64
    image_path = dua.image.path
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

    return JsonResponse({
        "image": encoded_image,
        "caption": dua.caption
    })

import datetime
from django.utils.timezone import timedelta


def get_ramadan_time(request, telegram_id, day):
    user = get_object_or_404(BotUserModel, telegram_id=telegram_id)
    target_date = datetime.date.today() if day == "today" else datetime.date.today() + datetime.timedelta(days=1)

    ramadan_time = RamadanTime.objects.filter(region=user.region, date=target_date).first()

    if not ramadan_time:
        return JsonResponse({"error": "No data found for this region and date"}, status=404)

    return JsonResponse({
        "suhoor_time": ramadan_time.suhoor_time.strftime("%H:%M"),  # ✅ Add Suhoor time
        "iftar_time": ramadan_time.iftar_time.strftime("%H:%M"),
        "image": ramadan_time.image_base64,  # ✅ Use the Base64 property
        "caption": ramadan_time.caption
    })


def get_all_users(request):
    users = BotUserModel.objects.all().values("telegram_id", "region")  # ✅ Get users with region info
    return JsonResponse(list(users), safe=False)


import base64
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import MonthlyRamadanTime
import traceback

def get_monthly_times(request):
    """Fetch the monthly Ramadan times and return image + caption."""
    try:
        # Fetch first available record
        ramadan_data = MonthlyRamadanTime.objects.first()

        if not ramadan_data:
            return JsonResponse({"error": "No data available"}, status=404)

        # ✅ Check if the image exists
        if not ramadan_data.image or not ramadan_data.image.path:
            return JsonResponse({"error": "Image file missing"}, status=500)

        # ✅ Read image as base64
        try:
            with open(ramadan_data.image.path, "rb") as img_file:
                image_base64 = base64.b64encode(img_file.read()).decode("utf-8")
        except FileNotFoundError:
            return JsonResponse({"error": "Image file not found"}, status=500)

        return JsonResponse({
            "image": image_base64,
            "caption": ramadan_data.caption
        }, status=200)

    except Exception as e:
        print("🔥 ERROR:", str(e))
        print(traceback.format_exc())  # ✅ Show full error traceback in logs
        return JsonResponse({"error": str(e)}, status=500)