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
Please generate 5 bullet points for a lesson plan on the following topic for a {grade} class:
{lesson_description}

YOUR LESSON PLAN BULLET POINTS:
"""

prompt = PromptTemplate(
    input_variables=["grade", "lesson_description"],
    template=template,
)

# Load OpenAI LLM
def load_LLM(openai_api_key):
    llm = OpenAI(temperature=.7, openai_api_key=openai_api_key)
    return llm

# Define the form to get user input
with st.form("lesson_planner"):
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Let user choose the grade level
        option_grade = st.selectbox(
            'Which grade do you teach?',
            ["Elementary School", "Middle School", "High School", "College", "Graduate School"],
            index=3  # Set default value to College
        )

    with col2:
        # Let user input the subject
        subject = st.text_input("What is the subject of the lesson?")

        # Let user input the lesson description
        lesson_description = st.text_input("What do you want the lesson to be about?")

        # Let user input the difficulty level
        difficulty = st.selectbox(
            'Difficulty level',
            ["Beginner", "Intermediate", "Expert"],
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
        subject=subject,
        difficulty=difficulty,
        lesson_description=lesson_description
    )

    lesson_plan = llm(prompt_with_grade_subject_difficulty_and_description)

   
    # Display the generated lesson plan
st.markdown("### Your Lesson Plan Bullet Points:")
st.write(lesson_plan)

# Add a "Copy to Clipboard" button to copy the lesson plan to clipboard
st.write("")
copy_button = st.button("Copy to Clipboard")
if copy_button:
    st.experimental_set_query_params(text=lesson_plan)
    st.success("Copied to Clipboard")

# Add a "Tweet" button to share the lesson plan on Twitter
tweet_button = st.button("Tweet")
if tweet_button:
    tweet_text = f"Check out this lesson plan I generated on {option_grade} {lesson_description} using #OpenAI and #Streamlit! {st.share_twitter(lesson_plan)}"
    st.experimental_set_query_params(text=tweet_text)
    st.success("Tweeted!")

# Add a "Download" button to download the lesson plan as a text file
download_button = st.button("Download as Text File")
if download_button:
    st.download_button(
        label="Download Lesson Plan",
        data=lesson_plan,
        file_name=f"{option_grade}_{lesson_description}.txt",
        mime="text/plain",
    )



