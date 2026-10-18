from contextlib import asynccontextmanager
from pathlib import Path
import tempfile

from fastapi import FastAPI, File, HTTPException, UploadFile

from recognition import FaceRecognitionEngine

MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10 MB


@asynccontextmanager
async def lifespan(app: FastAPI):
    engine = FaceRecognitionEngine()
    engine.load_visitors()
    app.state.recognition_engine = engine
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/recognize")
async def recognize_face(file: UploadFile = File(...)):
    if file.content_type and not file.content_type.startswith("image/"):
        raise HTTPException(status_code=415, detail="Upload an image file.")

    image_data = await file.read(MAX_IMAGE_SIZE + 1)

    if not image_data:
        raise HTTPException(status_code=400, detail="Empty image.")

    if len(image_data) > MAX_IMAGE_SIZE:
        raise HTTPException(status_code=413, detail="Image exceeds 10 MB.")

    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp:
            temp.write(image_data)
            temp_path = Path(temp.name)

        return app.state.recognition_engine.recognize_face(str(temp_path))

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    finally:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)
