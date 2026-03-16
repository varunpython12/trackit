# TrackIt 📦 | Logistics Tracking System

A professional-grade, full-stack shipment management application. This system allows logistics managers to create shipments, track real-time status updates, and maintain a permanent audit trail of every status change.

## 🚀 Key Features
* **Full CRUD Operations:** Create, Read, and Update shipment data via a RESTful API.
* **Audit Trail (One-to-Many):** Every status change is automatically logged in a separate history table with millisecond-precise timestamps.
* **State-Machine Logic:** The system automatically captures the `received_at` timestamp only when a shipment is marked as "Delivered."
* **Interactive Dashboard:** A clean, user-friendly interface for managing shipments without writing code.

## 🛠️ Tech Stack
* **Backend:** Python 3.x, Flask (REST API)
* **Database:** SQLAlchemy ORM with SQLite (Relational Schema)
* **Frontend:** Streamlit (UI), Pandas (Data Presentation)
* **Version Control:** Git (Feature-branch workflow)

## 📁 Project Structure
```text
TrackIt/
├── app/
│   ├── __init__.py    # App Factory
│   ├── models.py      # Database Schema (Shipment & StatusLog)
│   └── routes.py      # API Endpoints (POST, GET, PUT)
├── dashboard.py       # Streamlit Frontend
├── run.py             # Entry point for Flask
├── requirements.txt   # Project Dependencies
└── README.md          # Documentation
```
## ⚙️ Setup & Installation
###1. Clone the Repository
```text
Bash

git clone [https://github.com/your-username/TrackIt.git](https://github.com/your-username/TrackIt.git)
cd TrackIt
```

### 2. Set Up Virtual Environment
```text
Bash

python -m venv venv
# On Windows
venv\Scripts\activate
# On Mac/Linux
source venv/bin/activate
```
### 3. Install Dependencies
```text
Bash

pip install -r requirements.txt
```
### 4. Initialize the Database
Run this one-liner to create your SQLite database tables based on the models:
```text
Bash

python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"
```
## 🖥️ How to Run
To run the full-stack application, you need to open two terminals:
Terminal 1: Start the Backend (API)
```text
Bash
python run.py
```
Terminal 2: Start the Frontend (Dashboard)
```text
Bash
streamlit run dashboard.py
```
## 📊 API Documentation (Quick Reference)

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| **POST** | `/api/shipments` | Register a new shipment |
| **GET** | `/api/shipments/<id>` | Fetch shipment details + History logs |
| **PUT** | `/api/shipments/<id>` | Update status (Logs event to History) |