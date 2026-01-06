# Hand Piano - Interactive Music Creation with Computer Vision (WorkShop Traning Code)

This application allows you to create music by moving your hand in front of your webcam. It uses computer vision to track your hand movements and converts them into musical notes in real-time.

## Features

- Real-time hand tracking using OpenCV and MediaPipe
- Dynamic sound generation based on hand position
- Interactive visualization showing hand movement and musical notes
- Live webcam feed with hand landmark overlay
- Real-time audio feedback

## Requirements

- Python 3.8+
- Webcam
- The required Python packages are listed in `requirements.txt`

## Installation

1. Clone this repository
2. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:
```bash
python src/main.py
```

2. Position yourself in front of the webcam
3. Raise your hand with your index finger pointing
4. Move your hand up and down to play different musical notes
5. To exit, press Ctrl+C in the terminal or close the window

## How It Works

- The application uses OpenCV and MediaPipe to track your hand in real-time
- The vertical position of your index finger determines the musical note
- Moving your hand up plays higher notes, moving down plays lower notes
- The visualization shows your hand movement pattern and note history
- Sound is generated in real-time using pygame's audio system

## Controls

- Moving hand up/down: Changes the musical note
- Moving hand out of frame: Stops the current note
- Close window or Ctrl+C: Exits the application

## Components

- `hand_tracker.py`: Handles webcam input and hand detection
- `sound_engine.py`: Manages sound synthesis and playback
- `visualizer.py`: Handles UI and real-time visualization
- `main.py`: Main application controller

## Requirements

See `requirements.txt` for the complete list of dependencies.
