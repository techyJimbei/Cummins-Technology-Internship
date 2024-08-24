##README

###Project: CVML Object Detection for MR Shaft and Wheel Manufacturing

Overview:

This project aims to automate the identification and classification of MR shafts and wheels in a manufacturing line using Computer Vision and Machine Learning (CVML). The project leverages the YOLOv8 object detection model to achieve this goal.
Key Features:

* Wheel Detection: Detects the presence of a wheel in front of a camera.
* Wheel Type Classification: Differentiates between various types of wheels (e.g., '270', '378', '393', '676', '686').
* Flask Application: Provides a user interface for selecting wheel types and viewing results.

Prerequisites:

* Python 3.x
* Required Python packages (listed in `requirements.txt`)
* A compatible GPU (if using GPU acceleration)

Installation:

1. Clone the repository:
   ```bash
   git clone https://github.com/techyJimbei/Cummins-Technology-Internship
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

Usage:

1. Train models:
   - Run the training scripts for wheel detection and wheel type classification.
   - Ensure that the training data is prepared and organized correctly.
2. Start the Flask application:
   ```bash
   python app.py
   ```
3. Use the web application:
   - Access the Flask application in your web browser.
   - Select the desired wheel type.
   - Upload an image or capture a live feed.
   - The application will detect the wheel and classify its type.

Structure:

* Model A/: Contains the trained YOLOv8 model for Presence Check.
* Model /: Contains the trained YOLOv8 model for Object Detection.
* MR S&W/: Contains the used dataset.
* directory/: Stores the training and validation data of both models in their respective folders.
* static/: Contains the JS and CSS scripts used.
* templats/: Contains the HTML script.
* app.py: The Flask application file.
* requirements.txt: Lists the required Python packages.

Future Work:

* Model optimization: Explore techniques to improve model accuracy and performance.
* Real-time implementation: Integrate the system into a real-time manufacturing environment.
* Additional features: Consider adding features like defect detection or measurement.



