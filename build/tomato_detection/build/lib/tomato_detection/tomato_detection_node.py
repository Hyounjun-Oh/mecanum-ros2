import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Int32
from geometry_msgs.msg import Point

import cv2
import torch
import pyrealsense2 as rs
import numpy as np

class TomatoDetectionNode(Node):
    def __init__(self):
        super().__init__('tomato_detection_node')

        # YOLOv5 모델 로드
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt')

        # Realsense 카메라 설정
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        self.config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        self.config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

        # Realsense 카메라 시작
        self.pipeline.start(self.config)

        # 카메라 캘리브레이션 정보 로드
        calibration_file = 'camera_calibration.xml'
        calibration_data = cv2.FileStorage(calibration_file, cv2.FILE_STORAGE_READ)
        self.camera_matrix = calibration_data.getNode("camera_matrix").mat()
        self.dist_coeffs = calibration_data.getNode("dist_coeffs").mat()
        calibration_data.release()

        # 토마토 좌표 발행을 위한 Publisher 생성
        self.tomato_pub = self.create_publisher(Point, 'tomato_coordinates', 10)
        # ID 발행을 위한 Publisher 생성
        self.id_pub = self.create_publisher(Int32, 'tomato_id', 10)

        # 토마토 개수 초기화
        self.tomato_count = 0

        # 실행 주기 설정
        self.timer = self.create_timer(0.1, self.detect_and_publish_tomato)

    def detect_and_publish_tomato(self):
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

        for detection in results.xyxy[0]:
            if detection[5] == 0:  # "tomato" 클래스 라벨을 나타내는 인덱스
                x, y, w, h = detection[:4]

                # 물체의 중심 좌표 계산
                center_x = int((x + w) / 2)
                center_y = int((y + h) / 2)

                # 물체의 3D 좌표 계산
                depth = depth_image[center_y, center_x].astype(float)
                depth_scale = self.pipeline.get_active_profile().get_device().first_depth_sensor().get_depth_scale()
                depth_in_meters = depth * depth_scale

                # 2D 좌표를 3D 좌표로 변환
                point_2D = np.array([[center_x, center_y]], dtype=np.float32)
                point_3D = cv2.undistortPoints(point_2D, self.camera_matrix, self.dist_coeffs)
                point_3D = np.concatenate((point_3D[0][0], [1]))  # Homogeneous 좌표로 변환
                point_in_3D = np.dot(np.linalg.inv(self.camera_matrix), point_3D)[:3] * depth_in_meters

                # 좌표계 변환
                x_cm = point_in_3D[2] * 100  # z축을 위로 올리고, 단위를 cm로 변환
                y_cm = -point_in_3D[0] * 100  # x축을 전방으로 옮기고, 부호를 반대로 하여 왼쪽 방향으로 변환
                z_cm = -point_in_3D[1] * 100  # y축을 원점에서 왼쪽 방향으로 옮기고, 부호를 반대로 하여 변환

                # 토마토 개수에 따라 ID 할당
                self.tomato_count += 1

                # 토마토 좌표 발행
                tomato_coordinates = Point()
                tomato_coordinates.x = x_cm
                tomato_coordinates.y = y_cm
                tomato_coordinates.z = z_cm
                self.tomato_pub.publish(tomato_coordinates)

                # ID 발행
                tomato_id = Int32()
                tomato_id.data = self.tomato_count
                self.id_pub.publish(tomato_id)

def main(args=None):
    rclpy.init(args=args)
    tomato_detection_node = TomatoDetectionNode()
    rclpy.spin(tomato_detection_node)
    tomato_detection_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
