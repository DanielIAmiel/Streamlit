import os
from apikey import apikey

import streamlit as st
from langchain.llms import OpenAI

st.title('Title')
prompt = st.text_input('Plug in your prompt here')

llm = OpenAI(temperature = 0.9, openai_api_key = apikey)

if prompt:
    response = llm(prompt)
    st.write(response)

