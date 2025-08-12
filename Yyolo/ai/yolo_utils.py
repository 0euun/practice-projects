from ultralytics import YOLO
import cv2
from pathlib import Path
from collections import Counter

_model = YOLO("ai/models/yolov8n.pt")

def detect_image(src_path: Path, out_dir: Path, conf: float = 0.5, allowed_classes: list[str] = ["person", "book"]):
    out_dir.mkdir(parents=True, exist_ok=True)

    # 1. 클래스 이름 → 클래스 ID 매핑
    all_names = _model.names
    class_ids = [cls_id for cls_id, name in all_names.items() if name in allowed_classes]

    # 2. 추론 실행
    results = _model.predict(
        source=str(src_path),
        conf=conf,
        classes=class_ids,
        save=False,
        verbose=False
    )
    r = results[0]

    # 3. 결과 이미지 저장
    annotated = r.plot()
    out_path = out_dir / f"{src_path.stem}_det.jpg"
    cv2.imwrite(str(out_path), annotated)

    # 4. 객체 정보 추출
    objs = []
    if r.boxes is not None and len(r.boxes) > 0:
        xyxy = r.boxes.xyxy.cpu().numpy()
        cls_ids = r.boxes.cls.int().cpu().tolist()
        confs = r.boxes.conf.cpu().tolist()
        for (x1, y1, x2, y2), cls_id, c in zip(xyxy, cls_ids, confs):
            objs.append({
                "cls_id": int(cls_id),
                "cls_name": all_names[int(cls_id)],
                "conf": float(round(c, 4)),
                "bbox": [float(x1), float(y1), float(x2), float(y2)]
            })

    counts = Counter(o["cls_name"] for o in objs)
    return {
        "output_path": str(out_path),
        "objects": objs,
        "counts": dict(counts),
    }

# ✅ 여기부터 실행 영역
if __name__ == "__main__":
    # 예시: media/test.jpg → media/detections/test_det.jpg
    result = detect_image(
        src_path=Path("media/test.jpg"),
        out_dir=Path("media/detections"),
        conf=0.4,
        allowed_classes=["person", "book"]
    )

    print("✅ 이미지 저장:", result["output_path"])
    print("📦 감지된 객체 개수:", result["counts"])
    for obj in result["objects"]:
        print(obj)
