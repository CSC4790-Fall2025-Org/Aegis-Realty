# Aegis Realty

Aegis Realty is an AI-powered real estate investment and property management 
platform built with a React frontend and a FastAPI backend. It provides an integrated 
solution to simplify property analysis, risk assessment, and administration for investors

## Features
- Core Investment Analysis: Users can analyze any property address to receive instant, 
  comprehensive reports on its investment potential, including Cap Rate and ROI projections
- AI-Powered Insights: Utilizes the Google Gemini API to synthesize complex
- Property Data Retrieval: Integrates the RentCast API (and can be expanded with the Zillow API) 
  to access up-to-date public records, sales history, and rental estimates
- Project Management Tools (Stretch Goals):
  - Property Management: Tools to manage tenants, track rental payments, 
    and schedule maintenance tasks
  - Document Analysis: AI functionality to upload legal documents 
    (e.g., leases, inspection reports) and receive automated summaries and red flag detection
- Database Scalability: Uses Alembic for reliable database migrations
- User Authentication: Secure user sign-up and login via Firebase Authentication

## Prerequisites
- Python 3.10 or higher
- Node.js 18.x
- npm or Yarn (package manager for Node.js)
- Git (used to clone the repository)
- PostgreSQL (Neon, AWS RDS, or local Docker instance)

## API Keys
You will need API keys for:
- [Firebase](https://console.firebase.google.com/u/0/)
- [Firebase Admin SDK](https://firebase.google.com/docs/admin/setup)
- [Gemini API](https://aistudio.google.com/prompts/new_chat)
- [RentCast API ](https://app.rentcast.io/app)

Create a `.env` file in the root of the backend directory with the following content:

```bash
FIREBASE_CREDENTIALS=app/your_firebase_admin_sdk_credentials_json
GENAI_API_KEY=your_gemini_api_key
RENTCAST_API_KEY=your_rentcast_api_key
DATABASE_URL=your_postgress_url
```

Create a `.env` file in the root of the frontend directory with the following content:
```bash
VITE_FIREBASE_API_KEY=your_firebase_key
VITE_FIREBASE_AUTH_DOMAIN=your_firebase_auth_domain
VITE_FIREBASE_PROJECT_ID=your_firebase_project_id
VITE_FIREBASE_STORAGE_BUCKET=your_firebase_storage_bucket
VITE_FIREBASE_MESSAGING_SENDER_ID=your_firebase_messaging_sender_id
VITE_FIREBASE_APP_ID=your_firebase_app_id
VITE_FIREBASE_MEASUREMENT_ID=your_firebase_measurement_id

VITE_BACKEND_URL=your_backend_url
```

> The application uses [`python-dotenv`](https://pypi.org/project/python-dotenv/) 
> to automatically load environment variables from the `.env` file. 
> No manual loading is required.

## Getting Started

Follow these steps to set up and run the project locally:

### 1. Clone the Repository

```bash
git clone https://github.com/your-repo/Aegis-Realty.git
cd Aegis-Realty
````

### 2. Backend Setup

```bash
cd backend
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```
The backend requires a PostgreSQL database. You can use Neon or any compatible PostgreSQL provider.
Set your connection string in DATABASE_URL in the .env file

### 3. Database Migrations

Once your database is set up, run the migrations from the 
backend/ directory to create the tables:

```
# Apply the migration
alembic upgrade head
```

### 4. Frontend Setup
```bash
cd ../frontend
npm install
```

### 5. Environment Configuration
- Add your API keys to the .env files in `backend/` and `frontend/`
- Configure Firebase in `frontend/src/services/firebase.js`

### 6. Running the Application
- Backend (from `backend/`):
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
- Frontend (from `frontend/`):
```bash
npm run dev
```

## Usage
- Sign up and log in via the web interface
- Input a property address on the dashboard to generate an AI-powered investment analysis report
- View the Cap Rate and ROI projections to quickly assess profitability

## Directory Structure
- `backend/` — FastAPI backend, business logic, API integrations
- `frontend/` — React app, UI components, pages, services