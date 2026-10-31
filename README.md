# AI-Powered Smart Visitor Recognition and Information Assistant

An AI-powered visitor recognition system developed as a Computer Science capstone project at Prairie View A&M University.

The system uses facial recognition to identify registered visitors, maintain recognition activity records, and provide a foundation for personalized information and intelligent interactions.

**Faculty Mentors:** Dr. Shuvo and Dr. Yang

## Project Documentation

For the complete project overview, objectives, technical scope, and expected deliverables, see [Project Description](project_desc.md).

## Technology Stack

- **Python** – Core programming language
- **FastAPI** – Backend REST API
- **InsightFace** – Facial detection and recognition
- **Buffalo_L** – Pretrained facial recognition model
- **OpenCV** – Image processing and camera access
- **ONNX Runtime** – Neural network inference
- **Uvicorn** – ASGI server

## Current Features

- Webcam-based visitor enrollment.
- Facial detection and recognition.
- Facial embedding generation and comparison.
- Image-based recognition through REST API.
- Recognition activity logging.
- Visitor recognition analytics.
- Interactive API documentation.

## Repository Structure

```text
AI-Powered-Visitor-Recognition/
│
├── Backend/
│   ├── data/
│   │   ├── visitors/
│   │   └── recognition_events.jsonl
│   │
│   ├── models/
│   ├── activity.py
│   ├── camera.py
│   ├── enroll.py
│   ├── main.py
│   ├── recognition.py
│   ├── requirements.txt
│   └── setup.ps1
│
├── README.md
└── project_desc.md
```

## Installation

### Prerequisites

- Python 3.11 or 3.12 recommended.
- Git.
- A webcam for visitor enrollment.

### 1. Clone the Repository

```bash
git clone https://github.com/IniquezRusk/AI-Powered-Visitor-Recognition.git
```

### 2. Navigate to the Backend

```bash
cd AI-Powered-Visitor-Recognition/Backend
```

### 3. Run the Setup Script

On Windows PowerShell:

```powershell
.\setup.ps1
```

The setup script creates a virtual environment, installs the required Python dependencies, and initializes the InsightFace `buffalo_l` model.

### 4. Start the Backend

```powershell
.\.venv\Scripts\Activate.ps1
python -m uvicorn main:app --reload
```

The backend will run at:

`http://127.0.0.1:8000`

## API Documentation

Interactive API documentation is available through FastAPI's Swagger UI:

`http://127.0.0.1:8000/docs`

### Available Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Check backend status |
| POST | `/recognize` | Recognize a visitor from an uploaded image |
| GET | `/activity` | Retrieve recognition activity |
| GET | `/analytics/summary` | Retrieve recognition statistics |

## Visitor Enrollment

To enroll a visitor using a connected webcam:

```powershell
python enroll.py
```

Enrolled visitor information and facial embeddings are stored in the backend's visitor data directory.

## Recognition Workflow

1. Capture and enroll a visitor's face.
2. Generate facial embeddings using InsightFace.
3. Submit an image to the recognition API.
4. Generate an embedding from the submitted image.
5. Compare the embedding against enrolled visitor records.
6. Return the recognition result.
7. Record the recognition event for activity tracking and analytics.

## Project Status

**Currently in development.**

The backend supports visitor enrollment, facial recognition, activity logging, and analytics. Additional features and frontend integration are being developed.

## Privacy and Security

Facial embeddings and visitor records are sensitive biometric information. Do not commit private visitor data, credentials, or other sensitive information to the repository.

## Contributors

Computer Science Capstone Project  
Prairie View A&M University

**Faculty Mentors:** Dr. Shuvo and Dr. Yang