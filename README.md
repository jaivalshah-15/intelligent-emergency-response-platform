#  Intelligent Emergency Response Platform

An emergency incident monitoring and response platform designed to help authorities coordinate incidents, alerts, emergency resources, and response activities from a single dashboard.

The platform collects incident reports, classifies emergencies using rule-based AI assistance, detects possible duplicate incidents, recommends suitable resources, manages assignments, generates alerts, provides AI-assisted incident summaries, and displays real-time analytics and incident locations on a map.

---

##  Problem Statement

During large-scale emergencies such as fires, floods, road accidents, industrial incidents, and medical emergencies, information can arrive from multiple disconnected sources.

This can make it difficult to:

* Understand the current emergency situation.
* Identify high-priority incidents.
* Detect duplicate reports.
* Find suitable emergency resources.
* Coordinate resource assignments.
* Monitor alerts and incidents in real time.
* Analyze the overall emergency response situation.

The goal of this project is to provide a centralized platform that helps organize this information and support faster, more coordinated emergency response.

---

##  Solution

The Intelligent Emergency Response Platform provides a centralized dashboard where emergency incidents can be reported, analyzed, monitored, and coordinated.

The system follows this workflow:

```text
Incident Report
      ↓
AI Classification
      ↓
Duplicate Detection
      ↓
Resource Recommendation
      ↓
Resource Assignment
      ↓
Emergency Alerts
      ↓
AI Assistance
      ↓
Real-Time Dashboard
      ↓
Analytics
```

---

#  Features

## 1.  Incident Reporting

Users can report emergencies by providing:

* Incident title
* Description
* Incident type
* Source
* Address
* Latitude
* Longitude

Supported incident types include:

```text
FIRE
FLOOD
ACCIDENT
INDUSTRIAL
MEDICAL
OTHER
```

Supported sources include:

```text
CITIZEN
SENSOR
EMERGENCY_CALL
FIELD_TEAM
```

---

## 2.  AI Incident Classification

The platform analyzes the incident title and description to identify:

* Incident type
* Severity
* Priority
* Classification confidence
* Reasoning behind the classification

The current implementation uses a lightweight rule-based classification service designed for the hackathon prototype.

Example:

```text
Input:
"Large fire with heavy smoke and people trapped inside a factory"

Output:
Incident Type: FIRE
Severity: CRITICAL
Priority: HIGH
Confidence: 95%
```

---

## 3.  Duplicate Incident Detection

The platform checks incoming incidents for possible duplicate reports.

This helps identify multiple reports describing the same emergency and prevents unnecessary duplication during response coordination.

Duplicate candidates can be reviewed and their status can be updated through the API.

---

## 4.  Resource Recommendation

The platform recommends suitable emergency resources for an incident based on factors such as:

* Resource type
* Incident type
* Severity
* Priority
* Distance

Example:

```text
Fire Incident
    ↓
Recommended Resources
    ├── Fire Truck
    ├── Rescue Team
    └── Ambulance
```

Recommendations receive a score and explanation for the recommendation.

---

## 5.  Resource Assignment

Recommended resources can be assigned to incidents.

The system tracks resource status such as:

```text
AVAILABLE
ASSIGNED
```

The assignment workflow supports:

```text
Available Resource
       ↓
Assign to Incident
       ↓
Resource becomes ASSIGNED
       ↓
Release Assignment
       ↓
Resource becomes AVAILABLE
```

---

## 6.  Emergency Alerts

The platform automatically generates alerts for important incidents.

Alert levels include:

```text
CRITICAL_INCIDENT
HIGH_PRIORITY
```

Alerts can have statuses such as:

```text
ACTIVE
ACKNOWLEDGED
RESOLVED
```

Operators can acknowledge and resolve alerts directly from the dashboard.

---

## 7. 🗺️ Interactive Emergency Map

The dashboard includes an interactive map using Leaflet.

Incidents with valid latitude and longitude are displayed as markers.

Clicking a marker shows incident information such as:

* Title
* Incident type
* Severity
* Priority
* Status

