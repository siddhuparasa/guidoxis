
import json
import random
import time
from datetime import date

import streamlit as st
from groq import Groq
from google import genai
from google.genai import types


GROQ_MODEL = "openai/gpt-oss-20b"
GEMINI_MODEL = "gemini-2.5-flash"


ROADMAP_SCHEMA = {
    "goal": "Specific goal",
    "total_duration": "Realistic duration",
    "phases": [
        {
            "phase": 1,
            "title": "Phase title",
            "duration": "Week or date range",
            "objective": "Measurable objective",
            "prerequisites": ["Prerequisite"],
            "skills_to_learn": [
                {
                    "skill": "Skill name",
                    "importance": "Brief reason",
                    "topics": ["Important topic"],
                    "mastery_check": "Practical verification",
                }
            ],
            "tools_and_technologies": [
                {
                    "name": "Tool",
                    "purpose": "Brief purpose",
                    "cost": "Free or verify",
                }
            ],
            "learning_resources": [
                {
                    "title": "Resource title",
                    "url": "Direct URL",
                    "type": "Official docs or course",
                    "purpose": "What to learn",
                }
            ],
            "tasks": [
                {
                    "task": "Specific action",
                    "instructions": ["Concrete step"],
                    "estimated_hours": 2,
                    "deliverable": "Tangible output",
                    "completion_criteria": ["Testable result"],
                }
            ],
            "milestone": "Measurable outcome",
        }
    ],
}


def _extract_roadmap(text):
    """Parse and validate the roadmap JSON."""
    if not text or not text.strip():
        raise ValueError("The model returned an empty response.")

    cleaned = text.strip()

    if cleaned.startswith("```"):
        lines = cleaned.splitlines()

        if lines and lines[0].startswith("```"):
            lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        cleaned = "\n".join(lines).strip()

    start = cleaned.find("{")
    end = cleaned.rfind("}")

    if start < 0 or end <= start:
        raise ValueError(
            "The model did not return a complete JSON object."
        )

    try:
        roadmap = json.loads(cleaned[start:end + 1])
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Malformed JSON near line {exc.lineno}, "
            f"column {exc.colno}: {exc.msg}"
        ) from exc

    if not isinstance(roadmap, dict):
        raise ValueError("The roadmap must be a JSON object.")

    phases = roadmap.get("phases")

    if not isinstance(phases, list) or not phases:
        raise ValueError("The roadmap contains no valid phases.")

    for index, phase in enumerate(phases, start=1):
        if not isinstance(phase, dict) or not phase.get("title"):
            raise ValueError(
                f"Phase {index} is missing its title."
            )

        phase.setdefault("phase", index)
        phase.setdefault("prerequisites", [])
        phase.setdefault("skills_to_learn", [])
        phase.setdefault("tools_and_technologies", [])
        phase.setdefault("learning_resources", [])
        phase.setdefault("tasks", [])
        phase.setdefault(
            "milestone",
            "Complete the phase deliverables.",
        )

    roadmap.setdefault("goal", "Personalized roadmap")
    roadmap.setdefault("total_duration", "Not specified")
    roadmap["generated_on"] = date.today().isoformat()

    return roadmap


def _build_prompt(profile, followup_answers):
    """Build a compact prompt for medium-detail roadmaps."""
    return f"""
You are Guidoxis, a practical roadmap planner.

TODAY:
{date.today().isoformat()}

USER PROFILE:
{json.dumps(profile, ensure_ascii=False, default=str)}

ADDITIONAL ANSWERS:
{json.dumps(followup_answers or {}, ensure_ascii=False, default=str)}


ROADMAP REQUIREMENTS:
- Create a personalized roadmap directly related to the user's actual goal.
- Support goals from any domain, including education, career development,
  business, entrepreneurship, finance education, creative arts, hobbies,
  fitness, personal development, communication, and technology.
- Do not assume the goal is technical, software-related, or IT-related.
- Do not automatically include programming, coding, software tools,
  testing, APIs, deployment, or technical projects.
- Include a topic, activity, tool, resource, or assessment only when it
  is relevant to the specific goal.
- Generate 4-5 meaningful phases, adjusting the number when the goal
  genuinely requires a different structure.
- Use medium-level detail: clear, organized, practical, and concise.
- Include 2-4 relevant skills, abilities, knowledge areas, or competencies
  per phase, depending on the goal.
- For each skill or competency, explain its importance briefly, list
  2-3 relevant topics or subskills, and provide a suitable mastery check.
- Include prerequisites only when genuinely necessary.
- Recommend 1-3 relevant tools, materials, methods, or resources per phase
  when useful. These may include books, equipment, software, exercises,
  practice methods, professional services, or other domain-specific aids.
- Include 1-2 reliable learning resources per phase where appropriate.
- Prefer reputable, authoritative, affordable, and accessible resources.
- Respect the user's budget, location when relevant, available resources,
  preferences, and constraints.
- Never invent URLs, prices, qualifications, or resource details.
- Include 2-3 practical activities or tasks per phase.
- Each task must have 1-2 clear instructions, a numeric estimated_hours,
  one tangible or observable deliverable, and 1-2 suitable completion
  criteria.
- Define deliverables appropriately for the goal. Examples include an
  essay, completed practice set, business plan, portfolio piece, practice
  performance, study notes, personal routine, or completed project.
- Choose completion criteria appropriate to the domain. These may include
  accuracy, consistency, demonstrated ability, quality, measurable
  progress, feedback, or successful completion of an activity.
- Give every phase a clear objective, realistic duration, relevant
  prerequisites, and a measurable milestone.
- Adapt the roadmap to the user's starting level, target date, available
  time, budget, existing knowledge, and personal limitations.
- Sequence phases logically from foundations to practice, improvement,
  and the intended outcome, where appropriate.
- Estimate realistic hours and ensure the plan fits the available time.
- Include evaluation, feedback, practice, implementation, or maintenance
  only when relevant to the goal.
- For health, fitness, financial, or other sensitive goals, keep advice
  appropriate to the domain and avoid unsafe or unsupported claims.
- Avoid unnecessary theory, repetitive tasks, irrelevant tools, and
  excessive detail.
- Do not guarantee results.
- Make every recommendation specific to the user's goal rather than
  forcing all goals into the same template.
- Return a complete JSON object matching the provided schema.
- Return valid JSON only, without Markdown fences or additional prose.
{json.dumps(ROADMAP_SCHEMA, ensure_ascii=False)}
- Return JSON only. No Markdown fences or explanatory text.
"""


