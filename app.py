import streamlit as st
import openai

# Import the API key from apikey.py
openai_api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="Lesson Planner for Educators", page_icon=":robot:")
st.header("Lesson Planner for Educators")

openai.api_key = openai_api_key

col1, col2, col3 = st.columns(3)
with col1:
    option_grade = st.selectbox(
        'Which grade do you teach?',
        [str(x) for x in range(1, 13)])

with col2:
    subject = st.text_input("Subject", "")

with col3:
    lesson_description = st.text_input("What do you want the lesson to be about?", "")

if lesson_description and subject:
    if not openai_api_key:
        st.warning(
            'Missing OpenAI API key',
            icon="⚠️")
        st.stop()

    prompt = f"""
    Please generate 5 bullet points for a lesson plan on the following topic for a {option_grade} {subject} class:
    {lesson_description}

    YOUR LESSON PLAN BULLET POINTS:
    """

    response = openai.Completion.create(
        engine="gpt-3.5-turbo",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )

    lesson_plan = response.choices[0].text.strip()

    st.markdown("### Your Lesson Plan Bullet Points:")
    st.write(lesson_plan)
