from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from pathlib import Path
from datetime import datetime, date

app = Flask(__name__)
CORS(app)  # allow your React app to call this API

DATA_FILE = Path("assistant_data.json")

def load_data():
    if DATA_FILE.exists():
        try:
            return json.loads(DATA_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    return {
        "study_sessions": [],
        "settings": {"daily_study_goal_minutes": 30}
    }

def save_data(data):
    DATA_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")

def now_stamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M")

def today_str():
    return date.today().strftime("%Y-%m-%d")

@app.get("/api/health")
def health():
    return {"ok": True}

@app.get("/api/settings")
def get_settings():
    data = load_data()
    return jsonify(data["settings"])

@app.post("/api/settings")
def update_settings():
    data = load_data()
    payload = request.get_json(force=True)
    goal = payload.get("daily_study_goal_minutes")
    if isinstance(goal, int) and goal > 0:
        data["settings"]["daily_study_goal_minutes"] = goal
        save_data(data)
    return jsonify(data["settings"])

@app.get("/api/study/sessions")
def list_sessions():
    data = load_data()
    return jsonify(data["study_sessions"])

@app.post("/api/study/sessions")
def add_session():
    data = load_data()
    payload = request.get_json(force=True)

    topic = (payload.get("topic") or "").strip()
    minutes = payload.get("minutes")

    if not topic:
        return jsonify({"error": "topic is required"}), 400
    if not isinstance(minutes, int) or minutes <= 0:
        return jsonify({"error": "minutes must be a positive integer"}), 400

    session = {
        "topic": topic,
        "minutes": minutes,
        "notes": (payload.get("notes") or "").strip(),
        "date": now_stamp(),
        "day": today_str(),
    }
    data["study_sessions"].append(session)
    save_data(data)
    return jsonify(session), 201

@app.get("/api/study/today")
def today_progress():
    data = load_data()
    goal = data["settings"].get("daily_study_goal_minutes", 30)
    t = today_str()
    done = sum(s["minutes"] for s in data["study_sessions"] if s.get("day") == t)
    return jsonify({"date": t, "goal": goal, "done": done, "remaining": max(goal - done, 0)})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
