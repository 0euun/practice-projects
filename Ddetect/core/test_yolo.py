import cv2
import os
from yolo_utils import analyze_seat

# 좌표 정의
SEAT_COORDS = {
    "A1": (53, 106, 286, 252),  # 좌측 / 좌측 상단
    "A2": (12, 249, 246, 413),  # 좌측 / 좌측 하단
    "A3": (285, 94, 513, 253),  # 좌측 / 우측 상단
    "A4": (244, 255, 511, 437),  # 좌측 / 우측 하단
    "B1": (632, 97, 857, 209),  # 우측 / 좌측 상단
    "B2": (643, 219, 935, 490),  # 우측 / 좌측 하단
    "B3": (847, 54, 1123, 203),  # 우측 / 우측 상단
    "B4": (939, 208, 1217, 453),  # 우측 / 우측 하단
}

# 모델 로드
model_path = os.path.join("Ddetect", "yolov8n.onnx")
yolo_net = cv2.dnn.readNetFromONNX(model_path)

# 이미지 불러오기
img_path = os.path.join("Ddetect", "media", "frames", "f1.png")
img = cv2.imread(img_path)

if img is None:
    raise FileNotFoundError(f"이미지를 불러올 수 없습니다: {img_path}")

# 각 좌석 분석
print("=== 좌석 상태 로그 ===")
for seat_id, (x1, y1, x2, y2) in SEAT_COORDS.items():
    seat_roi = img[y1:y2, x1:x2]
    status = analyze_seat(seat_roi, yolo_net)
    print(f"{seat_id}: {status}")
