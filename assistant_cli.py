import json
import random
from datetime import datetime, date
from pathlib import Path

DATA_FILE = Path("assistant_data.json")


def load_data():
    if DATA_FILE.exists():
        try:
            return json.loads(DATA_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    return {
        "jobs": [],
        "study_sessions": [],
        "settings": {
            "daily_study_goal_minutes": 30,
            "preferred_topics": ["SQL", "Python", "Interview", "Portfolio"],
        },
    }


def save_data(data):
    DATA_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")


def now_stamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def today_str():
    return date.today().strftime("%Y-%m-%d")


def menu():
    print("Career/Study Assistant 🤖 (Study Mode)")
    print("1) Log study session")
    print("2) Today progress + streak")
    print("3) Study summary")
    print("4) What should I study today?")
    print("5) SQL practice")
    print("6) Update study settings")
    print("7) Exit")


def log_study(data):
    print("\n--- Log Study Session ---")
    topic = input("Topic (SQL/Python/Interview/Portfolio/etc.): ").strip()
    minutes_str = input("Minutes studied: ").strip()
    notes = input("What did you work on? (optional): ").strip()

    try:
        minutes = int(minutes_str)
        if minutes <= 0:
            raise ValueError
    except ValueError:
        print("❌ Minutes must be a positive number.\n")
        return

    session = {
        "topic": topic,
        "minutes": minutes,
        "notes": notes,
        "date": now_stamp(),
        "day": today_str(),
    }
    data["study_sessions"].append(session)
    save_data(data)
    print("✅ Logged study session.\n")


def minutes_today(data):
    t = today_str()
    return sum(s["minutes"] for s in data["study_sessions"] if s.get("day") == t)


def compute_streak(data):
    # Streak = consecutive days with >= 1 study session
    days = sorted({s.get("day") for s in data["study_sessions"] if s.get("day")})
    if not days:
        return 0

    # Convert to date objects
    day_objs = [datetime.strptime(d, "%Y-%m-%d").date() for d in days]
    day_set = set(day_objs)

    streak = 0
    current = date.today()
    while current in day_set:
        streak += 1
        current = current.fromordinal(current.toordinal() - 1)
    return streak


def today_progress(data):
    goal = data.get("settings", {}).get("daily_study_goal_minutes", 30)
    done = minutes_today(data)
    streak = compute_streak(data)

    print("\n--- Today Progress ---")
    print(f"Date: {today_str()}")
    print(f"Daily goal: {goal} minutes")
    print(f"Done today: {done} minutes")

    if done >= goal:
        print("✅ Goal met! Great work.\n")
    else:
        print(f"⏳ You need {goal - done} more minutes to hit your goal.\n")

    print(f"🔥 Study streak: {streak} day(s)\n")


def study_summary(data):
    print("\n--- Study Summary ---")
    sessions = data["study_sessions"]
    if not sessions:
        print("No study sessions logged yet.\n")
        return

    total_minutes = sum(s["minutes"] for s in sessions)

    by_topic = {}
    for s in sessions:
        by_topic[s["topic"]] = by_topic.get(s["topic"], 0) + s["minutes"]

    print(f"Total time: {total_minutes} minutes")
    print("By topic:")
    for topic, mins in sorted(by_topic.items(), key=lambda x: x[1], reverse=True):
        print(f" - {topic}: {mins} minutes")
    print()


def recommend_topic(data):
    prefs = data.get("settings", {}).get("preferred_topics", ["SQL", "Python"])
    # Look at last 7 sessions to avoid repeating the same thing every time
    recent = data["study_sessions"][-7:]
    recent_topics = [s["topic"].strip().lower() for s in recent if s.get("topic")]

    # If SQL appears more than Python recently, recommend Python, otherwise SQL
    sql_count = sum(1 for t in recent_topics if "sql" in t)
    py_count = sum(1 for t in recent_topics if "python" in t)

    # Default logic with variety
    if sql_count > py_count:
        candidates = [t for t in prefs if t.lower() != "sql"] or prefs
    elif py_count > sql_count:
        candidates = [t for t in prefs if t.lower() != "python"] or prefs
    else:
        candidates = prefs

    return random.choice(candidates)


def what_to_study(data):
    print("\n--- What Should I Study Today? ---")
    goal = data.get("settings", {}).get("daily_study_goal_minutes", 30)
    done = minutes_today(data)

    if done >= goal:
        print("✅ You already hit your goal today.")
        print("If you want bonus work, do 10 minutes of SQL practice or 1 interview answer.\n")
        return

    topic = recommend_topic(data)
    remaining = goal - done

    print(f"Suggested focus: {topic}")
    print(f"Plan: {remaining} minutes total")
    if topic.lower() == "sql":
        print(" - 10 min: review joins + group by")
        print(" - 10 min: do SQL practice quiz (menu option 5)")
        print(" - remaining: write 1 query from memory (SELECT + WHERE + ORDER BY)\n")
    elif topic.lower() == "python":
        print(" - 10 min: lists/dicts practice")
        print(" - 10 min: write a small function + test it")
        print(" - remaining: read + refactor 20 lines of your code\n")
    elif topic.lower() == "interview":
        print(" - 10 min: write 1 STAR story (challenge + result)")
        print(" - 10 min: practice “Tell me about yourself”")
        print(" - remaining: review the job posting + match 3 skills\n")
    else:
        print(" - 10 min: add a small improvement to a project")
        print(" - 10 min: update README or notes")
        print(" - remaining: commit + push to GitHub\n")


SQL_PRACTICE = [
    {
        "type": "mcq",
        "q": "Which clause filters rows BEFORE aggregation?",
        "choices": ["HAVING", "WHERE", "GROUP BY", "ORDER BY"],
        "a": "WHERE",
        "why": "WHERE filters rows first; HAVING filters after GROUP BY.",
    },
    {
        "type": "mcq",
        "q": "Which join keeps all rows from the LEFT table even if no match?",
        "choices": ["INNER JOIN", "LEFT JOIN", "RIGHT JOIN", "CROSS JOIN"],
        "a": "LEFT JOIN",
        "why": "LEFT JOIN returns all left rows + matching right rows (or NULLs).",
    },
    {
        "type": "short",
        "q": "What keyword removes duplicates in SELECT results?",
        "a": "DISTINCT",
        "why": "DISTINCT eliminates duplicate rows in the result set.",
    },
    {
        "type": "short",
        "q": "Name the function used to count rows.",
        "a": "COUNT",
        "why": "COUNT(*) counts rows; COUNT(column) counts non-NULL values.",
    },
    {
        "type": "mcq",
        "q": "What does GROUP BY do?",
        "choices": [
            "Sorts rows",
            "Filters rows",
            "Aggregates rows into groups",
            "Renames columns",
        ],
        "a": "Aggregates rows into groups",
        "why": "GROUP BY groups rows so you can apply aggregates like SUM/AVG/COUNT.",
    },
]


def sql_practice():
    print("\n--- SQL Practice ---")
    print("Answer a few questions. Type 'q' anytime to stop.\n")

    score = 0
    asked = 0

    questions = SQL_PRACTICE[:]
    random.shuffle(questions)

    for item in questions:
        asked += 1
        if item["type"] == "mcq":
            print(item["q"])
            for i, c in enumerate(item["choices"], start=1):
                print(f"  {i}) {c}")
            ans = input("Your answer (1-4 or q): ").strip().lower()
            if ans == "q":
                break
            if ans in {"1", "2", "3", "4"}:
                chosen = item["choices"][int(ans) - 1]
                if chosen.strip().lower() == item["a"].strip().lower():
                    print("✅ Correct!")
                    score += 1
                else:
                    print(f"❌ Not quite. Answer: {item['a']}")
                print(f"Why: {item['why']}\n")
            else:
                print("❌ Invalid input.\n")

        else:  # short
            ans = input(f"{item['q']} (or q): ").strip()
            if ans.lower() == "q":
                break
            if ans.strip().lower() == item["a"].strip().lower():
                print("✅ Correct")
                score += 1
            else:
                print(f"❌ Not quite. Answer: {item['a']}")
            print(f"Why: {item['why']}\n")

    if asked > 0:
        pct = int(100 * score / asked)
        print(f"\n--- Quiz Results ---")
        print(f"Score: {score}/{asked} ({pct}%)\n")


def update_settings(data):
    print("\n--- Update Study Settings ---")
    goal_str = input("Daily study goal (minutes, or press Enter to keep current): ").strip()
    if goal_str:
        try:
            goal = int(goal_str)
            if goal <= 0:
                raise ValueError
            data["settings"]["daily_study_goal_minutes"] = goal
            save_data(data)
            print(f"✅ Daily goal updated to {goal} minutes.\n")
        except ValueError:
            print("❌ Invalid input.\n")
    else:
        print("(No change)\n")


def main():
    data = load_data()

    while True:
        menu()
        choice = input("Enter choice (1-7): ").strip()

        if choice == "1":
            log_study(data)
        elif choice == "2":
            today_progress(data)
        elif choice == "3":
            study_summary(data)
        elif choice == "4":
            what_to_study(data)
        elif choice == "5":
            sql_practice()
        elif choice == "6":
            update_settings(data)
        elif choice == "7":
            print("Goodbye! Keep studying. 📚\n")
            break
        else:
            print("❌ Invalid choice. Please try again.\n")


if __name__ == "__main__":
    main()
