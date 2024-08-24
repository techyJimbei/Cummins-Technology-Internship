from flask import Flask, render_template, Response, jsonify, request
import cv2
import os
import threading
import numpy as np
from ultralytics import YOLO

app = Flask(__name__)

# Model paths
model_A_path = r"C:\Users\ishru\OneDrive\Desktop\Internship\FailSafe_Profile_Grinding\best_FailSafe_Presence_Check_2.pt"
model_B_path = r"C:\Users\ishru\OneDrive\Desktop\Internship\FailSafe_Profile_Grinding\best_FailSafe_Reaugmented.pt"

# Load models
model_A = YOLO(model_A_path)
model_B = YOLO(model_B_path)

# Global variables
detection_running = False
stable_detected = False
result_text = "Waiting for result..."
selected_type = None
detection_lock = threading.Lock()  # Lock for thread safety

# Initialize video capture with cv2
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise Exception("Error: Could not open video capture device.")

temp_folder = r"C:\Users\ishru\OneDrive\Desktop\Temp_folder"
if not os.path.exists(temp_folder):
    os.makedirs(temp_folder)

stable_frame_path = os.path.join(temp_folder, "stable_frame.jpg")

# Define detection region dimensions
detect_region_x = 200
detect_region_y = 100
detect_region_width = 240
detect_region_height = 240  # Make it square

def detect_objects():
    global detection_running, stable_detected, result_text
    stable_count = 0
    required_stable_count = 5  # Adjust as needed

    while detection_running:
        try:
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame")
                continue

            # Draw the detection region square on the frame
            cv2.rectangle(frame, (detect_region_x, detect_region_y),
                          (detect_region_x + detect_region_width, detect_region_y + detect_region_height),
                          (255, 0, 0), 2)

            # Define detection region and resize for model
            detect_region = frame[detect_region_y:detect_region_y + detect_region_height,
                                  detect_region_x:detect_region_x + detect_region_width]

            detect_region_resized = cv2.resize(detect_region, (640, 640))  # Example size, adjust as needed
            results_A = model_A.predict(source=detect_region_resized, conf=0.6)
            wheel_detected = any(result.boxes for result in results_A)

            if wheel_detected:
                stable_count += 1
            else:
                stable_count = 0

            if stable_count >= required_stable_count:
                stable_frame = frame.copy()
                cv2.imwrite(stable_frame_path, stable_frame)
                stable_detected = True
                stable_count = 0

            if stable_detected:
                results_B = model_B.predict(source=stable_frame_path, conf=0.8)

                detected_type = "Unknown"
                for result in results_B:
                    boxes = result.boxes
                    if boxes is None:
                        continue
                    for box in boxes:
                        x1, y1, x2, y2 = box.xyxy[0].tolist()
                        conf = box.conf[0]
                        cls = box.cls[0]
                        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                        cls = int(cls)

                        # Draw bounding box and label
                        cv2.rectangle(stable_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        label = f'{model_B.names[cls]} {conf:.2f}'
                        cv2.putText(stable_frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                        detected_type = model_B.names[cls] if cls < len(model_B.names) else "Unknown"

                with detection_lock:
                    if selected_type and detected_type == selected_type:
                        result_text = "Valid"
                    else:
                        result_text = "Invalid"
                    stable_detected = False

            # Encode the color frame as JPEG and convert to bytes
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

        except Exception as e:
            print(f"Error during detection: {e}")
            break

def gen():
    while True:
        try:
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame")
                continue

            # Encode the color frame as JPEG and convert to bytes
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        except Exception as e:
            print(f"Error in video feed generation: {e}")
            break

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/start_detection', methods=['POST'])
def start_detection():
    global detection_running
    with detection_lock:
        if detection_running:
            return jsonify({"status": "already_running"})
        detection_running = True
    detection_thread = threading.Thread(target=detect_objects)
    detection_thread.start()
    return jsonify({"status": "detection_started"})

@app.route('/stop_detection', methods=['POST'])
def stop_detection():
    global detection_running
    with detection_lock:
        detection_running = False
    return jsonify({"status": "detection_stopped"})

@app.route('/get_detection_output')
def get_detection_output():
    with detection_lock:
        return jsonify({"result": result_text})

@app.route('/set_selected_type', methods=['POST'])
def set_selected_type():
    global selected_type
    selected_type = request.json.get('type', None)
    return jsonify({"status": "type_set", "selected_type": selected_type})

if __name__ == '__main__':
    app.run(debug=True)
