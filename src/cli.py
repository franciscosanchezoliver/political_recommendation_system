import json


DEFAULT_QUESTIONS = [
    ("taxes", "Lower taxes or higher public spending? (low/high)"),
    ("immigration", "Stricter or more open immigration? (restrictive/open)"),
    ("climate", "Stronger or weaker climate regulation? (stronger/weaker)"),
    ("labor", "Pro-worker or pro-business? (pro-worker/pro-business)"),
]


def run_interview(questions=DEFAULT_QUESTIONS):
    profile = {}
    print("Answer the following questions (short answers accepted):\n")
    for key, q in questions:
        ans = input(f"{q} ")
        profile[key] = ans.strip()

    print("\nCollected profile:")
    print(json.dumps(profile, indent=2))
    return profile
