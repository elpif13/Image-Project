# 🖼️ Image Project

A simple Django-based REST API for uploading images, resizing them to 224x224, retrieving metadata, listing all uploaded images, and deleting them.

---

## 🚀 Getting Started

### 📦 Prerequisites

- Python 3.8 or higher  
- pip  
- (Optional) `virtualenv`

---

### ⚙️ Installation

1. Clone the repository
```bash
git clone https://github.com/elpif13/Image-Project.git
cd Image-Project
```

2. Create a virtual environment
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run migrations
```bash
python manage.py migrate
```

5. Start the server
```bash
python manage.py runserver
```

---

## 📡 API Endpoints

| Method   | Endpoint                    | Description                                 |
|----------|-----------------------------|---------------------------------------------|
| `POST`   | `/upload/`                  | Upload an image                             |
| `GET`    | `/images/<filename>`        | Get resized image (224x224)                 |
| `GET`    | `/metadata/<filename>`      | Get metadata of an image                    |
| `GET`    | `/images/`                  | List all uploaded images                    |
| `DELETE` | `/images/delete/<filename>` | Delete original, resized image and metadata |

---

## 🧪 Example Usage

### Upload an image
```bash
curl -X POST -F "image=@/path/to/image.jpg" http://127.0.0.1:8000/upload/
```

### Retrieve resized image
```bash
curl http://127.0.0.1:8000/images/test-image.jpg
```

### Delete an image
```bash
curl -X DELETE http://127.0.0.1:8000/images/delete/<filename>
```
