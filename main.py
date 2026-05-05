import re
import tkinter as tk

COMMON_PASSWORDS = {
    "password", "password1", "password123", "123456", "123456789", "12345678",
    "1234567", "1234567890", "qwerty", "qwerty123", "abc123", "letmein",
    "monkey", "dragon", "master", "sunshine", "princess", "welcome", "shadow",
    "superman", "michael", "football", "baseball", "soccer", "hockey",
    "iloveyou", "trustno1", "hello", "charlie", "donald", "password!",
    "admin", "login", "pass", "test", "guest", "root", "toor", "changeme",
}

STRENGTH_COLORS = {
    "Very Weak": "#e74c3c",
    "Weak":      "#e67e22",
    "Moderate":  "#f1c40f",
    "Strong":    "#2ecc71",
    "Very Strong": "#27ae60",
}


def check_password_strength(password: str) -> dict:
    issues = []
    score = 0

    if password.lower() in COMMON_PASSWORDS:
        return {
            "score": 0,
            "max_score": 6,
            "strength": "Very Weak",
            "issues": ["This is one of the most common passwords — choose something unique"],
        }

    if len(password) >= 8:
        score += 1
    else:
        issues.append("At least 8 characters required")

    if len(password) >= 12:
        score += 1

    if re.search(r"[A-Z]", password):
        score += 1
    else:
        issues.append("Add at least one uppercase letter")

    if re.search(r"[a-z]", password):
        score += 1
    else:
        issues.append("Add at least one lowercase letter")

    if re.search(r"\d", password):
        score += 1
    else:
        issues.append("Add at least one number")

    if re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]", password):
        score += 1
    else:
        issues.append("Add at least one special character (!@#$%^&*...)")

    if score <= 2:
        strength = "Weak"
    elif score <= 4:
        strength = "Moderate"
    elif score == 5:
        strength = "Strong"
    else:
        strength = "Very Strong"

    return {"score": score, "max_score": 6, "strength": strength, "issues": issues}


class PasswordCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Checker")
        self.root.geometry("420x380")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e2e")

        self._build_ui()

    def _build_ui(self):
        bg = "#1e1e2e"
        fg = "#cdd6f4"
        entry_bg = "#313244"

        tk.Label(self.root, text="Password Checker", font=("Helvetica", 18, "bold"),
                 bg=bg, fg=fg).pack(pady=(24, 4))

        tk.Label(self.root, text="Enter a password to check its strength",
                 font=("Helvetica", 10), bg=bg, fg="#a6adc8").pack()

        entry_frame = tk.Frame(self.root, bg=bg)
        entry_frame.pack(pady=16, padx=32, fill="x")

        self.password_var = tk.StringVar()
        self.password_var.trace_add("write", self._on_change)

        self.entry = tk.Entry(
            entry_frame, textvariable=self.password_var, show="•",
            font=("Helvetica", 13), bg=entry_bg, fg=fg, insertbackground=fg,
            relief="flat", bd=8,
        )
        self.entry.pack(side="left", fill="x", expand=True)

        self.show_var = tk.BooleanVar(value=False)
        tk.Checkbutton(
            entry_frame, text="Show", variable=self.show_var,
            command=self._toggle_show, bg=bg, fg="#a6adc8",
            activebackground=bg, activeforeground=fg,
            selectcolor=entry_bg, relief="flat", font=("Helvetica", 9),
        ).pack(side="left", padx=(6, 0))

        # Strength bar (6 segments)
        bar_frame = tk.Frame(self.root, bg=bg)
        bar_frame.pack(padx=32, fill="x")

        self.segments = []
        for _ in range(6):
            seg = tk.Frame(bar_frame, height=8, bg="#313244")
            seg.pack(side="left", expand=True, fill="x", padx=2)
            self.segments.append(seg)

        self.strength_label = tk.Label(self.root, text="", font=("Helvetica", 13, "bold"),
                                       bg=bg, fg=fg)
        self.strength_label.pack(pady=(10, 2))

        self.suggestions_frame = tk.Frame(self.root, bg=bg)
        self.suggestions_frame.pack(padx=32, fill="x", pady=(4, 0))

        self.entry.focus()

    def _toggle_show(self):
        self.entry.config(show="" if self.show_var.get() else "•")

    def _on_change(self, *_):
        password = self.password_var.get()

        for widget in self.suggestions_frame.winfo_children():
            widget.destroy()

        if not password:
            for seg in self.segments:
                seg.configure(bg="#313244")
            self.strength_label.config(text="", fg="#cdd6f4")
            return

        result = check_password_strength(password)
        color = STRENGTH_COLORS[result["strength"]]

        for i, seg in enumerate(self.segments):
            seg.configure(bg=color if i < result["score"] else "#313244")

        self.strength_label.config(
            text=f"{result['strength']}  ({result['score']}/{result['max_score']})",
            fg=color,
        )

        for issue in result["issues"]:
            tk.Label(
                self.suggestions_frame, text=f"• {issue}",
                font=("Helvetica", 10), bg="#1e1e2e", fg="#f38ba8",
                anchor="w", wraplength=356, justify="left",
            ).pack(fill="x", pady=1)

        if not result["issues"]:
            tk.Label(
                self.suggestions_frame, text="Your password meets all requirements!",
                font=("Helvetica", 10), bg="#1e1e2e", fg="#a6e3a1",
                anchor="w",
            ).pack(fill="x")


def main():
    root = tk.Tk()
    PasswordCheckerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
