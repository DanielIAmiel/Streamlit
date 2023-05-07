import streamlit as st
from langchain import PromptTemplate
from langchain.llms import OpenAI

# Import the API key from apikey.py
import os

openai_api_key = st.secrets["OPENAI_API_KEY"]

template = """
    Please generate 5 bullet points for a lesson plan on {subject} for a {grade} class:
    {lesson_description}

    YOUR LESSON PLAN BULLET POINTS:
"""

prompt = PromptTemplate(
    input_variables=["subject", "grade", "lesson_description"],
    template=template,
)

def load_LLM(openai_api_key):
    llm = OpenAI(engine="davinci", temperature=0.5, max_tokens=100, top_p=1, frequency_penalty=0, presence_penalty=0, openai_api_key=openai_api_key)
    return llm

st.set_page_config(page_title="Lesson Planner for Educators", page_icon=":robot:")
st.header("Lesson Planner for Educators")

openai_api_key = st.secrets["OPENAI_API_KEY"]

col1, col2, col3 = st.columns([1, 1, 2])

with col1:
    option_grade = st.selectbox(
        'Which grade do you teach?',
        [str(x) for x in range(1, 13)])

with col2:
    lesson_subject = st.text_input("What subject do you want the lesson to be about?", "")

with col3:
    lesson_description = st.text_input("What do you want the lesson to be about?", "")

if lesson_description and lesson_subject:
    if not openai_api_key:
        st.warning(
            'Missing OpenAI API key',
            icon="⚠️")
        st.stop()

    llm = load_LLM(openai_api_key=openai_api_key)

    prompt_with_subject_grade_and_description = prompt.format(
        subject=lesson_subject,
        grade=option_grade, 
        lesson_description=lesson_description
    )

    lesson_plan = llm(prompt_with_subject_grade_and_description).choices[0].text.strip().split("\n")

    st.markdown("### Your Lesson Plan Bullet Points:")
    for point in lesson_plan:
        st.write("- " + point.strip())
