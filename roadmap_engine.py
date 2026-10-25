
from datetime import date, timedelta


# --------------------------------------------------
# ROADMAP TEMPLATES
# --------------------------------------------------

ROADMAP_TEMPLATES = {
    "Career": [
        {
            "title": "Assess and strengthen your foundations",
            "fraction": 0.20,
            "tasks": [
                "Identify the skills required for your target role.",
                "Assess your current skills against those requirements.",
                "Create a focused learning plan for the biggest skill gaps.",
            ],
            "deliverable": "A skills-gap assessment and learning plan.",
        },
        {
            "title": "Develop practical skills",
            "fraction": 0.30,
            "tasks": [
                "Practise the most important skills for your target role.",
                "Complete practical exercises relevant to the role.",
                "Document your progress and address weak areas.",
            ],
            "deliverable": "Evidence of practical skill development.",
        },
        {
            "title": "Build and demonstrate your abilities",
            "fraction": 0.25,
            "tasks": [
                "Build a project relevant to the target role.",
                "Test the project and document your decisions.",
                "Prepare a clear demonstration of your work.",
            ],
            "deliverable": "A documented portfolio project.",
        },
        {
            "title": "Prepare and pursue opportunities",
            "fraction": 0.25,
            "tasks": [
                "Prepare your resume and professional profile.",
                "Practise relevant interview questions.",
                "Apply to suitable opportunities and track responses.",
            ],
            "deliverable": "An application and interview preparation tracker.",
        },
    ],
    "Education": [
        {
            "title": "Define the target and requirements",
            "fraction": 0.20,
            "tasks": [
                "Identify suitable programs and institutions.",
                "Verify entry requirements and application deadlines.",
                "List the documents and tests required.",
            ],
            "deliverable": "A verified requirements checklist.",
        },
        {
            "title": "Prepare the application",
            "fraction": 0.30,
            "tasks": [
                "Prepare academic and supporting documents.",
                "Complete any required tests or prerequisites.",
                "Draft application essays and request recommendations if needed.",
            ],
            "deliverable": "A complete draft application package.",
        },
        {
            "title": "Evaluate affordability and options",
            "fraction": 0.25,
            "tasks": [
                "Estimate tuition, living costs, and other expenses.",
                "Review available funding and scholarship options.",
                "Compare programs against your priorities.",
            ],
            "deliverable": "A program comparison and funding plan.",
        },
        {
            "title": "Submit and track applications",
            "fraction": 0.25,
            "tasks": [
                "Review each application against official requirements.",
                "Submit before the applicable deadlines.",
                "Track decisions and complete any required follow-up.",
            ],
            "deliverable": "An application status tracker.",
        },
    ],
    "Startup or Business": [
        {
            "title": "Validate the problem",
            "fraction": 0.20,
            "tasks": [
                "Define the target customer and problem.",
                "Interview potential customers.",
                "Record evidence supporting or challenging the idea.",
            ],
            "deliverable": "A problem-validation summary.",
        },
        {
            "title": "Design the solution",
            "fraction": 0.25,
            "tasks": [
                "Define the minimum viable product.",
                "Prioritize essential features.",
                "Estimate initial costs and required resources.",
            ],
            "deliverable": "An MVP scope and resource estimate.",
        },
        {
            "title": "Build and test",
            "fraction": 0.30,
            "tasks": [
                "Build a testable version of the product.",
                "Test it with representative users.",
                "Record feedback and prioritize improvements.",
            ],
            "deliverable": "A tested MVP with user feedback.",
        },
        {
            "title": "Launch and measure",
            "fraction": 0.25,
            "tasks": [
                "Choose an initial customer acquisition channel.",
                "Launch to a defined initial audience.",
                "Track adoption, feedback, and costs.",
            ],
            "deliverable": "A launch report with measurable indicators.",
        },
    ],
    "Technology Project": [
        {
            "title": "Define requirements",
            "fraction": 0.15,
            "tasks": [
                "Define the problem and target users.",
                "List the essential features and acceptance criteria.",
                "Choose an appropriate technology stack.",
            ],
            "deliverable": "A scoped project specification.",
        },
        {
            "title": "Build the core functionality",
            "fraction": 0.35,
            "tasks": [
                "Implement the main user workflow.",
                "Connect the required application components.",
                "Test the core functionality with representative inputs.",
            ],
            "deliverable": "A working functional prototype.",
        },
        {
            "title": "Validate and improve",
            "fraction": 0.25,
            "tasks": [
                "Test edge cases and failure scenarios.",
                "Fix high-priority defects.",
                "Improve usability based on test results.",
            ],
            "deliverable": "A tested and improved application.",
        },
        {
            "title": "Deploy and demonstrate",
            "fraction": 0.25,
            "tasks": [
                "Prepare deployment and configuration instructions.",
                "Deploy the application to the chosen environment.",
                "Document the project and prepare a demonstration.",
            ],
            "deliverable": "A deployed, documented project.",
        },
    ],
    "Personal Development": [
        {
            "title": "Establish a baseline",
            "fraction": 0.20,
            "tasks": [
                "Define the specific behaviour or outcome to improve.",
                "Record your current baseline.",
                "Choose a realistic way to measure progress.",
            ],
            "deliverable": "A baseline and measurement method.",
        },
        {
            "title": "Build a sustainable routine",
            "fraction": 0.30,
            "tasks": [
                "Break the target behaviour into manageable actions.",
                "Schedule consistent practice.",
                "Track completion and obstacles.",
            ],
            "deliverable": "A repeatable routine and progress log.",
        },
        {
            "title": "Review and adjust",
            "fraction": 0.25,
            "tasks": [
                "Review progress against the baseline.",
                "Identify what helps or interrupts consistency.",
                "Adjust the routine using the evidence collected.",
            ],
            "deliverable": "A progress review and revised routine.",
        },
        {
            "title": "Evaluate the outcome",
            "fraction": 0.25,
            "tasks": [
                "Measure the final result against your target.",
                "Identify which methods worked best.",
                "Create a sustainable continuation plan.",
            ],
            "deliverable": "An outcome review and maintenance plan.",
        },
    ],
    "Other": [
        {
            "title": "Clarify the outcome",
            "fraction": 0.20,
            "tasks": [
                "Define what successful completion looks like.",
                "Identify the main requirements and constraints.",
                "Choose a measurable indicator of progress.",
            ],
            "deliverable": "A goal definition and success criteria.",
        },
        {
            "title": "Prepare the approach",
            "fraction": 0.25,
            "tasks": [
                "Break the goal into smaller work packages.",
                "Identify required resources and dependencies.",
                "Choose the first practical milestone.",
            ],
            "deliverable": "A structured execution plan.",
        },
        {
            "title": "Execute and review",
            "fraction": 0.30,
            "tasks": [
                "Complete the highest-priority work.",
                "Record progress and obstacles.",
                "Adjust the plan when new information emerges.",
            ],
            "deliverable": "Completed milestones and a progress record.",
        },
        {
            "title": "Evaluate completion",
            "fraction": 0.25,
            "tasks": [
                "Compare results with the original success criteria.",
                "Resolve remaining gaps.",
                "Document the outcome and remaining work.",
            ],
            "deliverable": "An outcome report and follow-up plan.",
        },
    ],
}