---

## 8.  Real-Time WebSocket Updates

The platform includes WebSocket support for real-time dashboard updates.

WebSocket endpoint:

```text
/api/ws
```

The frontend connects to the backend using WebSocket and refreshes important dashboard information when new incident events are received.

The dashboard displays:

```text
● Live
```

when the WebSocket connection is active.

---

## 9.  AI Assistance

The platform provides an AI-assisted incident summary for individual incidents.

The assistant provides:

* Incident summary
* Current situation
* Key findings
* Recommended actions
* Resource needs
* Generation source

Example resource needs for a fire incident:

```text
FIRE_TRUCK
RESCUE_TEAM
AMBULANCE
```

---

## 10.  Emergency Analytics

The platform provides real-time emergency statistics including:

* Total incidents
* Active incidents
* Critical incidents
* High-priority incidents
* Total alerts
* Active alerts
* Resolved alerts
* Total resources
* Available resources
* Assigned resources
* Total assignments
* Active assignments

It also provides breakdowns by:

```text
Incident Type
Incident Severity
Incident Priority
Alert Level
```

---

# Technology Stack

## Frontend

* React
* Vite
* React-Leaflet
* Leaflet
* JavaScript
* CSS

## Backend

* Python
* FastAPI
* Uvicorn
* SQLAlchemy
* Pydantic
* Alembic

## Database

* PostgreSQL

## Real-Time Communication

* WebSocket

## Development & Tools

* Docker
* Docker Compose
* Git
* GitHub

---

# Project Structure

```text
intelligent-emergency-response-platform/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/
│   │   │       ├── incidents.py
│   │   │       ├── duplicates.py
│   │   │       ├── recommendations.py
│   │   │       ├── assignments.py
│   │   │       ├── alerts.py
│   │   │       ├── resources.py
│   │   │       ├── hospitals.py
│   │   │       ├── teams.py
│   │   │       ├── websocket.py
│   │   │       ├── ai_assistance.py
│   │   │       └── analytics.py
│   │   │
│   │   ├── core/
│   │   ├── crud/
│   │   ├── db/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── main.py
│   │
│   ├── alembic/
│   ├── tests/
│   ├── requirements.txt
│   └── alembic.ini
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── ...
│   ├── package.json
│   └── vite.config.js
│
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

# ⚙️ Local Setup

## Prerequisites

Install the following before running the project:

* Python 3
* Node.js and npm
* Docker Desktop
* Git

---

## 1. Clone the Repository

```bash
git clone https://github.com/jaivalshah-15/intelligent-emergency-response-platform.git
cd intelligent-emergency-response-platform
```

---

#  2. Start PostgreSQL

The project uses PostgreSQL through Docker Compose.

From the project root:

```bash
docker compose up -d postgres
```

Check the database container:

```bash
docker compose ps
```

The PostgreSQL service should be running.

---

#  3. Setup Backend

Go to the backend:

```bash
cd backend
```

Create a virtual environment:

### Windows

```powershell
python -m venv venv
```

Activate it in PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, you can run the project directly with:

```powershell
.\venv\Scripts\python.exe
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

---

#  4. Configure Database Environment Variable

The backend reads the database connection from:

```text
DATABASE_URL
```

For local development, create:

```text
backend/.env
```

and add your local PostgreSQL connection string:

```env
DATABASE_URL=your_local_postgresql_connection_string
```

Do not commit `.env` to GitHub.

---

# 5. Run Database Migrations

From the `backend` directory:

```bash
alembic upgrade head
```

This creates the required database tables.

---

# 6. Start the Backend

From:

```text
backend/
```

run:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

If the `uvicorn` command is not recognized on Windows, use:

