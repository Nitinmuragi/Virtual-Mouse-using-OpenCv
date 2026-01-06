



# Fruit Ninja Enhanced


![alt text](https://static.wixstatic.com/media/e58508_4dc070f3ec02433faf33e54bae1dc302~mv2.png)

A motion-controlled Fruit Ninja clone using computer vision for hand tracking. Slice fruits with your hand movements in this enhanced version featuring improved tracking, visual feedback, and fullscreen support.

## Features

- Real-time hand tracking using computer vision
- Dynamic blade trail effects
- Particle effects for sliced fruits
- Combo system with visual feedback
- Camera preview with tracking visualization
- Fullscreen support
- Smooth hand movement tracking
- Enhanced visual effects

## Requirements

- Python 3.8 or higher
- Webcam
- Required packages listed in requirements.txt

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd fruit-ninja-enhanced
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## How to Play

1. Run the game:
```bash
python fruit_ninja_enhanced.py
```

2. Controls:
- Use your hand in front of the webcam to control the katana
- Move your hand to slice fruits
- Press F to toggle fullscreen mode
- Press ESC to exit fullscreen or quit game

## Game Elements

- Camera Preview: Shows your hand position and tracking status
- Score Counter: Tracks your points
- Combo System: Chain multiple slices for bonus points
- Visual Guides: Help you understand the tracking area

## Project Structure

- `fruit_ninja_enhanced.py`: Main game file
- `game_engine.py`: Core game mechanics and rendering
- `game_objects.py`: Game object classes (fruits, blade trail)
- `hand_tracking.py`: Computer vision and hand tracking

## Assets

The game requires the following asset directories:
- `background/`: Background images
- `cursor/`: Katana cursor image
- `fonts/`: Font files
- `fruits/`: Fruit images
- `sounds/`: Sound effects

## Dependencies

- pygame: Game engine and graphics
- opencv-python: Computer vision and webcam
- mediapipe: Hand tracking
- numpy: Numerical computations

## Performance Tips

1. Ensure good lighting for better hand tracking
2. Keep your hand within the tracking boundaries shown in the camera preview
3. Make deliberate slicing motions for better detection
4. Adjust your distance from the camera if tracking is inconsistent

## Known Issues

- Hand tracking may be affected by poor lighting conditions
- Some systems may experience slight input lag
- Webcam initialization may take a few seconds

## Credits

- Original Fruit Ninja concept by Halfbrick Studios
- Hand tracking implementation using Google's MediaPipe
- Game engine built with Pygame

## License

This project is open source and available under the MIT License.
