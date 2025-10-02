import cv2
import numpy as np

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)

    lower = np.array([100, 100, 100]) # HSV
    upper = np.array([130, 255, 255])

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = cv2.resize(frame, (1280, 960))
        filtered = cv2.bilateralFilter(frame, d=9, sigmaColor=75, sigmaSpace=75)
        hsv = cv2.cvtColor(filtered, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower, upper)

        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)  # top-left (x,y), width, height
            # Draw rectangle
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

        cv2.imshow("Frame", frame)

        # Press 'q' to quit early
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()