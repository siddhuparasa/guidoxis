
import json
from datetime import date, timedelta
from io import BytesIO
from xml.sax.saxutils import escape

import streamlit as st
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    KeepTogether,
)
from research_engine import generate_researched_roadmap

st.set_page_config(
    page_title="Guidoxis",
    page_icon="🧭",
    layout="wide"
)


st.markdown(
    """
    <style>
    /* ===== MIDNIGHT FOREST THEME ===== */

    .stApp {
        background: #111A15;
        color: #F2F0E6;
    }

    .block-container {
        max-width: 1100px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    #MainMenu,
    footer {
        visibility: hidden;
    }

    header[data-testid="stHeader"] {
        background: transparent;
    }

    /* ===== HERO CONTAINER ===== */

    .hero {
        box-sizing: border-box;
        width: 100%;
        padding: 30px 32px;
        margin: 0 0 30px 0;
        text-align: left;
        background: linear-gradient(135deg, #19271F, #142019);
        border: 1px solid rgba(197, 224, 165, 0.16);
        border-radius: 16px;
    }

    /* ===== GUIDOXIS BRAND ===== */

    .Guidoxis-heading {
        color: #F2F0E6;
        font-family: sans-serif;
        font-size: 50px;
        font-weight: 750;
        letter-spacing: -1.2px;
        line-height: 1.2;
        text-align: left;
        margin: 0 0 28px 0;
        padding: 0;
    }

    .Guidoxis-heading span {
        color: #C5E0A5;
    }

    .Guidoxis-brand {
    display: flex;
    align-items: center;
    gap: 10px;
}

.Guidoxis-symbol {
    font-size: 50px;
    line-height: 1;
}

    /* ===== EYEBROW TEXT ===== */

    .hero-eyebrow {
        color: #C5E0A5;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        text-align: left;
        margin-bottom: 14px;
    }

    /* ===== MAIN HEADING ===== */

    .hero-title {
        color: #F2F0E6;
        font-family: sans-serif;
        font-size: clamp(32px, 4vw, 46px);
        font-weight: 750;
        line-height: 1.2;
        letter-spacing: -1.5px;
        text-align: left;
        margin: 0 0 16px 0;
    }

    .hero-title span {
        color: #C5E0A5;
    }

    /* ===== DESCRIPTION ===== */

    .hero-description {
        max-width: 700px;
        color: #C3CCC4;
        font-size: 20px;
        font-weight: 400;
        line-height: 1.85;
        text-align: left;
        margin: 0;
    }

    /* ===== FORM SECTION SPACING ===== */

    div[data-testid="stForm"] {
        border-color: rgba(197, 224, 165, 0.20);
        border-radius: 12px;
    }

    /* ===== MOBILE RESPONSIVENESS ===== */

    @media (max-width: 640px) {
        .block-container {
            padding: 1rem 1rem 2rem 1rem;
        }

        .hero {
            padding: 24px 20px;
            border-radius: 12px;
        }

        .Guidoxis-heading {
            font-size: 50px;
            margin-bottom: 24px;
        }

        .hero-title {
            font-size: 35px;
            letter-spacing: -0.8px;
        }

        .hero-description {
            font-size: 18px;
            line-height: 1.8;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)



# ===== GUIDOXIS HERO SECTION =====

st.markdown(
    """
   <div class="Guidoxis-brand">
    <span class="Guidoxis-symbol">🧭</span>
    <span class="Guidoxis-heading">Guidoxis<span>.</span></span>
   </div>
        <div class="hero-eyebrow">
            YOUR NEXT CHAPTER STARTS HERE
        </div>
        <div class="hero-title">
            Find your direction.<br>
            <span>Build your path.</span>
        </div>
        <div class="hero-description">
            Turn your ambitions into a practical, personalized roadmap
            with clear steps, useful resources, and milestones that fit
            your time, experience, and budget.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)



if "roadmap" not in st.session_state:
    st.session_state.roadmap = None


