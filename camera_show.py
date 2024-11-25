import cv2

# Mở camera (index 0 thường là camera mặc định)
cap = cv2.VideoCapture(0)

# Kiểm tra nếu camera được mở thành công
if not cap.isOpened():
    print("Không thể mở camera")
    exit()

# Cấu hình độ phân giải cho video preview
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Độ rộng 640 pixel
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # Độ cao 480 pixel

while True:
    # Đọc từng frame từ camera
    ret, frame = cap.read()

    # Kiểm tra nếu đọc frame thành công
    if not ret:
        print("Không thể đọc frame")
        break

    # Hiển thị frame lên cửa sổ
    cv2.imshow('Camera Preview', frame)

    # Dừng chương trình khi người dùng nhấn phím 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Giải phóng tài nguyên và đóng cửa sổ khi kết thúc
cap.release()
cv2.destroyAllWindows()
