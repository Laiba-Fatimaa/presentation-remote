import cv2
import mediapipe as mp
import time
import pyautogui

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.6, min_tracking_confidence=0.5, model_complexity=0)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

window_name = "Hand Tracking"
cv2.namedWindow(window_name)

# --- Gesture detection variables ---
gesture_text = ""
gesture_display_until = 0
current_zone = "center"  # tracks which zone the hand is currently in
armed = True  # only trigger once per visit to a side zone

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (800, 600))  # display bigger without stressing the camera

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    current_time = time.time()

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            wrist = hand_landmarks.landmark[0]
            curr_x = wrist.x

            # Which zone is the hand in right now?
            if curr_x < 0.40:
                new_zone = "left"
            elif curr_x > 0.60:
                new_zone = "right"
            else:
                new_zone = "center"

            # Trigger only the moment we ENTER a side zone (not every frame we're in it)
            if new_zone != current_zone:
                if new_zone == "left" and armed:
                    gesture_text = "SWIPE LEFT"
                    pyautogui.press('left')
                    print(gesture_text)
                    gesture_display_until = current_time + 1
                    armed = False
                elif new_zone == "right" and armed:
                    gesture_text = "SWIPE RIGHT"
                    pyautogui.press('right')
                    print(gesture_text)
                    gesture_display_until = current_time + 1
                    armed = False
                elif new_zone == "center":
                    armed = True  # back in center, ready to trigger again next time

                current_zone = new_zone

    if current_time < gesture_display_until:
        cv2.putText(frame, gesture_text, (50, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)

    cv2.imshow(window_name, frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q') or key == 27:
        break
    if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
        break

cap.release()
cv2.destroyAllWindows()