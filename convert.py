import cv2
import torch
import pyrealsense2 as rs
import numpy as np

# YOLOv5 모델 로드
model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt')

# Realsense 카메라 설정
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

# Realsense 카메라 시작
pipeline.start(config)

# 카메라 캘리브레이션 정보 로드
calibration_file = 'camera_calibration.xml'
calibration_data = cv2.FileStorage(calibration_file, cv2.FILE_STORAGE_READ)
camera_matrix = calibration_data.getNode("camera_matrix").mat()
dist_coeffs = calibration_data.getNode("dist_coeffs").mat()
calibration_data.release()

while True:
    # 프레임 가져오기
    frames = pipeline.wait_for_frames()
    color_frame = frames.get_color_frame()
    depth_frame = frames.get_depth_frame()
    if not color_frame or not depth_frame:
        continue
    color_image = np.asanyarray(color_frame.get_data())
    depth_image = np.asanyarray(depth_frame.get_data())

    # YOLOv5를 사용하여 물체 감지
    results = model(color_image)

    # 검출된 물체의 좌표와 클래스 출력
    tomato_count = 0  # 검출된 토마토 개수 초기화

    for detection in results.xyxy[0]:
        if detection[5] == 0:  # "tomato" 클래스 라벨을 나타내는 인덱스
            x, y, w, h = detection[:4]
            label = f"{results.names[int(detection[5])]}: {detection[4]:.2f}"
            cv2.rectangle(color_image, (int(x), int(y)), (int(w), int(h)), (0, 255, 0), 2)
            cv2.putText(color_image, label, (int(x), int(y) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            # 물체의 중심 좌표 계산
            center_x = int((x + w) / 2)
            center_y = int((y + h) / 2)

            # 물체의 3D 좌표 계산
            depth = depth_image[center_y, center_x].astype(float)
            depth_scale = pipeline.get_active_profile().get_device().first_depth_sensor().get_depth_scale()
            depth_in_meters = depth * depth_scale
            # 물체의 중심에 점 그리기
            cv2.circle(color_image, (center_x, center_y), 3, (0, 0, 255), -1)
            # 2D 좌표를 3D 좌표로 변환
            point_2D = np.array([[center_x, center_y]], dtype=np.float32)
            point_3D = cv2.undistortPoints(point_2D, camera_matrix, dist_coeffs)
            point_3D = np.concatenate((point_3D[0][0], [1]))  # Homogeneous 좌표로 변환
            point_in_3D = np.dot(np.linalg.inv(camera_matrix), point_3D)[:3] * depth_in_meters

            # 좌표계 변환
            x_cm = point_in_3D[2] * 100  # z축을 위로 올리고, 단위를 cm로 변환
            y_cm = -point_in_3D[0] * 100  # x축을 전방으로 옮기고, 부호를 반대로 하여 왼쪽 방향으로 변환
            z_cm = -point_in_3D[1] * 100  # y축을 원점에서 왼쪽 방향으로 옮기고, 부호를 반대로 하여 변환

            # 토마토 개수에 따라 ID 할당
            tomato_count += 1
            print(f"Tomato {tomato_count}: X={x_cm:.2f}cm, Y={y_cm:.2f}cm, Z={z_cm:.2f}cm")

    # 좌표계 원점 표시
    origin_x, origin_y = int(color_image.shape[1] / 2), int(color_image.shape[0] / 2)
    cv2.circle(color_image, (origin_x, origin_y), 5, (255, 0, 0), -1)

    # 프레임 출력
    cv2.imshow('Webcam', color_image)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) == ord('q'):
        break

# Realsense 카메라 종료
pipeline.stop()
cv2.destroyAllWindows()
