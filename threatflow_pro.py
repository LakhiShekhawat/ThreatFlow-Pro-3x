import tkinter as tk
from tkinter import messagebox, ttk
import json
import random

# ------------------ LOAD SCENARIOS ------------------
with open("scenarios.json") as f:
    scenarios = json.load(f)

# Randomize scenario order
random.shuffle(scenarios)

# ------------------ APP CLASS ------------------
class ThreatFlowPro3x:
    def __init__(self, root):
        self.root = root
        self.root.title("ThreatFlow Pro 3x – Cyber Incident Response Simulator")
        self.root.geometry("850x600")
        self.root.configure(bg="#0f172a")

        # Difficulty settings
        self.difficulty = None  # Will be set by user
        self.timer_seconds = 30

        self.score = 0
        self.current = 0
        self.total = len(scenarios)
        self.logs = []
        self.total_possible = sum(max(opt["score"] for opt in s["options"]) for s in scenarios)

        self.create_dashboard()

    # ------------------ DASHBOARD ------------------
    def create_dashboard(self):
        self.clear_screen()

        tk.Label(self.root, text="ThreatFlow Pro 3x",
                 font=("Consolas", 30, "bold"),
                 fg="#38bdf8", bg="#0f172a").pack(pady=20)

        tk.Label(self.root,
                 text="Advanced Cyber Incident Response Simulation",
                 font=("Arial", 13),
                 fg="#cbd5f5", bg="#0f172a").pack(pady=10)

        tk.Label(self.root, text="Select Difficulty",
                 font=("Arial", 12, "bold"),
                 fg="#facc15", bg="#0f172a").pack(pady=10)

        frame = tk.Frame(self.root, bg="#0f172a")
        frame.pack(pady=10)

        tk.Button(frame, text="Beginner", width=15, command=lambda: self.start_sim("Beginner")).grid(row=0, column=0, padx=10)
        tk.Button(frame, text="Intermediate", width=15, command=lambda: self.start_sim("Intermediate")).grid(row=0, column=1, padx=10)
        tk.Button(frame, text="Advanced", width=15, command=lambda: self.start_sim("Advanced")).grid(row=0, column=2, padx=10)

    def start_sim(self, level):
        self.difficulty = level
        if level == "Beginner":
            self.timer_seconds = 40
        elif level == "Intermediate":
            self.timer_seconds = 25
        else:
            self.timer_seconds = 15
        self.load_scenario()

    # ------------------ SCENARIO SCREEN ------------------
    def load_scenario(self):
        self.clear_screen()
        self.time_left = self.timer_seconds

        self.scenario = scenarios[self.current]

        # Incident Counter
        tk.Label(self.root,
                 text=f"Incident {self.current + 1} / {self.total}",
                 font=("Arial", 12, "bold"),
                 fg="#22c55e", bg="#0f172a").pack(pady=5)

        # Progress Bar
        self.progress = ttk.Progressbar(self.root, length=600, maximum=self.total)
        self.progress.pack(pady=5)
        self.progress["value"] = self.current + 1

        # Severity Alert
        tk.Label(self.root,
                 text=f"ALERT (Severity: {self.scenario['severity']})",
                 font=("Arial", 14, "bold"),
                 fg="#ef4444" if self.scenario["severity"]=="HIGH" else "#f97316" if self.scenario["severity"]=="MEDIUM" else "#38bdf8",
                 bg="#0f172a").pack(pady=10)

        # Alert Message
        tk.Label(self.root,
                 text=self.scenario["alert"],
                 font=("Arial", 12),
                 fg="white", bg="#0f172a",
                 wraplength=750, justify="left").pack(pady=15)

        # Randomize options
        options = self.scenario["options"].copy()
        random.shuffle(options)

        for option in options:
            tk.Button(self.root,
                      text=option["text"],
                      font=("Arial", 11),
                      bg="#1e293b", fg="white",
                      width=80,
                      command=lambda opt=option: self.process_choice(opt)).pack(pady=5)

        # Timer Label
        self.timer_label = tk.Label(self.root, text=f"Time left: {self.time_left}s", font=("Arial", 12), fg="#fbbf24", bg="#0f172a")
        self.timer_label.pack(pady=5)
        self.countdown()

        # Logs Panel
        self.log_panel = tk.Text(self.root, height=8, width=100, bg="#1e293b", fg="white")
        self.log_panel.pack(pady=10)
        self.update_logs("Simulation started.\n")

    # ------------------ TIMER ------------------
    def countdown(self):
        if self.time_left > 0:
            self.timer_label.config(text=f"Time left: {self.time_left}s")
            self.time_left -= 1
            self.root.after(1000, self.countdown)
        else:
            # Penalty if time runs out
            self.logs.append(f"Incident {self.current+1}: Timeout → Penalty -10")
            messagebox.showwarning("Time Up!", "You ran out of time! -10 points penalty applied.")
            self.score -= 10
            self.current += 1
            if self.current < self.total:
                self.load_scenario()
            else:
                self.show_report()

    # ------------------ PROCESS CHOICE ------------------
    def process_choice(self, option):
        self.score += option["score"]
        self.logs.append(f"Incident {self.current+1}: {option['text']} → Score {option['score']}")
        messagebox.showinfo("Decision Outcome", option["explanation"])
        self.current += 1
        if self.current < self.total:
            self.load_scenario()
        else:
            self.show_report()

    # ------------------ UPDATE LOG PANEL ------------------
    def update_logs(self, message):
        self.log_panel.insert(tk.END, message)
        self.log_panel.see(tk.END)

    # ------------------ FINAL REPORT ------------------
    def show_report(self):
        self.clear_screen()

        tk.Label(self.root,
                 text="Simulation Complete",
                 font=("Arial", 24, "bold"),
                 fg="#22c55e", bg="#0f172a").pack(pady=20)

        tk.Label(self.root,
                 text=f"Final Security Score: {self.score} / {self.total_possible}",
                 font=("Arial", 14), fg="white", bg="#0f172a").pack(pady=10)

        performance = "Excellent Analyst" if self.score >= 70 else "Good Analyst" if self.score >= 40 else "Needs Improvement"
        tk.Label(self.root,
                 text=f"Performance Level: {performance}",
                 font=("Arial", 14), fg="#38bdf8", bg="#0f172a").pack(pady=10)

        # Display decision logs
        log_text = "\n".join(self.logs)
        tk.Label(self.root, text="Incident Logs:", font=("Arial", 12, "bold"), fg="#facc15", bg="#0f172a").pack(pady=5)
        log_panel = tk.Text(self.root, height=10, width=100, bg="#1e293b", fg="white")
        log_panel.pack(pady=5)
        log_panel.insert(tk.END, log_text)
        log_panel.config(state="disabled")

        tk.Button(self.root, text="Exit",
                  font=("Arial", 12),
                  bg="#ef4444", fg="white",
                  width=15, command=self.root.quit).pack(pady=20)

    # ------------------ UTILITY ------------------
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# ------------------ RUN APP ------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = ThreatFlowPro3x(root)
    root.mainloop()
