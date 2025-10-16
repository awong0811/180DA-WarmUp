import cv2
import numpy as np
from sklearn.cluster import KMeans

if __name__ == "__main__":
    # Open the video file
    cap = cv2.VideoCapture(0)

    # if not cap.isOpened():
    #     raise ValueError(f"Error: Could not open video {video_path}")
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

        rect_size = 150
        x1 = 1280//2 - rect_size//2
        y1 = 960//2 - rect_size//2
        x2 = x1 + rect_size
        y2 = y1 + rect_size

        # Extract the region of interest (ROI)
        roi = frame[y1:y2, x1:x2]  # still in BGR
        
        # Reshape ROI to a list of pixels
        pixels = roi.reshape(-1, 3)
        
        # Apply KMeans to find the dominant color
        k = 1  # number of clusters
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(pixels)
        dominant_color = kmeans.cluster_centers_[0].astype(int)
        # Convert to text
        color_text = f"BGR: {dominant_color[0]},{dominant_color[1]},{dominant_color[2]}"
        
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

        # Put text on the frame
        cv2.putText(
            frame,
            color_text,
            (x1, y1 - 10),  # position above rectangle
            cv2.FONT_HERSHEY_SIMPLEX,
            1,            # font scale
            (0, 0, 255),    # text color (red)
            1,              # thickness
            cv2.LINE_AA
        )

        cv2.imshow("Frame", frame)

        # Press 'q' to quit early
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()