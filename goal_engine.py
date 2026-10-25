
import re


GOAL_KEYWORDS = {
    "Career": [
        "job", "career", "engineer", "developer",
        "employment", "interview", "promotion",
        "placement", "freelance",
    ],
    "Education": [
        "study", "university", "college", "degree",
        "master", "masters", "admission", "learn",
        "exam", "scholarship",
    ],
    "Startup or Business": [
        "startup", "business", "company", "customers",
        "revenue", "launch a product", "entrepreneur",
    ],
    "Technology Project": [
        "build an app", "build a website", "software",
        "application", "AI project", "machine learning project",
        "develop a", "create an app",
    ],
    "Personal Development": [
        "fitness", "get fit", "habit", "confidence",
        "productivity", "improve myself", "personal growth",
    ],
}


def identify_category(goal, selected_category):
    """Identify a likely goal category from user input."""

    if selected_category != "Let Guidoxis identify it":
        return selected_category

    text = goal.lower()
    scores = {}

    for category, keywords in GOAL_KEYWORDS.items():
        scores[category] = sum(
            1 for keyword in keywords if keyword in text
        )

    best_category = max(scores, key=scores.get)

    if scores[best_category] == 0:
        return "Other"

    # Avoid pretending that ambiguous goals are certain.
    highest_score = scores[best_category]
    tied = [
        category for category, score in scores.items()
        if score == highest_score
    ]

    if len(tied) > 1:
        return "Other"

    return best_category


def understand_goal(profile):
    """
    Convert the user's input into a structured goal profile.
    This function does not generate a roadmap yet.
    """

    goal = profile.get("goal", "").strip()

    category = identify_category(
        goal,
        profile.get("category", "Let Guidoxis identify it"),
    )

    deadline = profile.get("deadline", "").strip()
    current_stage = profile.get("current_stage", "")
    daily_time = profile.get("daily_time", "")
    resources = profile.get("resources", "").strip()
    constraints = profile.get("constraints", "").strip()

    missing_information = []

    if not deadline:
        missing_information.append("deadline")

    if (
        not current_stage
        or current_stage == "Help me identify my starting point"
    ):
        missing_information.append("starting point")

    if not resources:
        missing_information.append("available resources")

    if not constraints:
        missing_information.append("constraints or obstacles")

    if not daily_time or daily_time == "Not decided":
        missing_information.append("available time")

    # Select only the questions that are currently relevant.
    follow_up_questions = []

    if "starting point" in missing_information:
        follow_up_questions.append({
            "key": "starting_point",
            "question": "What best describes your current situation?",
            "options": [
                "Complete beginner",
                "Know the basics",
                "Have some experience",
                "Already making progress",
            ],
        })

    if "deadline" in missing_information:
        follow_up_questions.append({
            "key": "deadline",
            "question": "When do you want to achieve this goal?",
            "options": [
                "Within 1 month",
                "Within 3 months",
                "Within 6 months",
                "Within 1 year",
                "Flexible timeline",
            ],
        })

    if "available time" in missing_information:
        follow_up_questions.append({
            "key": "available_time",
            "question": "How much time can you realistically commit?",
            "options": [
                "Less than 1 hour daily",
                "1–2 hours daily",
                "2–4 hours daily",
                "More than 4 hours daily",
            ],
        })

    if "available resources" in missing_information:
        follow_up_questions.append({
            "key": "resources",
            "question": "What resources do you already have?",
            "options": [
                "Basic tools and a laptop",
                "Relevant skills or experience",
                "Budget or financial support",
                "A team or mentor",
                "None of these yet",
            ],
        })

    if "constraints or obstacles" in missing_information:
        follow_up_questions.append({
            "key": "constraints",
            "question": "What is your biggest limitation right now?",
            "options": [
                "Limited time",
                "Limited budget",
                "Lack of skills or experience",
                "Lack of guidance",
                "I am not sure yet",
            ],
        })

    return {
        "goal": goal,
        "category": category,
        "deadline": deadline,
        "starting_point": current_stage,
        "available_time": daily_time,
        "resources": resources,
        "constraints": constraints,
        "missing_information": missing_information,
        "follow_up_questions": follow_up_questions,
    }
