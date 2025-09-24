_____Flexapy Wristband Motion Tracking_____

This project powers the motion-tracking and mapping capabilities of the Flexapy wristbands. It collects real-time motion data from an MPU-6050 sensor, visualizes it, and maps it for further processing. The goal of this project was to build a minimum viable product (MVP) to demonstrate the feasibility of Flexapy’s vision — a full-body tracking suit for adaptive, AI-driven physical therapy solutions. This served as a proof of concept for potential sponsors and collaborators.

_____Requirements_____
    
    - Arduino Nano Every
    - MPU-6050 motion sensor
    - Protoboard (breadboard)

_____How to Run_____

Install dependencies:
'''bash
"pip install -r requirements.txt"
Then follow the steps below to run this project

1. Start Data Capture
    Run the following command to begin serial data capture of acceleration and gyroscopic measurements:
    
    "python3 Motion_Tracking.py"
    
    This script uses Matplotlib to chart the measurements across the X, Y, and Z axes in real time.

2. Visualize Motion Mapping
    Once data capture is running, execute:

    "python3 Motion_Mirroring.py"

    This displays a live view of tracked movements. In future iterations, this will integrate with AI models to provide personalized feedback.