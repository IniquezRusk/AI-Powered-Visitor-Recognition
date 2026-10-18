from insightface.app import FaceAnalysis

def main():
    print("Initializing InsightFace...")

    app = FaceAnalysis(name="buffalo_l", 
    providers=()"CudaExecutionProvider",
    )

    app.prepare(ctx_id=0, det_size=(640, 640))

    print("Model loaded successfully!")
    print("Detection and recognition are ready.")

    if __name__ == "__main__":
        main()
