# FastAPI Log Parser

A simple FastAPI application that parses Apache log files, counts errors, filters recent logs, and sends email alerts if the error rate exceeds a threshold.

---

## 🚀 Features

1. Counts `notice` and `error` logs and serves results via FastAPI.  
2. Saves error logs to CSV and JSON files.  
3. Checks if errors in the last hour exceed a threshold (default: 10) and sends email alerts.  

---

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/fastapi-log-parser.git
cd fastapi-log-parser
```

### 2. Create and activate a virtual environment

#### On Windows (PowerShell):
```powershell
python -m venv .venv
.venv\Scripts\Activate
```

#### On macOS / Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create a `.env` file in the project root
```text
MY_EMAIL=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
TO_EMAIL=recipient_email@gmail.com
```

> 💡 **Note:** If using Gmail, generate an [app-specific password](https://support.google.com/accounts/answer/185833) instead of your regular password.

---

## ▶️ Usage

Start the FastAPI application:
```bash
uvicorn main:app --reload
```

Then open your browser or Postman at:
👉 [http://127.0.0.1:8000/logs/](http://127.0.0.1:8000/logs/)

You’ll see:
- Log counts (e.g., `notice` and `error`)  
- Number of errors in the last hour  
- CSV and JSON files automatically generated with filtered errors  

---

## 📁 Example API Response

```json
{
  "Logs": {
    "notice": 1405,
    "error": 595
  },
  "ErrorsLastHours": 12
}
```

---

Made with ❤️ using **Python + FastAPI + Pandas**
