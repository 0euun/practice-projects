from rest_framework import views
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import render
from django.conf import settings
from .serializers import *
import requests

class PublicAPI(views.APIView):
    def get(self, request):
        url = "http://apis.data.go.kr/B551982/plr/rlt_rdrm_info"
        params = {
            "serviceKey": settings.DECODING_KEY,
            "type": "json",
            "pageNo": "1",
            "numOfRows": "10",
            # "stdgCd": "1168000000", # 행정구역코드 삭제
        }

        try:

            headers = {
                'User-Agent': 'Mozilla/5.0'
            }
            response = requests.get(url, params=params, headers=headers, verify=False)
            if response.status_code != 200:
                return Response({"error": "Failed to fetch data from the external API."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            data = response.json()
            items = data.get("body", {}).get("item", [])
            lang = request.GET.get("lang", "ko")

            serializer = PublicSerializer(items, many=True, context={"language": lang})
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        except Exception as e:
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
