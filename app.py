from tempfile import NamedTemporaryFile
import os

import streamlit as st
from llama_index.core import VectorStoreIndex
from llama_index.llms.openai import OpenAI
from llama_index.readers.file import PDFReader
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="AI Resume Feedback Chat Bot",
    page_icon="🦙",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None,
)


if "messages" not in st.session_state.keys():  # Initialize the chat messages history
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi, You can upload your CV and ask me a question about your that!"}
    ]

uploaded_file = st.file_uploader("Upload your resume here")

if uploaded_file:
    bytes_data = uploaded_file.read()
    with NamedTemporaryFile(delete=False) as tmp:  
        tmp.write(bytes_data)  
        reader = PDFReader()
        docs = reader.load_data(tmp.name)
        llm = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_API_BASE"),
            model="gpt-3.5-turbo",
            temperature=0.0,
            system_prompt="You are a professional resume corrector in tech. You are taught that a strong resume should be brief but powerful, have strong action verbs (facilitated is not a strong action verb), and show impact of the experience. You will be provided with the document of the candidate's resume. Give detailed helpful feedback on what changes can be made to make the resume more effective. You should always tailor your response to the role the candidate is applying for. You should also provide a score out of 100 with different aspects (like structure, grammatical errors, related experience, Professional skills, and the impact of working outcomes). The score should reflect the quality of the resume for the role. Refer to the candidate as 'you' and the resume as 'your resume'. You should give specific suggestions for refinement. ",
        )
        index = VectorStoreIndex.from_documents(docs)
    os.remove(tmp.name)

    if "chat_engine" not in st.session_state.keys():  
        st.session_state.chat_engine = index.as_chat_engine(
            chat_mode="condense_question", verbose=False, llm=llm
        )

    st.session_state.file_processed = True

    if "initial_analysis_triggered" not in st.session_state:
        st.session_state.initial_analysis_triggered = True  
        initial_prompt = "Analyze my resume file and provide feedback with bullet and well-structured points."
        st.session_state.messages = [{"role": "user", "content": initial_prompt}]
        initial_response = st.session_state.chat_engine.stream_chat(initial_prompt)
        if initial_response and initial_response.response:
            st.session_state.messages.append({"role": "assistant", "content": initial_response.response})

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Upload your CV to start."}]

if prompt := st.chat_input("Your question"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    response = st.session_state.chat_engine.stream_chat(prompt)
    if response and response.response:
        st.session_state.messages.append({"role": "assistant", "content": response. response})


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.chat_engine.stream_chat(prompt)
            st.write_stream(response.response_gen)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message)  # Add response to message history