def create_roadmap_pdf(roadmap):
    """Convert the generated roadmap dictionary into a downloadable PDF."""

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=0.65 * inch,
        leftMargin=0.65 * inch,
        topMargin=0.65 * inch,
        bottomMargin=0.65 * inch,
        title="Guidoxis Personalized Roadmap",
        author="Guidoxis",
    )

    styles = getSampleStyleSheet()

    styles.add(
        ParagraphStyle(
            name="RoadmapTitle",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=22,
            leading=28,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#3730A3"),
            spaceAfter=10,
        )
    )

    styles.add(
        ParagraphStyle(
            name="RoadmapSubtitle",
            parent=styles["Normal"],
            fontSize=10,
            leading=15,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#555555"),
            spaceAfter=18,
        )
    )

    styles.add(
        ParagraphStyle(
            name="SectionHeading",
            parent=styles["Heading2"],
            fontSize=14,
            leading=18,
            textColor=colors.HexColor("#3730A3"),
            spaceBefore=12,
            spaceAfter=6,
            keepWithNext=True,
        )
    )

    styles.add(
        ParagraphStyle(
            name="PhaseHeading",
            parent=styles["Heading1"],
            fontSize=16,
            leading=21,
            textColor=colors.HexColor("#1D4ED8"),
            spaceBefore=14,
            spaceAfter=8,
            keepWithNext=True,
        )
    )

    styles.add(
        ParagraphStyle(
            name="RoadmapBody",
            parent=styles["BodyText"],
            fontSize=9.5,
            leading=14,
            spaceAfter=5,
            wordWrap="LTR",
        )
    )

    styles.add(
        ParagraphStyle(
            name="RoadmapBullet",
            parent=styles["BodyText"],
            fontSize=9.5,
            leading=14,
            leftIndent=14,
            firstLineIndent=-9,
            spaceAfter=4,
            wordWrap="LTR",
        )
    )

    story = []

    def add_paragraph(value, style="RoadmapBody"):
        """Add escaped text to the PDF safely."""
        if value is None:
            return

        if isinstance(value, (dict, list)):
            value = json.dumps(
                value,
                ensure_ascii=False,
                default=str,
            )

        value = str(value).strip()

        if value:
            story.append(
                Paragraph(escape(value), styles[style])
            )

    def add_bullet(value):
        """Add a bullet point."""
        if isinstance(value, dict):
            value = json.dumps(
                value,
                ensure_ascii=False,
                default=str,
            )

        add_paragraph(f"• {value}", "RoadmapBullet")

    def add_list(items, empty_text="None specified."):
        if not items:
            add_paragraph(empty_text)
            return

        for item in items:
            if isinstance(item, dict):
                label = (
                    item.get("name")
                    or item.get("skill")
                    or item.get("title")
                    or item.get("task")
                    or item.get("phase")
                    or "Item"
                )
                add_bullet(label)

                for key in ("purpose", "importance", "description"):
                    if item.get(key):
                        add_paragraph(f"  {key.title()}: {item[key]}")
            else:
                add_bullet(item)

    # PDF title
    story.append(
        Paragraph("Guidoxis", styles["RoadmapTitle"])
    )
    story.append(
        Paragraph(
            "Your Personalized Roadmap",
            styles["RoadmapSubtitle"],
        )
    )

    # Goal and overview
    story.append(
        Paragraph("Roadmap Overview", styles["SectionHeading"])
    )

    add_paragraph(
        f"Goal: {roadmap.get('goal', 'Not specified')}"
    )
    add_paragraph(
        f"Total duration: "
        f"{roadmap.get('total_duration', 'Not specified')}"
    )

    if roadmap.get("generated_on"):
        add_paragraph(
            f"Generated on: {roadmap['generated_on']}"
        )

    if roadmap.get("fallback_reason"):
        add_paragraph(
            f"Note: {roadmap['fallback_reason']}"
        )

    phases = roadmap.get("phases", [])

    for index, phase in enumerate(phases, start=1):
        story.append(Spacer(1, 8))

        phase_number = phase.get("phase", index)
        phase_title = phase.get("title", f"Phase {index}")
        phase_duration = phase.get(
            "duration",
            "Duration not specified",
        )

        story.append(
            Paragraph(
                escape(
                    f"Phase {phase_number}: "
                    f"{phase_title} ({phase_duration})"
                ),
                styles["PhaseHeading"],
            )
        )

        # Objective
        story.append(
            Paragraph("Objective", styles["SectionHeading"])
        )
        add_paragraph(
            phase.get("objective", "Not specified.")
        )

        # Prerequisites
        story.append(
            Paragraph("Prerequisites", styles["SectionHeading"])
        )
        add_list(phase.get("prerequisites", []))

        # Skills
        story.append(
            Paragraph("Skills to Learn", styles["SectionHeading"])
        )

        skills = phase.get("skills_to_learn", [])

        if not skills:
            add_paragraph("No skills specified.")

        for skill in skills:
            if isinstance(skill, dict):
                add_paragraph(
                    skill.get("skill", "Skill"),
                    "RoadmapBody",
                )

                if skill.get("importance"):
                    add_paragraph(
                        f"Importance: {skill['importance']}"
                    )

                if skill.get("topics"):
                    add_paragraph("Topics:")
                    add_list(skill["topics"])

                if skill.get("mastery_check"):
                    add_paragraph(
                        f"Mastery check: {skill['mastery_check']}"
                    )
            else:
                add_bullet(skill)

        # Tools and technologies
        story.append(
            Paragraph(
                "Tools and Technologies",
                styles["SectionHeading"],
            )
        )

        tools = phase.get("tools_and_technologies", [])

        if not tools:
            add_paragraph("No tools specified.")

        for tool in tools:
            if isinstance(tool, dict):
                add_paragraph(
                    tool.get("name", "Tool"),
                    "RoadmapBody",
                )

                if tool.get("purpose"):
                    add_paragraph(
                        f"Purpose: {tool['purpose']}"
                    )

                if tool.get("cost"):
                    add_paragraph(f"Cost: {tool['cost']}")
            else:
                add_bullet(tool)

        # Learning resources
        story.append(
            Paragraph(
                "Learning Resources",
                styles["SectionHeading"],
            )
        )

        resources = phase.get("learning_resources", [])

        if not resources:
            add_paragraph("No resources specified.")

        for resource in resources:
            if isinstance(resource, dict):
                add_paragraph(
                    resource.get("title", "Learning resource")
                )

                url = str(resource.get("url", "")).strip()

                if url.startswith(("https://", "http://")):
                    # Escape the URL before placing it in a link.
                    safe_url = escape(url, {'"': "&quot;"})
                    story.append(
                        Paragraph(
                            f'<link href="{safe_url}" '
                            f'color="#2563EB">{escape(url)}</link>',
                            styles["RoadmapBody"],
                        )
                    )

                if resource.get("type"):
                    add_paragraph(
                        f"Type: {resource['type']}"
                    )

                if resource.get("purpose"):
                    add_paragraph(
                        f"Purpose: {resource['purpose']}"
                    )
            else:
                add_bullet(resource)

        # Tasks
        story.append(
            Paragraph("Tasks", styles["SectionHeading"])
        )

        tasks = phase.get("tasks", [])

        if not tasks:
            add_paragraph("No tasks specified.")

        total_hours = 0.0

        for task_index, task in enumerate(tasks, start=1):
            if not isinstance(task, dict):
                add_bullet(task)
                continue

            task_name = task.get(
                "task",
                f"Task {task_index}",
            )

            task_content = [
                Paragraph(
                    escape(f"{task_index}. {task_name}"),
                    styles["Heading3"],
                )
            ]

            hours = task.get("estimated_hours")

            if hours is not None:
                task_content.append(
                    Paragraph(
                        escape(f"Estimated time: {hours} hours"),
                        styles["RoadmapBody"],
                    )
                )

                try:
                    total_hours += float(hours or 0)
                except (TypeError, ValueError):
                    pass

            story.append(KeepTogether(task_content))

            if task.get("instructions"):
                add_paragraph("Steps:")
                add_list(task["instructions"])

            if task.get("deliverable"):
                add_paragraph(
                    f"Deliverable: {task['deliverable']}"
                )

            if task.get("completion_criteria"):
                add_paragraph("Completion criteria:")
                add_list(task["completion_criteria"])

        if total_hours:
            add_paragraph(
                f"Estimated task time for this phase: "
                f"{total_hours:g} hours"
            )

        # Milestone
        story.append(
            Paragraph("Milestone", styles["SectionHeading"])
        )
        add_paragraph(
            phase.get("milestone", "Not specified.")
        )

    def add_page_number(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.HexColor("#666666"))
        canvas.drawCentredString(
            A4[0] / 2,
            0.35 * inch,
            f"Guidoxis | Page {doc.page}",
        )
        canvas.restoreState()

    document.build(
        story,
        onFirstPage=add_page_number,
        onLaterPages=add_page_number,
    )

    buffer.seek(0)
    return buffer.getvalue()


