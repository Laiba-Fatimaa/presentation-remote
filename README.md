# Gesture Presentation Remote

Control your slides with a wave of your hand. This project uses your webcam and [MediaPipe](https://developers.google.com/mediapipe) hand tracking to detect when your hand moves to the left or right side of the frame, then sends the matching arrow key press to whatever app is in focus (PowerPoint, Google Slides, Keynote, PDF viewers, etc.).

- Hand to the **left** → presses `←` (previous slide)
- Hand to the **right** → presses `→` (next slide)

## How It Works

1. OpenCV captures video from your webcam and mirrors it so movement feels natural.
2. MediaPipe Hands tracks a single hand and returns 21 landmarks.
3. The script reads the **wrist** landmark's horizontal position (`x`, from 0.0 to 1.0) and places it in one of three zones:

   | Zone   | Wrist `x` range |
   |--------|-----------------|
   | Left   | `x < 0.40`      |
   | Center | `0.40 – 0.60`   |
   | Right  | `x > 0.60`      |

4. A gesture fires **once**, the moment your hand *enters* the left or right zone. The trigger is then "disarmed" until your hand returns to the center zone, which prevents a single swipe from flipping through many slides.
5. `pyautogui` sends the arrow key press, and a green "SWIPE LEFT / SWIPE RIGHT" label appears on screen for one second.

## Requirements

- Python 3.8 – 3.11 (recommended; MediaPipe's `solutions` API may not be available in newer versions)
- A working webcam
- Python packages:
  - `opencv-python`
  - `mediapipe`
  - `pyautogui`

## Installation

```bash
git clone https://github.com/Laiba-Fatimaa/presentation-remote.git
cd presentation-remote

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install opencv-python mediapipe pyautogui
```

## Usage

```bash
python presentation_remote.py
```

1. Run the script. A "Hand Tracking" window opens showing your webcam feed.
2. Open your presentation and put it in slideshow mode.
3. **Click on the presentation window** so it has keyboard focus. The key presses go to whichever window is active.
4. Stand or sit in front of the camera and move your hand to the left or right side of the frame, then bring it back to the center before the next swipe.

### Quitting

Press `q` or `Esc` while the tracking window is focused, or just close the window.

## Configuration

Everything is tweakable at the top of the script or in the zone checks:

| Setting | Where | Default | What it does |
|---------|-------|---------|--------------|
| `max_num_hands` | `Hands(...)` | `1` | Number of hands tracked |
| `min_detection_confidence` | `Hands(...)` | `0.6` | How sure MediaPipe must be to detect a hand |
| `min_tracking_confidence` | `Hands(...)` | `0.5` | How sure it must be to keep tracking |
| `model_complexity` | `Hands(...)` | `0` | `0` is fastest, `1` is more accurate |
| Left / right thresholds | `0.40` / `0.60` | — | Widen the center zone for fewer accidental triggers, narrow it for more sensitivity |
| Camera resolution | `cap.set(...)` | `640x480` | Capture size (kept low for performance) |
| Display size | `cv2.resize(...)` | `800x600` | Size of the preview window |
| Gesture label time | `current_time + 1` | `1` second | How long the on-screen label stays visible |

To use different keys (for example `pageup` / `pagedown`), change the `pyautogui.press('left')` and `pyautogui.press('right')` calls.

## Troubleshooting

**Camera doesn't open or the window is black**
Try a different camera index: `cv2.VideoCapture(1)` instead of `0`. Close other apps that might be using the webcam.

**Slides don't change**
Make sure the presentation window is focused. On macOS, grant your terminal or IDE **Accessibility** permission (System Settings → Privacy & Security → Accessibility) so `pyautogui` can send key presses.

**Gestures trigger by accident**
Widen the center zone (for example `0.35` / `0.65`), raise `min_detection_confidence`, or make sure only one person is in frame.

**Hand isn't detected**
Use good, even lighting and keep your hand clearly visible against the background.

**Laggy video**
Keep `model_complexity=0` and the capture resolution at `640x480`.

## Known Limitations

- Tracks one hand only.
- Detection is based on hand position, not motion speed, so the hand needs to travel into a side zone and back to center for each slide change.
- Key presses go to the active window, so switching windows mid-presentation will send them to the wrong place.

## Tech Stack

- [OpenCV](https://opencv.org/): video capture and display
- [MediaPipe](https://developers.google.com/mediapipe): hand landmark detection
- [PyAutoGUI](https://pyautogui.readthedocs.io/): keyboard automation

## Ideas for Future Improvements

- Add gestures for starting or ending the slideshow
- Support a pointer or laser mode using the index fingertip
- Add a cooldown timer between swipes
- Calibration step for different camera angles and distances
