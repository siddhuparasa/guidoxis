import streamlit as st
from groq import Groq

st.title("Guidoxis — Groq Connection Test")

try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)

    with st.spinner("Testing Groq and web research..."):
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "user",
                    "content": (
                        "Search the web for the official Python tutorial. "
                        "Give me its title, direct URL, and one sentence "
                        "explaining why it is useful for beginners."
                    ),
                }
            ],
            tools=[{"type": "browser_search"}],
            max_completion_tokens=1500,
            temperature=0.2,
        )

    st.success("Groq connection successful!")
    st.markdown(response.choices[0].message.content)

except Exception as e:
    st.error(f"Connection failed: {e}")