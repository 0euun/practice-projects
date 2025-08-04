import cv2
import numpy as np

def analyze_seat(image, yolo_net, conf_threshold=0.4, nms_threshold=0.3):
    height, width = image.shape[:2]

    # 1. 전처리
    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (640, 640), swapRB=True, crop=False)
    yolo_net.setInput(blob)

    # 2. 추론
    outputs = yolo_net.forward(yolo_net.getUnconnectedOutLayersNames())
    outputs = outputs[0] if isinstance(outputs, (tuple, list)) else outputs
    outputs = outputs.squeeze(0)

    boxes = []
    confidences = []
    class_ids = []

    for row in outputs:
        x, y, w, h = row[0:4]
        objectness = row[4]
        class_scores = row[5:]

        class_id = np.argmax(class_scores)
        confidence = class_scores[class_id] * objectness

        if confidence > conf_threshold:
            cx, cy = int(x * width), int(y * height)
            w, h = int(w * width), int(h * height)
            x1 = int(cx - w / 2)
            y1 = int(cy - h / 2)

            boxes.append([x1, y1, w, h])
            confidences.append(float(confidence))
            class_ids.append(class_id)

    # 3. NMS 적용
    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)
    detected = [class_ids[i] for i in indices.flatten()] if len(indices) > 0 else []

    # 4. 좌석 상태 판단
    if 0 in detected:  # COCO: 0번 클래스 = 'person'
        return "사람 있음"
    elif detected:
        return "짐만 있음"
    else:
        return "비어 있음"
