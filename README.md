# 🧭 Guidoxis — AI-Powered Learning Roadmap Generator

### Turn your goals into a clear, actionable roadmap.

Guidoxis is an AI-powered decision-support application that transforms personal and professional goals into structured learning roadmaps. It helps users identify essential skills, discover learning resources, complete practical tasks, and track measurable milestones.

Built with Python and Streamlit, Guidoxis uses generative AI to make learning and career planning more accessible, structured, and actionable.

## ✨ Features

- 🎯 **Goal-Based Planning** — Generate personalized roadmaps based on individual goals.
- 🗺️ **Structured Learning Paths** — Break complex goals into manageable phases.
- 🧠 **Skill Identification** — Identify essential skills and knowledge areas.
- 📚 **Learning Resources** — Discover relevant learning materials.
- 🛠️ **Practical Tasks** — Apply concepts through hands-on activities.
- 📈 **Measurable Milestones** — Organize progress around achievable outcomes.
- 🤖 **Multiple AI Providers** — Support for Groq and Google Gemini APIs.
- 🌐 **Interactive Web Interface** — Access the application through Streamlit.
- 🔐 **Secure API Configuration** — Manage credentials through Streamlit Secrets.

## 🧰 Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Streamlit | Web interface |
| Groq API | AI-powered generation |
| Google Gemini API | Alternative AI provider |
| Requests | HTTP requests |
| Beautiful Soup | Web content parsing |
| Pydantic | Data validation |

## 📁 Project Structure

```text
guidoxis/
├── .streamlit/
│   └── secrets.toml
├── app.py
├── goal_engine.py
├── research_engine.py
├── roadmap_engine.py
├── requirements.txt
├── test_groq.py
├── .gitignore
└── README.md