with st.form("roadmap_form"):
    st.header("Define your goal")

    goal = st.text_area(
        "What do you want to achieve?",
        placeholder=(
            "Example: Build and deploy an AI-powered document "
            "QA app using RAG within 8 weeks."
        ),
        height=95,
    )

    left, right = st.columns(2)

    with left:
        category = st.selectbox(
            "Goal category",
            [
                "Technology Project",
                "AI / Machine Learning",
                "Software Development",
                "Career Preparation",
                "Data Science / Analytics",
                "Business / Entrepreneurship",
                "Academic Learning",
                "Personal Development",
                "Other",
            ],
        )

        starting_stage = st.selectbox(
            "Your current level",
            [
                "Complete beginner",
                "Beginner",
                "Intermediate",
                "Advanced",
            ],
        )

        target_date = st.date_input(
            "Target completion date",
            value=date.today() + timedelta(days=56),
            min_value=date.today(),
        )

        daily_hours = st.slider(
            "Available hours per day",
            min_value=1,
            max_value=12,
            value=2,
        )

    with right:
        budget = st.selectbox(
            "Available budget",
            [
                "Free only",
                "Low budget",
                "Moderate budget",
                "Flexible budget",
            ],
        )

        learning_style = st.selectbox(
            "Preferred learning style",
            [
                "Hands-on projects first",
                "Theory followed by practice",
                "Video courses",
                "Documentation and reading",
                "Structured exercises",
            ],
        )

        existing_resources = st.text_area(
            "Skills, tools, and resources you already have",
            placeholder=(
                "Example: Python basics, Git, laptop, Streamlit..."
            ),
            height=90,
        )

        constraints = st.text_area(
            "Challenges or limitations",
            placeholder=(
                "Example: Weak in advanced Python, free tools only..."
            ),
            height=90,
        )

    followup_text = st.text_area(
        "Additional requirements (optional)",
        placeholder=(
            "Example: Include GitHub portfolio, interview preparation, "
            "or deployment."
        ),
        height=70,
    )

    submitted = st.form_submit_button(
        "Generate My Roadmap",
        type="primary",
        use_container_width=True,
    )


