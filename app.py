import streamlit as st
from langchain import PromptTemplate
from langchain.llms import OpenAI

# Import the API key from apikey.py
import os

openai_api_key = st.secrets["OPENAI_API_KEY"]



template = """
    Please generate 5 bullet points for a {difficulty} level lesson plan on the following topic for a {grade} class:
    {lesson_description}

    YOUR LESSON PLAN BULLET POINTS:
"""

prompt = PromptTemplate(
    input_variables=["grade", "difficulty", "lesson_description"],
    template=template,
)

def load_LLM(openai_api_key):
    llm = OpenAI(temperature=.7, openai_api_key=openai_api_key)
    return llm

st.set_page_config(page_title="Lesson Planner for Educators", page_icon=":robot:")
st.header("Lesson Planner for Educators")

openai_api_key = st.secrets["OPENAI_API_KEY"]


col1, col2, col3 = st.columns(3)
with col1:
    option_grade = st.selectbox(
        'Grade level',
        ["Elementary School", "Middle School", "High School", "College", "Graduate School"],
        index=3)
    
with col2:
    difficulty = st.selectbox(
        'Difficulty level',
        ["Beginner", "Intermediate", "Expert"],
        index = 1)

with col3:
    lesson_description = st.text_input("What do you want the lesson to be about?", "")

if lesson_description:
    if not openai_api_key:
        st.warning(
            'Missing OpenAI API key',
            icon="⚠️")
        st.stop()

    llm = load_LLM(openai_api_key=openai_api_key)

    prompt_with_grade_and_description = prompt.format(grade=option_grade, lesson_description=lesson_description, difficulty=difficulty)

    lesson_plan = llm(prompt_with_grade_and_description)

    st.markdown("### Your Lesson Plan Bullet Points:")
    st.write(lesson_plan)
