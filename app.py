import streamlit as st
import openai

# Set up the page
st.set_page_config(page_title="Lesson Planner for Educators", page_icon=":mortar_board:")
st.title("Lesson Planner for Educators")

# Get OpenAI API key
openai_api_key = st.secrets["OPENAI_API_KEY"]
openai.api_key = openai_api_key

# Define the prompt template
template = """
Please generate a brief formatted lesson plan on the following topic for a {grade} {subject} class:
{lesson_description}

Difficulty level: {difficulty}

YOUR LESSON PLAN:
"""

# Define the form to get user input
with st.form("lesson_planner"):
    col1, col2 = st.columns([1, 2])

    with col1:
        option_grade = st.selectbox(
            'Grade level',
            ["Elementary School", "Middle School", "High School", "College", "Graduate School"],
            index=3
        )

    with col2:
        subject = st.text_input("Subject")

    difficulty = st.select_slider(
        "Difficulty level",
        ["Beginner", "Low-Intermediate", "Intermediate", "High-Intermediate", "Advanced"]
    )

    lesson_description = st.text_input("Lesson description")

    submit_button = st.form_submit_button(label="Generate Lesson Plan")

# Generate the lesson plan
if lesson_description and submit_button:
    if not openai_api_key:
        st.warning('Missing OpenAI API key')
        st.stop()

    prompt_with_grade_subject_difficulty_and_description = template.format(
        grade=option_grade,
        subject=subject,
        difficulty=difficulty,
        lesson_description=lesson_description
    )

    # Prepare and send the request to the OpenAI API
    with st.spinner("Generating lesson plan..."):
        completions = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt_with_grade_subject_difficulty_and_description,
            max_tokens=400,
            n=1,
            stop=None,
            temperature=0.7
        )

    # Display the generated lesson plan
    st.markdown("### Your Lesson Plan:")
    st.text_area("Generated Lesson Plan", completions.choices[0].text, height=1100, max_chars=None, key="lesson_plan")
