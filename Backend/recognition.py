from pathlib import Path

import cv2
import numpy as np
from insightface.app import FaceAnalysis


class FaceRecognitionEngine:
    def __init__(self):
        self.data_dir = Path(__file__).resolve().parent / "data" / "visitors"
        model_root = Path(__file__).resolve().parent / "models"

        self.app = FaceAnalysis(
            name="buffalo_l",
            root=str(model_root),
            providers=["CPUExecutionProvider"],
        )
        self.app.prepare(ctx_id=-1, det_size=(640, 640))

        # visitor ID -> list of reference embeddings
        self.visitors = {}

    def get_embedding(self, image_path):
        image_path = Path(image_path)
        image = cv2.imread(str(image_path))

        if image is None:
            raise ValueError(f"Could not read image: {image_path}")

        faces = self.app.get(image)

        if len(faces) != 1:
            print(
                f"Skipping {image_path.name}: "
                f"expected 1 face, found {len(faces)}"
            )
            return None

        return faces[0].normed_embedding

    def load_visitors(self):
        """Load embeddings from each visitor's saved full-frame images."""
        self.visitors.clear()

        if not self.data_dir.exists():
            raise FileNotFoundError(
                f"Visitor data directory not found: {self.data_dir}"
            )

        for visitor_dir in sorted(self.data_dir.iterdir()):
            if not visitor_dir.is_dir():
                continue

            embeddings = []

            for image_path in sorted(visitor_dir.glob("frame_*.jpg")):
                embedding = self.get_embedding(image_path)

                if embedding is not None:
                    embeddings.append(embedding)

            if embeddings:
                self.visitors[visitor_dir.name] = embeddings
                print(
                    f"Loaded {len(embeddings)} embeddings "
                    f"for {visitor_dir.name}"
                )
            else:
                print(f"No usable face images for {visitor_dir.name}")

        print(f"Total enrolled visitors loaded: {len(self.visitors)}")

    def recognize_face(self, image_path, threshold=0.50):
        """Return the best matching visitor ID or Unknown."""
        query_embedding = self.get_embedding(image_path)

        if query_embedding is None:
            return {
                "visitor_id": None,
                "status": "no_single_face",
                "similarity": None,
            }

        if not self.visitors:
            return {
                "visitor_id": None,
                "status": "no_enrolled_visitors",
                "similarity": None,
            }

        best_visitor = None
        best_similarity = -1.0

        for visitor_id, reference_embeddings in self.visitors.items():
            # Compare the query with every reference image for this visitor.
            similarities = [
                float(np.dot(query_embedding, reference))
                for reference in reference_embeddings
            ]

            # Average the strongest 3 comparisons when available.
            top_scores = sorted(similarities, reverse=True)[:3]
            visitor_score = float(np.mean(top_scores))

            if visitor_score > best_similarity:
                best_similarity = visitor_score
                best_visitor = visitor_id

        if best_similarity >= threshold:
            result = {
                "visitor_id": best_visitor,
                "status": "recognized",
                "similarity": round(best_similarity, 4),
            }
        else:
            result = {
                "visitor_id": None,
                "status": "unknown",
                "similarity": round(best_similarity, 4),
            }

        return result


if __name__ == "__main__":
    engine = FaceRecognitionEngine()
    print("Face recognition engine initialized.")

    engine.load_visitors()

    # Test against one of the enrolled frames.
    test_image = (
        Path(__file__).resolve().parent
        / "data"
        / "visitors"
        / "visitor-001"
        / "frame_001.jpg"
    )

    result = engine.recognize_face(test_image)
    print("\nRecognition result:")
    print(result)
