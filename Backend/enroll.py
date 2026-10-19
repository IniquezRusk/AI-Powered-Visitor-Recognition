// AI Models are large, GPU will be a concern.
// Learn how big the model is, parameter size, and how to make it function on mutliple devices.
// Should be more of an app, simple to use

import cv2
from pathlib import Path

from camera import detect_faces

DATASET_DIR = Path("data/visitors")


def enroll_visitor(visitor_id: str, samples_required: int = 10):
    """Capture and save face samples for a consenting visitor."""

    # Validate input before creating files.
    if not visitor_id or not all(
        char.isalnum() or char in "-_" for char in visitor_id
    ):
        raise ValueError(
            "Visitor ID may contain only letters, numbers, hyphens, and underscores."
        )

    if samples_required < 1:
        raise ValueError("samples_required must be at least 1.")

    visitor_dir = DATASET_DIR / visitor_id

    # Avoid silently mixing samples from separate enrollment sessions.
    if visitor_dir.exists() and any(visitor_dir.iterdir()):
        raise FileExistsError(
            f"Enrollment data already exists for {visitor_id}. "
            "Use a new ID or implement a deliberate re-enrollment workflow."
        )

    visitor_dir.mkdir(parents=True, exist_ok=True)

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("Error: Could not open camera.")
        return

    samples_saved = 0

    try:
        while samples_saved < samples_required:
            ret, frame = camera.read()

            if not ret:
                print("Could not read camera frame.")
                break

            faces = detect_faces(frame)

            if len(faces) == 1:
                x, y, w, h = faces[0]

                cv2.rectangle(
                    frame,
                    (x, y),
                    (x + w, y + h),
                    (0, 255, 0),
                    2,
                )

                message = "One face detected - press SPACE"
                color = (0, 255, 0)

            elif len(faces) == 0:
                message = "No face detected"
                color = (0, 0, 255)

            else:
                message = "Multiple faces - only one person should be visible"
                color = (0, 0, 255)

            cv2.putText(
                frame,
                f"Samples: {samples_saved}/{samples_required}",
                (20, 35),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2,
            )

            cv2.putText(
                frame,
                message,
                (20, 70),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                color,
                2,
            )

            cv2.putText(
                frame,
                "Q to cancel",
                (20, 105),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (255, 255, 255),
                2,
            )

            cv2.imshow("Visitor Enrollment", frame)
            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break

            if key == ord(" ") and len(faces) == 1:
                x, y, w, h = faces[0]

                # Save the full webcam frame for detector testing
                frame_filename = visitor_dir / (
                    f"frame_{samples_saved + 1:03d}.jpg"
                )

                if not cv2.imwrite(str(frame_filename), frame):
                    print("Failed to save frame.")
                    continue

                # Keep saving the existing cropped face samples
                face_image = frame[y:y + h, x:x + w]

                filename = visitor_dir / (
                    f"sample_{samples_saved + 1:03d}.jpg"
                )

                if cv2.imwrite(str(filename), face_image):
                    samples_saved += 1
                    print(
                        f"Saved sample {samples_saved}/{samples_required}"
                    )
                else:
                    print("Failed to save sample.")

    finally:
        camera.release()
        cv2.destroyAllWindows()

    print(f"Enrollment complete: {samples_saved}/{samples_required}")
    print(f"Saved samples in: {visitor_dir}")


if __name__ == "__main__":
    visitor_id = input("Enter a visitor ID: ").strip()

    consent = input(
        "Has the visitor explicitly consented to biometric enrollment? (yes/no): "
    ).strip().lower()

    if consent == "yes":
        enroll_visitor(visitor_id)
    else:
        print("Enrollment cancelled.")
