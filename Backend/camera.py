import cv2

# Loads in OpenCV face detector
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)


camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Error: Could not open camera.")
    exit()

while True:
    ret, frame = camera.read()

    if not ret:
        print("Could not read frame.")
        break
    
    # Convert frame to grayscale for the face detector
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detects faces
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.05,
        minNeighbors=3,
        minSize=(30, 30)
    )

    # Draws a rectangle around every detected face
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, 
            (x, y), 
            (x + w, y + h), 
            (0, 255, 0), 
            2
            )

        cv2.putText(
            frame,
            "Face Detected",
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

    cv2.imshow("Smart Visitor Camera", frame)

    # Press Q to quit the camera
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()

