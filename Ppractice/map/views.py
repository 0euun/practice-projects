import os
import re
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .serializers import LibrarySerializer

def extract_keywords(name):
    # """도서관 이름에서 핵심 키워드만 추출"""
    name = re.sub(r'<.*?>', '', name)          # <b>태그 제거
    name = re.sub(r'\(.*?\)', '', name)        # 괄호 제거
    name = re.sub(r'도서관$', '', name)        # 접미어 제거 (선택)
    name = name.strip()
    return re.findall(r'[가-힣]+', name)        # 한글 단어 추출

class LibrarySearchView(APIView):
    def get(self, request):
        region = request.query_params.get('region')
        if not region:
            return Response({"error": "region 파라미터가 필요합니다."}, status=status.HTTP_400_BAD_REQUEST)

        # 네이버 지역 검색 API
        query = f"{region} 도서관"
        local_url = "https://openapi.naver.com/v1/search/local.json"
        headers = {
            "X-Naver-Client-Id": settings.NAVER_CLIENT_ID,
            "X-Naver-Client-Secret": settings.NAVER_CLIENT_SECRET,
        }
        params = {
            "query": query,
            "display": 5,
            "sort": "random"
        }

        try:
            local_response = requests.get(local_url, headers=headers, params=params)
            local_response.raise_for_status()
        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_502_BAD_GATEWAY)

        items = local_response.json().get('items', [])
        result = []

        for item in items:
            raw_title = item["title"]
            title_clean = raw_title.replace("<b>", "").replace("</b>", "")
            address = item["address"]

            print(f"[DEBUG] title: {title_clean}")
            library_info = self.get_library_info_by_keywords(address, title_clean)

            result.append({
                "title": title_clean,
                "link": item.get("link"),
                "category": item.get("category"),
                "description": item.get("description"),
                "telephone": item.get("telephone"),
                "address": item["address"],
                "roadAddress": item.get("roadAddress"),
                "mapx": item.get("mapx"),
                "mapy": item.get("mapy"),
                "map_url": f"https://map.naver.com/v5/search/{title_clean}",
                "open_time": library_info.get("openTime", "정보 없음"),
                "close_day": library_info.get("closeDay", "정보 없음"),
                "facility": library_info.get("facility", "정보 없음"),
            })


        serializer = LibrarySerializer(result, many=True)
        return Response(serializer.data)

    def get_library_info_by_keywords(self, address, lib_title):
        api_key = settings.LIBRARY_API_KEY
        address_parts = address.split()
        if len(address_parts) < 2:
            print(f"[WARN] 주소 분석 실패: {address}")
            return {}

        region = address_parts[0]        # ex. 경기도
        dtl_region = address_parts[1]    # ex. 파주시
        keywords = extract_keywords(lib_title)

        for keyword in keywords:
            url = "http://data4library.kr/api/libSrch"
            params = {
                "authKey": api_key,
                "libName": keyword,
                "region": region,
                "dtl_region": dtl_region,
                "format": "json",
                "pageSize": 20
            }

            try:
                res = requests.get(url, params=params)
                res.raise_for_status()
                libs = res.json().get("response", {}).get("libs", [])

                for item in libs:
                    lib = item.get("lib", {})
                    lib_name = lib.get("libName", "")
                    if all(k in lib_name for k in keywords):
                        return {
                            "openTime": lib.get("operatingTime"),
                            "closeDay": lib.get("closeDay"),
                            "facility": lib.get("facility")
                        }

            except Exception as e:
                print(f"[ERROR] 공공 API 호출 실패 ({keyword}): {e}")

        print(f"[WARN] 키워드 기반 매칭 실패: '{lib_title}'")
        return {}