if submitted:
    if not goal.strip():
        st.error("Please describe your goal.")

    elif target_date < date.today():
        st.error("Choose a target date that is today or later.")

    else:
        profile = {
            "goal": goal.strip(),
            "category": category,
            "starting_stage": starting_stage,
            "target_date": target_date.isoformat(),
            "daily_hours": daily_hours,
            "budget": budget,
            "learning_style": learning_style,
            "existing_resources": existing_resources.strip(),
            "constraints": constraints.strip(),
        }

        followup_answers = {
            "additional_requirements": followup_text.strip(),
        }

        st.session_state.roadmap = None

        try:
            with st.spinner(
                "Building your personalized roadmap..."
            ):
                roadmap = generate_researched_roadmap(
                    profile,
                    followup_answers=followup_answers,
                    use_cache=False,
                )

            st.session_state.roadmap = roadmap
            st.success("Your roadmap is ready!")

        except Exception as exc:
            st.error("Could not generate the roadmap.")

            with st.expander("View technical error"):
                st.code(str(exc))

            st.info(
                "A provider may be temporarily unavailable or out of "
                "quota. Wait briefly and try again. Check your API "
                "keys if the problem persists."
            )


def show_list(items, empty_text="No items provided."):
    """Display a simple list of strings or dictionaries."""
    if not items:
        st.caption(empty_text)
        return

    for item in items:
        if isinstance(item, dict):
            label = (
                item.get("name")
                or item.get("skill")
                or item.get("title")
                or "Item"
            )
            st.markdown(f"- **{label}**")
        else:
            st.markdown(f"- {item}")


