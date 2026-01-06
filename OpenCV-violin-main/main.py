import cv2
import pygame
from hand_tracker import HandTracker
from sound_engine import SoundEngine
from visualizer import Visualizer

def main():
    # Initialize components
    cap = cv2.VideoCapture(0)
    hand_tracker = HandTracker()
    sound_engine = SoundEngine()
    visualizer = Visualizer()

    # Set camera resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    try:
        while True:
            # Process events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise KeyboardInterrupt

            # Read camera frame
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame")
                break

            # Mirror frame horizontally
            frame = cv2.flip(frame, 1)

            # Process hand tracking
            frame, hand_positions = hand_tracker.process_frame(frame)

            # Get pointer position and convert to note
            pointer_pos = hand_tracker.get_pointer_position()
            current_note = None

            if pointer_pos:
                # Convert Y position to note and X position to volume
                x_pos, y_pos = pointer_pos
                current_note = sound_engine.get_note_from_position(y_pos, visualizer.height)
                volume = sound_engine.get_volume_from_position(x_pos, visualizer.width)
                sound_engine.play_note(current_note, volume)
            else:
                sound_engine.stop_current_note()

            # Convert frame from BGR to RGB for pygame
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Update visualization
            visualizer.update(frame, hand_positions, current_note)

    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        # Clean up resources
        cap.release()
        hand_tracker.release()
        sound_engine.cleanup()
        visualizer.cleanup()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()