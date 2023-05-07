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



openai_api_key = st.secrets["OPENAI_API_KEY"]


st.beta_set_page_config(page_title="Lesson Planner for Educators", page_icon=":robot:", layout="wide")

col1, col2, col3 = st.beta_columns(3)

with col1:
    st.markdown(
        """
        <style>
        .header {
            color: #fff;
            text-align: center;
            background-color: #00BFFF;
            padding: 5px;
            border-radius: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown('<h1 class="header">Lesson Planner for Educators</h1>', unsafe_allow_html=True)

with col2:
    option_grade = st.selectbox(
        'Grade level',
        ["Elementary School", "Middle School", "High School", "College", "Graduate School"],
        index=3
    )

with col3:
    subject = st.text_input("Subject", "")

lesson_description = st.text_input("What do you want the lesson to be about?", "")

if lesson_description:
    if not openai_api_key:
        st.warning(
            'Missing OpenAI API key',
            icon="⚠️")
        st.stop()

    llm = load_LLM(openai_api_key=openai_api_key)

    prompt_with_grade_and_description = prompt.format(grade=option_grade, lesson_description=lesson_description)

    lesson_plan = llm(prompt_with_grade_and_description)

    st.markdown(
        """
        <style>
        .lesson-plan {
            background-color: #eee;
            padding: 20px;
            border-radius: 10px;
            font-size: 16px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown('<div class="lesson-plan">{}</div>'.format("<br>".join(lesson_plan)), unsafe_allow_html=True)
