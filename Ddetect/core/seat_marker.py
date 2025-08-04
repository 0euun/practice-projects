import cv2

# 이미지 불러오기
image_path = 'Ddetect/media/frames/f1.png'
img = cv2.imread(image_path)
clone = img.copy()

drawing = False
start_point = ()
seat_index = 1
coords = {}

def draw_rectangle(event, x, y, flags, param):
    global drawing, start_point, seat_index

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        start_point = (x, y)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        end_point = (x, y)
        cv2.rectangle(img, start_point, end_point, (0, 255, 0), 2)
        seat_id = f"Seat{seat_index}"
        coords[seat_id] = (*start_point, *end_point)
        seat_index += 1
        print(f'"{seat_id}": {(*start_point, *end_point)},')  # 터미널 출력용

cv2.namedWindow("Image")
cv2.setMouseCallback("Image", draw_rectangle)

while True:
    cv2.imshow("Image", img)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("r"):  # R 누르면 리셋
        img = clone.copy()
        coords.clear()
        seat_index = 1
        print("Reset")
    elif key == ord("q"):  # Q 누르면 종료
        break

cv2.destroyAllWindows()