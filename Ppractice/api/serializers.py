from rest_framework import serializers
from datetime import datetime

class PublicSerializer(serializers.Serializer):
    stdgCd = serializers.CharField()           # 행정구역코드
    lclgvNm = serializers.CharField()          # 지역명
    pblibId = serializers.CharField()          # 도서관 ID
    pblibNm = serializers.CharField()          # 도서관 이름
    rdrmId = serializers.CharField()           # 열람실 ID
    rdrmNo = serializers.CharField()           # 열람실 번호
    rdrmNm = serializers.CharField()           # 열람실 이름
    rdrmTypeNm = serializers.CharField(allow_blank=True, required=False)  # 열람실 타입
    bldgFlrExpln = serializers.CharField()     # 층수 설명
    nowVstrCnt = serializers.CharField(allow_blank=True, required=False)  # 현재 이용자 수
    tseatCnt = serializers.CharField()         # 전체 좌석 수
    useSeatCnt = serializers.CharField()       # 사용 좌석 수
    rsvtSeatCnt = serializers.CharField()      # 예약 좌석 수
    rmndSeatCnt = serializers.CharField()      # 잔여 좌석 수
    totDt = serializers.CharField()            # 기준 시각
    formattedDate = serializers.SerializerMethodField() # 포맷된 날짜

    def get_formattedDate(self, obj):
        raw = obj.get("totDt", "")
        try:
            dt = datetime.strptime(raw, "%Y%m%d%H%M%S")
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except:
            return None
        
    def to_representation(self, instance):
        lang = self.context.get('language', 'ko')
        data = super().to_representation(instance)

        if lang == 'en':
            return data
        elif lang == 'ko':
            return {
                "행정구역코드": data["stdgCd"],
                "지역명": data["lclgvNm"],
                "도서관 ID": data["pblibId"],
                "도서관 이름": data["pblibNm"],
                "열람실 ID": data["rdrmId"],
                "열람실 번호": data["rdrmNo"],
                "열람실 이름": data["rdrmNm"],
                "열람실 타입": data.get("rdrmTypeNm", ""),
                "층수 설명": data["bldgFlrExpln"],
                "현재 이용자 수": data.get("nowVstrCnt", ""),
                "전체 좌석 수": data["tseatCnt"],
                "사용 좌석 수": data["useSeatCnt"],
                "예약 좌석 수": data["rsvtSeatCnt"],
                "잔여 좌석 수": data["rmndSeatCnt"],
                "기준 시각": data["totDt"],
                "포맷된 날짜": data.get("formattedDate", "")
            }