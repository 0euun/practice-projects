# myapp/views.py
from pathlib import Path
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import (
    DetectRequestSerializer,
    DetectResponseSerializer,
)
from ai.yolo_utils import detect_image

class DetectFromMediaView(APIView):
    """
    POST /api/detect-from-media/
    {
        "filename": "test.jpg",
        "conf": 0.5
    }
    """
    def post(self, request):
        # 1) 요청 검증
        req_ser = DetectRequestSerializer(data=request.data)
        req_ser.is_valid(raise_exception=True)
        filename = req_ser.validated_data["filename"]
        conf = req_ser.validated_data["conf"]

        # 2) 안전한 경로 구성 + 존재 여부 확인
        media_root = Path(settings.MEDIA_ROOT).resolve()
        src_path = (media_root / filename).resolve()
        if media_root not in src_path.parents and media_root != src_path.parent:
            return Response({"detail": "Invalid path."}, status=status.HTTP_400_BAD_REQUEST)
        if not src_path.exists():
            return Response({"detail": f"File not found: {src_path.name}"}, status=status.HTTP_404_NOT_FOUND)

        # 3) 추론 실행
        out_dir = media_root / "detections"
        result = detect_image(src_path=src_path, out_dir=out_dir, conf=conf)

        # 4) URL 변환
        rel_output = Path(result["output_path"]).relative_to(media_root)
        result_url = f"{settings.MEDIA_URL}{rel_output.as_posix()}"

        # 5) 응답 데이터 구성 → 응답 시리얼라이저로 직렬화
        resp_payload = {
            "input": filename,
            "result_image_url": result_url,
            "counts": result["counts"],
            "objects": result["objects"],
        }
        resp_ser = DetectResponseSerializer(resp_payload)
        return Response(resp_ser.data, status=status.HTTP_200_OK)