```powershell
.\venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at:

```text
http://localhost:8000
```

Health check:

```text
http://localhost:8000/api/health
```

Swagger API documentation:

```text
http://localhost:8000/docs
```

---

# 💻 7. Setup Frontend

Open another terminal and go to:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The frontend will normally be available at:

```text
http://localhost:5173
```

---

# 🔗 8. Frontend Backend Configuration

The frontend uses:

```text
VITE_API_URL
```

for the backend API URL.

For local development, the application defaults to:

```text
http://localhost:8000
```

For deployment, create a frontend environment variable such as:

```env
VITE_API_URL=https://your-backend-url
```

---

#  API Overview

The backend provides REST API endpoints for:

```text
/api/health
/api/incidents/
/api/incidents/{incident_id}
/api/incidents/{incident_id}/classify
/api/incidents/{incident_id}/summary

/api/duplicates/
/api/duplicates/{candidate_id}
/api/duplicates/{candidate_id}/status

/api/resources/
/api/resources/{resource_id}

/api/recommendations/
/api/recommendations/generate/{incident_id}
/api/recommendations/{incident_id}
/api/recommendations/{recommendation_id}/status

/api/assignments/
/api/assignments/{assignment_id}/release

/api/alerts/
/api/alerts/{alert_id}
/api/alerts/{alert_id}/acknowledge
/api/alerts/{alert_id}/resolve

/api/hospitals/
/api/teams/

/api/analytics/

/api/ws
```

Full interactive documentation is available through FastAPI Swagger:

```text
http://localhost:8000/docs
```

---

#  Testing

Backend tests are located in:

```text
backend/tests/
```

Run all tests from the backend directory:

```bash
python -m pytest -q
```

or on Windows without activating the virtual environment:

```powershell
.\venv\Scripts\python.exe -m pytest -q
```

The test suite covers major services including:

* Incident classification
* Duplicate detection
* Resource recommendation
* Resource assignment
* AI assistance
* Analytics

---

#  Example Emergency Workflow

A typical emergency response flow looks like:

```text
1. Citizen reports an incident
           ↓
2. Incident is stored in PostgreSQL
           ↓
3. AI classification identifies type/severity/priority
           ↓
4. Possible duplicate incidents are checked
           ↓
5. Suitable emergency resources are recommended
           ↓
6. Emergency resource is assigned
           ↓
7. Alerts are generated
           ↓
8. Dashboard receives real-time updates
           ↓
9. AI assistance summarizes the situation
           ↓
10. Analytics reflect the updated response state
```

---

#  Security Notes

Do not commit sensitive information to GitHub.

Never commit:

```text
.env
database passwords
API keys
private credentials
backend/venv/
frontend/node_modules/
frontend/dist/
```

Use environment variables for production secrets and database credentials.

---

#  Deployment

The project can be deployed using a structure such as:

```text
React/Vite Frontend
        ↓
Vercel / Static Hosting
        ↓
FastAPI Backend
        ↓
Render Web Service
        ↓
PostgreSQL
```

For production:

* The backend should use a production PostgreSQL connection through `DATABASE_URL`.
* The frontend should use `VITE_API_URL` pointing to the deployed backend.
* CORS should allow the deployed frontend domain through `FRONTEND_URLS`.
* WebSocket connections should use `wss://` in production.

---

#  Screenshots

Add project screenshots here after finalizing the UI.

Example:

```text
docs/
├── dashboard.png
├── map.png
├── alerts.png
├── analytics.png
└── ai-assistance.png
```

Then reference them in this README:

```markdown
![Emergency Dashboard](docs/dashboard.png)
```

---

# 🔮 Future Improvements

Possible future enhancements include:

* GPS-based automatic location detection
* Address-to-coordinate geocoding
* Integration with real emergency call systems
* Sensor and IoT integration
* Advanced machine-learning models
* Hospital capacity integration
* Traffic-aware resource routing
* SMS/email emergency notifications
* Role-based authentication
* Historical analytics and reporting
* Cloud-based monitoring and scaling

---

#  Team

**Project:** Intelligent Emergency Response Platform
**Problem Statement:** PS-9 - Intelligent Emergency Response & Resource Coordination Platform

Add your team members here:

```text
1. Name - Role
2. Name - Role
3. Name - Role
4. Name - Role
```

---

# License

This project was developed as a hackathon/academic project.
