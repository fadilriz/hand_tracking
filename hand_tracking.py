import cv2
import mediapipe as mp
import serial
import time

# Inisialisasi komunikasi serial ke Arduino (ubah COM sesuai port Arduino)
ser = serial.Serial('COM3', 9600, timeout=1)  # Untuk Linux/Mac gunakan '/dev/ttyUSB0'

# Inisialisasi Mediapipe untuk deteksi tangan
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Menggunakan kamera laptop
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  # Mirror tampilan kamera
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    finger_count = 0

    # Jika ada tangan yang terdeteksi
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Cek posisi jari (telunjuk, tengah, manis)
            finger_tips = [8, 12, 16]  # ID landmark ujung jari (telunjuk, tengah, manis)
            finger_bases = [6, 10, 14] # ID landmark pangkal jari
            
            for tip, base in zip(finger_tips, finger_bases):
                if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[base].y:
                    finger_count += 1  # Tambah jumlah jari yang terangkat

    # Kirim data ke Arduino
    ser.write(str(finger_count).encode())  

    # Tampilkan jumlah jari di layar
    cv2.putText(frame, f"Jari: {finger_count}", (50, 100), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Hand Tracking", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
ser.close()