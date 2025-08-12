# myapp/serializers.py
from rest_framework import serializers

# ✅ 요청 바디
class DetectRequestSerializer(serializers.Serializer):
    filename = serializers.CharField()                  # 예: "test.jpg"
    conf = serializers.FloatField(required=False, min_value=0.05, max_value=0.95, default=0.5)

    def validate_filename(self, value):
        # 간단 확장자 체크 (필요시 더 강화)
        allowed = {".jpg", ".jpeg", ".png", ".bmp"}
        import os
        ext = os.path.splitext(value)[1].lower()
        if ext not in allowed:
            raise serializers.ValidationError(f"허용 확장자: {', '.join(sorted(allowed))}")
        return value


# ✅ 단일 객체(디텍션) 표현
class DetectionObjectSerializer(serializers.Serializer):
    cls_id = serializers.IntegerField()
    cls_name = serializers.CharField()
    conf = serializers.FloatField()
    bbox = serializers.ListField(
        child=serializers.FloatField(),
        min_length=4, max_length=4,
        help_text="[x1,y1,x2,y2] (pixel, float)"
    )

# ✅ counts: {"person": 3, "chair": 2} 같은 맵 구조
class DetectionCountsField(serializers.DictField):
    child = serializers.IntegerField()

# ✅ 응답 전체
class DetectResponseSerializer(serializers.Serializer):
    input = serializers.CharField()                     # 요청 filename 그대로
    result_image_url = serializers.CharField()          # /media/detections/xxx_det.jpg
    counts = DetectionCountsField()
    objects = DetectionObjectSerializer(many=True)
