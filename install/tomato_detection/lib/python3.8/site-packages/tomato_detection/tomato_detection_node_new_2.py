import rclpy
from rclpy.node import Node
import cv2
import torch
import pyrealsense2 as rs
import numpy as np
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from std_msgs.msg import String

class TomatoDetectionNode(Node):
    def __init__(self):
        super().__init__('tomato_detection_node')
        
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path='/home/ohj/mecanum-ros2/src/tomato_detection/tomato_detection/tomato.pt')
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        self.config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        self.config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        
        self.publisher = self.create_publisher(String, 'detected_tomatoes', 10)
        self.bridge = CvBridge()
        
    def detect_tomatoes(self):
        while True:
            frames = self.pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()
            depth_frame = frames.get_depth_frame()
            
            if not color_frame or not depth_frame:
                continue
            
            color_image = np.asanyarray(color_frame.get_data())
            color_image1 = np.asanyarray(color_frame.get_data())
            depth_image = np.asanyarray(depth_frame.get_data())
            
            results = self.model(color_image)
            
            tomato_count = 0
            tomato_msg = String()
            
            for detection in results.xyxy[0]:
                class_index = int(detection[5])
                if class_index in [0, 1]:  # 'tomato' or 'unripe' class
                    x, y, w, h = detection[:4]
                    label = f"{results.names[class_index]}: {detection[4]:.2f}"
                    cv2.rectangle(color_image, (int(x), int(y)), (int(w), int(h)), (0, 255, 0), 2)
                    cv2.putText(color_image, label, (int(x), int(y) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    
                    center_x = int((x + w) / 2)
                    center_y = int((y + h) / 2)
    
                    depth = depth_image[center_y, center_x].astype(float)
                    depth_scale = self.pipeline.get_active_profile().get_device().first_depth_sensor().get_depth_scale()
                    depth_in_meters = depth * depth_scale
    
                    cv2.circle(color_image, (center_x, center_y), 3, (0, 0, 255), -1)
    
                    point_2D = np.array([[center_x, center_y]], dtype=np.float32)
                    point_3D = cv2.undistortPoints(point_2D, camera_matrix, dist_coeffs)
                    point_3D = np.concatenate((point_3D[0][0], [1]))
                    point_in_3D = np.dot(np.linalg.inv(camera_matrix), point_3D)[:3] * depth_in_meters
    
                    x_cm = point_in_3D[2] * 100
                    y_cm = -point_in_3D[0] * 100
                    z_cm = -point_in_3D[1] * 100
    
                    tomato_count += 1
                    tomato_msg.data += f"Tomato {tomato_count}: X={x_cm:.2f}cm, Y={y_cm:.2f}cm, Z={z_cm:.2f}cm\n"
    
            self.publisher.publish(tomato_msg)
    
            origin_x, origin_y = int(color_image.shape[1] / 2), int(color_image.shape[0] / 2)
            cv2.circle(color_image, (origin_x, origin_y), 5, (255, 0, 0), -1)
    
            cv2.imshow('detect_Camera', color_image)
            cv2.imshow('raw_Camera', color_image1)
    
            if cv2.waitKey(1) == ord('q'):
                break
    
    def run(self):
        self.pipeline.start(self.config)
        self.detect_tomatoes()
        self.pipeline.stop()
        cv2.destroyAllWindows()

def main(args=None):
    rclpy.init(args=args)
    node = TomatoDetectionNode()
    node.run()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
