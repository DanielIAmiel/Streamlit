import streamlit as st
from langchain import PromptTemplate
from langchain.llms import OpenAI

# Import the API key from apikey.py
import os

# Set page configuration
st.set_page_config(page_title="Lesson Planner for Educators", page_icon=":mortar_board:")

# Set up the OpenAI API key
openai_api_key = st.secrets["OPENAI_API_KEY"]

# Define the prompt for generating the lesson plan bullet points
template = """
    Please generate 5 bullet points for a lesson plan on the following topic for a {grade} class:
    {lesson_description}

    YOUR LESSON PLAN BULLET POINTS:
"""

prompt = PromptTemplate(
    input_variables=["grade", "lesson_description"],
    template=template,
)

# Define a function to load the OpenAI language model
def load_LLM(openai_api_key):
    llm = OpenAI(temperature=.7, openai_api_key=openai_api_key)
    return llm

# Define the layout of the page
st.title("Lesson Planner for Educators")
st.markdown("---")

# Get user input for grade level and lesson topic
col1, col2 = st.columns(2)
with col1:
    option_grade = st.selectbox(
        'Which grade do you teach?',
        ["Elementary School", "Middle School", "High School", "College", "Graduate School"],
        index=3
    )
with col2:
    lesson_description = st.text_input("What do you want the lesson to be about?", "")

# Generate the lesson plan bullet points if the user has entered a lesson topic
if lesson_description:
    if not openai_api_key:
        st.warning(
            'Missing OpenAI API key',
            icon="⚠️"
        )
        st.stop()

    # Load the OpenAI language model and generate the lesson plan bullet points
    llm = load_LLM(openai_api_key=openai_api_key)
    prompt_with_grade_and_description = prompt.format(grade=option_grade, lesson_description=lesson_description)
    lesson_plan = llm(prompt_with_grade_and_description)

    # Display the lesson plan bullet points
    st.markdown("---")
    st.markdown("### Your Lesson Plan Bullet Points:")
    st.write("\n- " + "\n- ".join(lesson_plan.split("\n")))
