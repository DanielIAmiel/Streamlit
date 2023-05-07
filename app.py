import streamlit as st
from langchain import PromptTemplate
from langchain.llms import OpenAI

# Import the API key from apikey.py
import os

# Set up the page
st.set_page_config(page_title="Lesson Planner for Educators", page_icon=":mortar_board:")
st.title("Lesson Planner for Educators")

# Get OpenAI API key
openai_api_key = st.secrets["OPENAI_API_KEY"]

# Define the prompt template
template = """
Please generate 5 bullet points for a {difficulty} {subject} lesson plan on the following topic for a {grade} class:
{lesson_description}

YOUR LESSON PLAN BULLET POINTS:
"""

prompt = PromptTemplate(
    input_variables=["grade", "lesson_description", "subject", "difficulty"],
    template=template,
)

# Load OpenAI LLM
def load_LLM(openai_api_key):
    llm = OpenAI(temperature=.7, openai_api_key=openai_api_key)
    return llm

# Define the form to get user input
with st.form("lesson_planner"):
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        # Let user choose the grade level
        option_grade = st.selectbox(
            'Grade level',
            ["Elementary School", "Middle School", "High School", "College", "Graduate School"],
            index=3  # Set default value to College
        )
    
    with col2:
        # Let user input the lesson description
        lesson_description = st.text_input("Lesson description")
        
        # Let user choose the subject
        option_subject = st.selectbox(
            'Subject',
            ["Math", "Science", "English", "Social Studies", "Other"],
            index=0  # Set default value to Math
        )
        
        # Let user choose the difficulty level
        option_difficulty = st.selectbox(
            'Difficulty level',
            ["Beginner", "Intermediate", "Advanced"],
            index=1  # Set default value to Intermediate
        )
    
    # Let user submit the form
    submit_button = st.form_submit_button(label="Generate Lesson Plan")

# Generate the lesson plan
if lesson_description and submit_button:
    if not openai_api_key:
        st.warning('Missing OpenAI API key')
        st.stop()

    llm = load_LLM(openai_api_key=openai_api_key)
    prompt_with_grade_subject_difficulty_and_description = prompt.format(
        grade=option_grade, 
        lesson_description=lesson_description,
        subject=option_subject,
        difficulty=option_difficulty
    )
    lesson_plan = llm(prompt_with_grade_subject_difficulty_and_description)

    # Display the generated lesson plan
    st.markdown("### Your Lesson Plan Bullet Points:")
    st.write(lesson_plan)
