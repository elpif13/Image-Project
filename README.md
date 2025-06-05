## 🚀 Getting Started

### 📦 Prerequisites

- Python 3.8 or higher
- pip
- (Optional) `virtualenv`

---

### ⚙️ Installation


# 1. Clone the repository
git clone https://github.com/elpif13/Image-Project.git
cd Image-Project

# 2. Create a virtual environment
python -m venv env
source env/bin/activate  # Windows: env\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run migrations
python manage.py migrate

# 5. Start the server
python manage.py runserver
