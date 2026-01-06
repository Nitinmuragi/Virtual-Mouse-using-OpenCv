# Virtual Mouse with OpenCV Game

A fun and educational project that combines computer vision with gaming to learn OpenCV in a gamified way.

## Author
**Shridhar Rudragoud**  
*CTO at Hivetech*

## About
This project is an educational tool designed to help developers understand OpenCV through practical, engaging implementation. By combining serious computer vision concepts with game mechanics, it makes learning both fun and effective.

## Features
- Hand gesture-controlled virtual mouse
- Real-time hand tracking using OpenCV and MediaPipe
- Interactive aim practice game
- Score tracking system
- Dark-themed modern interface

## Controls
- **Index Finger**: Move cursor
- **Thumb Up**: Left click
- **Last 2-3 Fingers Up**: Right click
- **Esc**: Emergency exit
- **Ctrl+S**: Toggle mouse control

## Game Rules
- Three apples appear in the game area
- Click all apples to complete a round
- Score based on completion time
- Faster completion = Higher score
- Base score: 1000 points
- Time penalty: -10 points/second
- Try to beat your high score!

## Technical Implementation
- OpenCV for webcam capture and image processing
- MediaPipe for hand landmark detection
- Tkinter for GUI implementation
- Custom mouse controller with safety features
- Game engine with score tracking
- Dark theme UI with proper containment

## Installation
1. Clone the repository
2. Install requirements:
```bash
pip install -r requirements.txt
```
3. Run the application:
```bash
python app.py
```

## Dependencies
- Python 3.x
- OpenCV
- MediaPipe
- NumPy
- PyAutoGUI
- Pillow
- Keyboard

## Educational Value
- Learn OpenCV image processing
- Understand hand tracking algorithms
- Practice GUI development
- Implement game mechanics
- Experience real-time computer vision applications

## Note from Author
This is an educational Python code to get used to working with OpenCV in a gamified way. I hope you learn and connect fun with serious concepts. Feel free to explore, modify, and learn from this implementation.

Connect and learn more!

## License
MIT License

Copyright (c) 2024 Shridhar Rudragoud

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.