import re


def check_password_strength(password: str) -> dict:
    issues = []
    score = 0

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


def main():
    print("=== Password Strength Checker ===\n")

    while True:
        password = input("Enter a password to check (or 'q' to quit): ")

        if password.lower() == "q":
            print("Goodbye!")
            break

        if not password:
            print("Please enter a password.\n")
            continue

        result = check_password_strength(password)

        print(f"\nStrength : {result['strength']} ({result['score']}/{result['max_score']})")

        if result["issues"]:
            print("Suggestions:")
            for issue in result["issues"]:
                print(f"  - {issue}")
        else:
            print("Your password meets all requirements!")

        print()


if __name__ == "__main__":
    main()
