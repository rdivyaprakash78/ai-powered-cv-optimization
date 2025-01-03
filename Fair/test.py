import streamlit as st
from extract_text import extract_text
from llm_helper import initiate_graph

st.title("Question Generation Test")

if "page" not in st.session_state:
    st.session_state["page"] = "home"

if "data" not in st.session_state:
    st.session_state.data = {}

if "answer" not in st.session_state:
    st.session_state.answer = None

if st.session_state.page == "home":

    with st.form(key = "init_form"):
        cv = st.file_uploader("Upload your CV here", type ="pdf")
        if cv:
            content = extract_text(cv)
            st.session_state.data["cv"] = content
        jd = st.text_area("Enter your job description here", height = 300,)
        if jd:
            st.session_state.data["jd"] = jd
        submit_button = st.form_submit_button("Submit")

    if submit_button:
        st.session_state.page = "generate_questions"
        st.rerun()

if st.session_state.page == "generate_questions":
    st.session_state["data"]["attributes"] = initiate_graph(st.session_state["data"]["jd"])
    st.session_state["data"]["sorted_attributes"] = sorted(st.session_state["data"]["attributes"], key=lambda att: att["priority"], reverse=True)
    
    st.markdown("\n")
    st.markdown("##### Assistant")
    st.write("Question")

    with st.form(key="form_answer"):
        user_input = st.text_input("", placeholder="Enter your text here")
        submit_button = st.form_submit_button("Submit")

    if submit_button :
        st.session_state.answer = user_input
        st.session_state.page = "generate_questions"
        st.rerun()

    