def _generate_with_groq(prompt):
    """Generate a roadmap using Groq JSON mode."""
    api_key = st.secrets.get("GROQ_API_KEY")

    if not api_key:
        raise RuntimeError("GROQ_API_KEY is not configured.")

    client = Groq(
        api_key=api_key,
        max_retries=0,
        timeout=120,
    )

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are Guidoxis. Return one complete valid JSON "
                    "object only. Follow the supplied schema and keep "
                    "the roadmap concise."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        response_format={"type": "json_object"},
        temperature=0.2,
        max_completion_tokens=6500,
    )

    choice = response.choices[0]

    if not choice.message.content:
        raise ValueError("Groq returned an empty response.")

    if choice.finish_reason == "length":
        raise ValueError(
            "Groq reached its output token limit. "
            "Reduce the roadmap detail."
        )

    roadmap = _extract_roadmap(choice.message.content)

    return roadmap, GROQ_MODEL


def _generate_with_gemini(prompt):
    """Generate a roadmap using Gemini with limited retries."""
    api_key = st.secrets.get("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured."
        )

    client = genai.Client(api_key=api_key)
    last_error = None

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.1,
                    max_output_tokens=8000,
                    response_mime_type="application/json",
                ),
            )

            if not response.text:
                raise ValueError(
                    "Gemini returned an empty response."
                )

            try:
                roadmap = _extract_roadmap(response.text)
                return roadmap, GEMINI_MODEL

            except ValueError as parse_error:
                # Attempt one repair if Gemini returns malformed JSON.
                if attempt == 0:
                    repair_prompt = f"""
Fix this response into one complete valid JSON object.

Use this schema:
{json.dumps(ROADMAP_SCHEMA, ensure_ascii=False)}

Preserve the original roadmap information. Shorten it if needed.
Return JSON only. Do not add explanations.

INVALID RESPONSE:
{response.text[:18000]}
"""

                    repair = client.models.generate_content(
                        model=GEMINI_MODEL,
                        contents=repair_prompt,
                        config=types.GenerateContentConfig(
                            temperature=0,
                            max_output_tokens=8000,
                            response_mime_type="application/json",
                        ),
                    )

                    if repair.text:
                        try:
                            roadmap = _extract_roadmap(repair.text)
                            return roadmap, GEMINI_MODEL
                        except ValueError:
                            pass

                raise parse_error

        except Exception as exc:
            last_error = exc
            error_text = str(exc).lower()

            retryable = any(
                term in error_text
                for term in (
                    "503",
                    "unavailable",
                    "429",
                    "resource_exhausted",
                    "500",
                    "502",
                    "504",
                    "timeout",
                    "temporarily",
                )
            )

            if not retryable or attempt == 2:
                raise

            time.sleep(
                (2 ** attempt) + random.uniform(0.2, 0.8)
            )

    raise RuntimeError(f"Gemini failed: {last_error}")


@st.cache_data(ttl=3600, show_spinner=False)
def _generate_cached(profile_json, answers_json):
    """Cache identical requests for one hour."""
    profile = json.loads(profile_json)
    answers = json.loads(answers_json)

    prompt = _build_prompt(profile, answers)
    groq_error = None

    try:
        roadmap, model = _generate_with_groq(prompt)

        roadmap["model"] = model
        

        return roadmap

    except Exception as exc:
        groq_error = str(exc)

    try:
        roadmap, model = _generate_with_gemini(prompt)

        roadmap["model"] = model
        
        roadmap["fallback_reason"] = (
            "Groq was unavailable or failed; Gemini generated "
            "this roadmap."
        )

        return roadmap

    except Exception as gemini_error:
        raise RuntimeError(
            "Both providers failed.\n\n"
            f"Groq error: {groq_error}\n\n"
            f"Gemini error: {gemini_error}\n\n"
            "Check provider quotas, API keys, model availability, "
            "and internet connectivity."
        ) from gemini_error


def generate_researched_roadmap(
    profile: dict,
    followup_answers: dict | None = None,
    use_cache: bool = True,
) -> dict:
    """Public function used by app.py."""
    profile_json = json.dumps(
        profile,
        sort_keys=True,
        ensure_ascii=False,
        default=str,
    )

    answers_json = json.dumps(
        followup_answers or {},
        sort_keys=True,
        ensure_ascii=False,
        default=str,
    )

    if use_cache:
        return _generate_cached(profile_json, answers_json)

    return _generate_cached.__wrapped__(
        profile_json,
        answers_json,
    )