# --------------------------------------------------
# TIMELINE PARSING
# --------------------------------------------------

def parse_duration(text):
    """Extract a rough duration in days from common expressions."""

    text = (text or "").lower().strip()

    if not text:
        return 90

    if "flexible" in text:
        return 90

    if "week" in text:
        number = _first_number(text, 12)
        return max(1, int(number * 7))

    if "month" in text:
        number = _first_number(text, 3)
        return max(1, int(number * 30))

    if "year" in text:
        number = _first_number(text, 1)
        return max(1, int(number * 365))

    if "day" in text:
        number = _first_number(text, 30)
        return max(1, int(number))

    # A bare number is interpreted as months.
    number = _first_number(text, 3)
    return max(1, int(number * 30))


def _first_number(text, default):
    import re

    match = re.search(r"\d+(?:\.\d+)?", text)

    if match:
        return float(match.group())

    return default


# --------------------------------------------------
# ROADMAP GENERATOR
# --------------------------------------------------

def generate_roadmap(profile, followup_answers=None):
    """
    Generate a structured roadmap from a goal profile.

    profile should contain:
        goal, category, deadline, starting_point,
        available_time, resources, constraints

    followup_answers is an optional dictionary of additional answers.
    """

    followup_answers = followup_answers or {}

    category = profile.get("category", "Other")

    if category not in ROADMAP_TEMPLATES:
        category = "Other"

    duration_days = parse_duration(profile.get("deadline", ""))

    today = date.today()
    target_date = today + timedelta(days=duration_days)

    templates = ROADMAP_TEMPLATES[category]

    phases = []
    current_day = 0

    for index, template in enumerate(templates, start=1):
        phase_days = max(
            1,
            round(duration_days * template["fraction"]),
        )

        start_date = today + timedelta(days=current_day)
        end_date = today + timedelta(
            days=min(duration_days, current_day + phase_days)
        )

        phases.append({
            "phase_number": index,
            "title": template["title"],
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "tasks": template["tasks"],
            "deliverable": template["deliverable"],
            "status": "Not started",
        })

        current_day += phase_days

    return {
        "goal": profile.get("goal", ""),
        "category": category,
        "starting_point": (
            followup_answers.get("starting_point")
            or profile.get("starting_point", "")
        ),
        "available_time": (
            followup_answers.get("available_time")
            or profile.get("available_time", "")
        ),
        "resources": (
            followup_answers.get("resources")
            or profile.get("resources", "")
        ),
        "constraints": (
            followup_answers.get("constraints")
            or profile.get("constraints", "")
        ),
        "duration_days": duration_days,
        "start_date": today.isoformat(),
        "target_date": target_date.isoformat(),
        "phases": phases,
        "assumptions": [
            "The timeline is an initial estimate based on the entered deadline.",
            "Phase durations are planning allocations, not guaranteed completion times.",
            "Tasks should be adjusted to the user's skills, resources, and actual progress.",
        ],
    }
