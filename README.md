# Career Study Assistant

A full-stack application to help you track and manage your career study sessions.

## Project Structure

```
career-study-assistant/
├── backend/
│   ├── app.py              # Flask API server
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.jsx         # Main React component
│   │   ├── index.css       # Styles with neon rainbow gradient
│   │   └── main.jsx        # React entry point
│   └── package.json        # Node dependencies
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## Getting Started

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm

### Backend Setup

1. Create virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r backend/requirements.txt
```

3. Run the server:
```bash
python backend/app.py
```

The API will be available at `http://localhost:5000`

### Frontend Setup

1. Navigate to frontend:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create `.env` file:
```
VITE_API_BASE=http://localhost:5000
```

4. Run dev server:
```bash
npm run dev
```

The app will be available at `http://localhost:5173`

## API Endpoints

- `GET /api/health` - Health check
- `GET /api/settings` - Get study settings
- `POST /api/settings` - Update study settings
- `GET /api/study/sessions` - List all study sessions
- `POST /api/study/sessions` - Create a new study session
- `GET /api/study/today` - Get today's progress

## Features

- Log study sessions with topic, duration, and notes
- Track daily study goals
- View study session history
- Rainbow neon animated background

## Technologies

- **Backend**: Flask, Flask-CORS
- **Frontend**: React, Vite
- **Styling**: CSS3 with animations

<img width="664" height="604" alt="Screenshot 2026-01-17 at 6 24 37 PM" src="https://github.com/user-attachments/assets/48c8e88d-2c10-4e66-8a4c-daefc3c78320" />


