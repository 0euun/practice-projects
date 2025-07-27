from rest_framework import views
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import render
from django.conf import settings
from .serializers import *
import requests

ENCODING_KEY = settings.ENCODING_KEY
DECODING_KEY = settings.DECODING_KEY

class PublicAPI(views.APIView):
    def get(self, request):
        url = "https://apis.data.go.kr/B551982/plr"
        params = {
            "serviceKey": DECODING_KEY,
            "type": "json",
            "pageNo": "1",
            "numOfRows": "10",
            "stdgCd": "1141000000",
        }

        try:
            response = requests.get(url, params=params)
            if response.status_code != 200:
                return Response({"error": "Failed to fetch data from the external API."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            data = response.json()
            items = data.get("body", {}).get("item", [])

            serializer = PublicSerializer(items, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        except Exception as e:
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
