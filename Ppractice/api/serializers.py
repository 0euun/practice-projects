from rest_framework import serializers

class PublicSerializer(serializers.Serializer):
    stdgCd = serializers.CharField()           # 행정구역코드
    lclgvNm = serializers.CharField()          # 지역명 (전북 익산시)
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
    totDt = serializers.CharField()            # 기준 시각 (예: 20250727164032)