def show_phase(phase, index):
    """Render one roadmap phase."""
    phase_number = phase.get("phase", index)
    title = phase.get("title", f"Phase {index}")
    duration = phase.get(
        "duration",
        "Duration not specified",
    )

    with st.expander(
        f"Phase {phase_number}: {title} · {duration}",
        expanded=(index == 1),
    ):
        st.markdown("**Objective**")
        st.write(phase.get("objective", "Not specified."))

        st.markdown("### Prerequisites")
        show_list(phase.get("prerequisites", []))

        st.markdown("### Skills to learn")
        skills = phase.get("skills_to_learn", [])

        if not skills:
            st.caption("No skills specified.")

        for skill in skills:
            if isinstance(skill, dict):
                st.markdown(
                    f"**{skill.get('skill', 'Skill')}**"
                )

                if skill.get("importance"):
                    st.write(skill["importance"])

                if skill.get("topics"):
                    st.caption("Topics")
                    show_list(skill["topics"])

                if skill.get("mastery_check"):
                    st.markdown(
                        "**Mastery check:** "
                        f"{skill['mastery_check']}"
                    )
            else:
                st.markdown(f"- {skill}")

        st.markdown("### Tools and technologies")
        tools = phase.get("tools_and_technologies", [])

        if not tools:
            st.caption("No tools specified.")

        for tool in tools:
            if isinstance(tool, dict):
                st.markdown(
                    f"**{tool.get('name', 'Tool')}**"
                )

                if tool.get("purpose"):
                    st.write(tool["purpose"])

                if tool.get("cost"):
                    st.caption(f"Cost: {tool['cost']}")
            else:
                st.markdown(f"- {tool}")

        st.markdown("### Learning resources")
        resources = phase.get("learning_resources", [])

        if not resources:
            st.caption("No resources specified.")

        for resource in resources:
            if isinstance(resource, dict):
                resource_title = resource.get(
                    "title",
                    "Learning resource",
                )
                url = resource.get("url", "")

                if url.startswith(("https://", "http://")):
                    st.markdown(
                        f"- [{resource_title}]({url})"
                    )
                else:
                    st.markdown(f"- **{resource_title}**")

                if resource.get("type"):
                    st.caption(resource["type"])

                if resource.get("purpose"):
                    st.write(resource["purpose"])
            else:
                st.markdown(f"- {resource}")

        st.markdown("### Tasks")
        tasks = phase.get("tasks", [])

        if not tasks:
            st.caption("No tasks specified.")

        total_hours = 0.0

        for task_index, task in enumerate(tasks, start=1):
            if not isinstance(task, dict):
                st.markdown(f"- {task}")
                continue

            task_name = task.get(
                "task",
                f"Task {task_index}",
            )
            hours = task.get("estimated_hours")

            try:
                total_hours += float(hours or 0)
            except (TypeError, ValueError):
                pass

            with st.container(border=True):
                st.markdown(
                    f"**{task_index}. {task_name}**"
                )

                if hours is not None:
                    st.caption(
                        f"Estimated time: {hours} hours"
                    )

                if task.get("instructions"):
                    st.markdown("**Steps**")
                    show_list(task["instructions"])

                if task.get("deliverable"):
                    st.markdown("**Deliverable**")
                    st.write(task["deliverable"])

                if task.get("completion_criteria"):
                    st.markdown("**Completion criteria**")
                    show_list(task["completion_criteria"])

        if total_hours:
            st.caption(
                f"Estimated task time for this phase: "
                f"{total_hours:g} hours"
            )

        st.markdown("### Milestone")
        st.write(
            phase.get("milestone", "Not specified.")
        )


roadmap = st.session_state.roadmap

if roadmap:
    st.divider()
    st.header("Your personalized roadmap")

    st.markdown(
        f"**Goal:** {roadmap.get('goal', 'Not specified')}"
    )

    col1, col2, col3 = st.columns(3)
    phases = roadmap.get("phases", [])

    col1.metric("Total phases", len(phases))
    col2.metric(
        "Total duration",
        roadmap.get("total_duration", "Not specified"),
    )

    if roadmap.get("fallback_reason"):
        st.caption(roadmap["fallback_reason"])

    if roadmap.get("generated_on"):
        st.caption(
            f"Generated on: {roadmap['generated_on']}"
        )

    for index, phase in enumerate(phases, start=1):
        show_phase(phase, index)

    # Download the roadmap as PDF instead of JSON.
    try:
        pdf_data = create_roadmap_pdf(roadmap)

        st.download_button(
            label="Download Roadmap (PDF)",
            data=pdf_data,
            file_name="guidoxis_roadmap.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

    except Exception as exc:
        st.error("Could not create the roadmap PDF.")

        with st.expander("View PDF error"):
            st.code(str(exc))

    if st.button(
        "Clear Roadmap and Start Again",
        use_container_width=True,
    ):
        st.session_state.roadmap = None
        st.rerun()


st.divider()
st.caption(
    "Guidoxis · AI-generated plans should be reviewed and "
    "adapted to your progress."
)
