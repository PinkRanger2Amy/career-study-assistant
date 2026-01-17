import { useEffect, useState } from "react";

const API = import.meta.env.VITE_API_BASE;

export default function App() {
  const [topic, setTopic] = useState("SQL");
  const [minutes, setMinutes] = useState(30);
  const [notes, setNotes] = useState("");
  const [sessions, setSessions] = useState([]);
  const [today, setToday] = useState(null);
  const [goal, setGoal] = useState(30);

  async function loadAll() {
    const [sRes, tRes, gRes] = await Promise.all([
      fetch(`${API}/api/study/sessions`),
      fetch(`${API}/api/study/today`),
      fetch(`${API}/api/settings`),
    ]);
    setSessions(await sRes.json());
    setToday(await tRes.json());
    const settings = await gRes.json();
    setGoal(settings.daily_study_goal_minutes ?? 30);
  }

  useEffect(() => {
    (async () => {
      await loadAll();
    })();
  }, []);

  async function addSession(e) {
    e.preventDefault();
    await fetch(`${API}/api/study/sessions`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ topic, minutes: Number(minutes), notes }),
    });
    setNotes("");
    await loadAll();
  }

  async function updateGoal(e) {
    e.preventDefault();
    await fetch(`${API}/api/settings`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ daily_study_goal_minutes: Number(goal) }),
    });
    await loadAll();
  }

  return (
    <div style={{ maxWidth: 900, margin: "40px auto", fontFamily: "system-ui", padding: 16 }}>
      <h1>Career / Study Assistant</h1>

      <section style={{ padding: 16, border: "1px solid #ddd", borderRadius: 12, marginBottom: 16 }}>
        <h2>Today</h2>
        {today ? (
          <p>
            Goal: <b>{today.goal}</b> min — Done: <b>{today.done}</b> min — Remaining: <b>{today.remaining}</b> min
          </p>
        ) : (
          <p>Loading...</p>
        )}

        <form onSubmit={updateGoal} style={{ display: "flex", gap: 8, alignItems: "center" }}>
          <label>Daily goal (minutes):</label>
          <input type="number" value={goal} onChange={(e) => setGoal(e.target.value)} min="1" />
          <button type="submit">Save goal</button>
        </form>
      </section>

      <section style={{ padding: 16, border: "1px solid #ddd", borderRadius: 12, marginBottom: 16 }}>
        <h2>Log a study session</h2>
        <form onSubmit={addSession} style={{ display: "grid", gap: 10 }}>
          <div style={{ display: "flex", gap: 10 }}>
            <input value={topic} onChange={(e) => setTopic(e.target.value)} placeholder="Topic (SQL/Python)" />
            <input type="number" value={minutes} onChange={(e) => setMinutes(e.target.value)} min="1" />
          </div>
          <textarea value={notes} onChange={(e) => setNotes(e.target.value)} placeholder="Notes (optional)" />
          <button type="submit">Add session</button>
        </form>
      </section>

      <section style={{ padding: 16, border: "1px solid #ddd", borderRadius: 12 }}>
        <h2>Sessions</h2>
        {sessions.length === 0 ? (
          <p>No sessions yet.</p>
        ) : (
          <ul>
            {sessions.slice().reverse().map((s, idx) => (
              <li key={idx}>
                <b>{s.topic}</b> — {s.minutes} min ({s.date})
                {s.notes ? ` — ${s.notes}` : ""}
              </li>
            ))}
          </ul>
        )}
      </section>
    </div>
  );
}

