import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
import cv2
import torch
import pyrealsense2 as rs
import numpy as np

class TomatoPublisher(Node):
    def __init__(self):
        super().__init__('tomato_publisher')
        self.tomato_count = 0
        self.tomato_pub = self.create_publisher(Float64MultiArray, 'tomato_topic', 10)

        # YOLOv5 모델 로드
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path='/home/ohj/mecanum-ros2/src/tomato_detection/tomato_detection/tomato.pt')

        # Realsense 카메라 설정
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        self.config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        self.config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

        # Realsense 카메라 시작
        self.pipeline.start(self.config)

        # 카메라 캘리브레이션 정보 로드
        calibration_file = '/home/ohj/mecanum-ros2/src/tomato_detection/tomato_detection/camera_calibration.xml'
        calibration_data = cv2.FileStorage(calibration_file, cv2.FILE_STORAGE_READ)
        self.camera_matrix = calibration_data.getNode("camera_matrix").mat()
        self.dist_coeffs = calibration_data.getNode("dist_coeffs").mat()
        calibration_data.release()

        self.timer = self.create_timer(1.0, self.publish_tomato_coordinates)

    def publish_tomato_coordinates(self):
        # 프레임 가져오기
        frames = self.pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        depth_frame = frames.get_depth_frame()
        if not color_frame or not depth_frame:
            return
        color_image = np.asanyarray(color_frame.get_data())
        depth_image = np.asanyarray(depth_frame.get_data())

        # YOLOv5를 사용하여 물체 감지
        results = self.model(color_image)

        # 검출된 물체의 좌표와 클래스 출력
        tomato_count = 0  # 검출된 토마토 개수 초기화

        for detection in results.xyxy[0]:
            if detection[5] in [0, 5]:  # "tomato" 또는 "upripe" 클래스 라벨을 나타내는 인덱스
                x, y, w, h = detection[:4]
                label = f"{results.names[int(detection[5])]}: {detection[4]:.2f}"
                cv2.rectangle(color_image, (int(x), int(y)), (int(w), int(h)), (0, 255, 0), 2)
                cv2.putText(color_image, label, (int(x), int(y) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

                # 물체의 중심 좌표 계산
                center_x = int((x + w) / 2)
                center_y = int((y + h) / 2)

                # 물체의 3D 좌표 계산
                depth = depth_image[center_y, center_x].astype(float)
                depth_scale = self.pipeline.get_active_profile().get_device().first_depth_sensor().get_depth_scale()
                depth_in_meters = depth * depth_scale
                # 물체의 중심에 점 그리기
                cv2.circle(color_image, (center_x, center_y), 3, (0, 0, 255), -1)
                # 2D 좌표를 3D 좌표로 변환
                point_2D = np.array([[center_x, center_y]], dtype=np.float32)
                point_3D = cv2.undistortPoints(point_2D, self.camera_matrix, self.dist_coeffs)
                point_3D = np.concatenate((point_3D[0][0], [1]))  # Homogeneous 좌표로 변환
                point_in_3D = np.dot(np.linalg.inv(self.camera_matrix), point_3D)[:3] * depth_in_meters

                # 좌표계 변환
                x_cm = point_in_3D[2] * 1000  # z축을 위로 올리고, 단위를 mm로 변환
                y_cm = -point_in_3D[0] * 1000  # x축을 전방으로 옮기고, 부호를 반대로 하여 왼쪽 방향으로 변환
                z_cm = -point_in_3D[1] * 1000  # y축을 원점에서 왼쪽 방향으로 옮기고, 부호를 반대로 하여 변환

                # 토마토 개수에 따라 ID 할당
                tomato_count += 1
                print(f"Tomato {tomato_count}: X={x_cm:.2f}mm, Y={y_cm:.2f}mm, Z={z_cm:.2f}mm")

                # 토마토 메시지 발행
                tomato = Float64MultiArray()
                tomato.data = [0.0, 0.0, 0.0]
                tomato.layout.data_offset = self.tomato_count
                tomato.data[0] = x_cm
                tomato.data[1] = y_cm
                tomato.data[2] = z_cm
                self.tomato_pub.publish(tomato)

        # 좌표계 원점 표시
        origin_x, origin_y = int(color_image.shape[1] / 2), int(color_image.shape[0] / 2)
        cv2.circle(color_image, (origin_x, origin_y), 5, (255, 0, 0), -1)

        # 프레임 출력
        cv2.imshow('Webcam', color_image)
        cv2.waitKey(1)

def main(args=None):
    rclpy.init(args=args)
    tomato_publisher = TomatoPublisher()
    rclpy.spin(tomato_publisher)
    tomato_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
